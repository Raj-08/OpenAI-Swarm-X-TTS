import os
from openai import OpenAI
from TTS.api import TTS
from swarm import Swarm
from .agents import initialize_enhanced_agents
from ..utils.audio import stitch_audio_files
from .visualization import VisualDemo

class EnhancedCorporateVoiceSystem:
    def __init__(self):
        self.client = Swarm()
        self.openai_client = OpenAI()
        
        print("Loading XTTS model...")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
        
        self.voice_configs = {
            "Receptionist": "voices/receptionist.mp3",
            "Sales Agent": "voices/sales.mp3",
            "Support Agent": "voices/support.mp3",
            "Billing Agent": "voices/billing.mp3",
            "Technical Agent": "voices/technical.mp3",
            "Customer Success": "voices/success.mp3",
            "Customer": "voices/customer.mp3"
        }
        
        self.conversation_audio_files = []
        self.full_conversation_history = []
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize all agents and their functions"""
        agents = initialize_enhanced_agents(self)
        self.receptionist = agents["receptionist"]
        self.sales_agent = agents["sales"]
        self.technical_agent = agents["technical"]
        self.customer_success = agents["success"]
        self.support_agent = agents["support"]
        self.billing_agent = agents["billing"]

    def generate_speech(self, text, speaker_name, message_count):
        """Generate speech using XTTS with voice cloning"""
        try:
            os.makedirs("temp_audio", exist_ok=True)
            output_path = f"temp_audio/speech_{message_count:03d}_{speaker_name.lower().replace(' ', '_')}.wav"
            
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=self.voice_configs[speaker_name],
                language="en"
            )
            
            self.conversation_audio_files.append(output_path)
            print(f"Generated speech: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

    def get_llm_response(self, conversation_history):
        """Get dynamic customer responses while maintaining clear role distinction"""
        try:
            formatted_messages = [
                {"role": "system", "content": """You are a CUSTOMER inquiring about enterprise software. 
                
                Your background:
                - You represent a mid-sized company looking for software solutions
                - You have genuine questions about technical features, pricing, and implementation
                - You respond naturally as someone evaluating a product
                
                Guidelines:
                - Always speak AS THE CUSTOMER asking questions or responding to information
                - Be concise (under 40 words)
                - Ask relevant follow-up questions
                - Express your needs and concerns
                - If agent mentions transferring you, simply agree politely
                """}
            ]
    
            for msg in conversation_history:
                if msg["role"] == "assistant":
                    formatted_messages.append({
                        "role": "assistant",
                        "content": f"[{msg['sender']}] {msg['content']}"
                    })
                else:
                    formatted_messages.append({
                        "role": "user",
                        "content": f"[Customer] {msg['content']}"
                    })
    
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=formatted_messages,
                max_tokens=100,
                temperature=0.7
            )
    
            customer_response = response.choices[0].message.content
            customer_response = customer_response.replace("[Customer]", "").strip()
            
            return customer_response
    
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return "Could you please explain that further?"

    def stitch_conversation(self):
        """Combine all audio files and create visualization"""
        try:
            if not self.conversation_audio_files:
                print("No audio files to stitch together")
                return

            print("\nStitching conversation audio files...")
            
            # Stitch audio files
            stitch_audio_files(self.conversation_audio_files, "full_conversation.wav")
            
            # Create visualization
            self.create_visualization()
            
            # Cleanup temporary files
            for file in self.conversation_audio_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error removing temporary file {file}: {e}")
            
            print("Temporary files cleaned up")
            
        except Exception as e:
            print(f"Error stitching conversation: {e}")

    def create_visualization(self):
        """Create visualization video from conversation history"""
        conversation_data = []
        
        for msg in self.full_conversation_history:
            speaker = msg["sender"]
            text = msg["content"]
            audio_index = len(conversation_data)
            
            audio_file = None
            if audio_index < len(self.conversation_audio_files):
                audio_file = self.conversation_audio_files[audio_index]
            
            conversation_data.append({
                "speaker": speaker,
                "text": text,
                "audio_file": audio_file
            })
        
        demo = VisualDemo()
        demo.generate_video(conversation_data, "agent_conversation_demo.mp4")
        print("Visualization saved as: agent_conversation_demo.mp4")
