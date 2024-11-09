import os
from dotenv import load_dotenv
from voice_system.core import EnhancedCorporateVoiceSystem

def run_creative_demo():
    """Run the enhanced demo with dynamic interactions and full context"""
    system = EnhancedCorporateVoiceSystem()
    
    print("\n=== Enhanced Corporate Voice Agent Demo ===")
    print("Press Ctrl+C to end the conversation")
    
    current_response = None
    current_agent = system.receptionist
    message_count = 0
    
    # Initial query
    user_input = """Hi, I'm researching enterprise software solutions for my company. 
    We have specific security requirements and need to understand your API capabilities."""
    
    while True:
        try:
            # Process input with current agent
            if current_response is None:
                current_response = system.client.run(
                    agent=current_agent,
                    messages=[{"role": "user", "content": user_input}]
                )
            else:
                messages = current_response.messages + [{"role": "user", "content": user_input}]
                current_response = system.client.run(
                    agent=current_response.agent,
                    messages=messages
                )
            
            # Handle agent response
            assistant_message = current_response.messages[-1]["content"]
            print(f"\n{current_response.agent.name}: {assistant_message}")
            
            # Add agent response to full conversation history
            system.full_conversation_history.append({
                "role": "assistant",
                "sender": current_response.agent.name,
                "content": assistant_message
            })
            
            # Generate speech
            system.generate_speech(
                assistant_message, 
                current_response.agent.name,
                message_count
            )
            
            message_count += 1
            
            # Get dynamic customer response with full context
            user_input = system.get_llm_response(system.full_conversation_history)
            print(f"\nCustomer: {user_input}")
            
            # Add customer response to full conversation history
            system.full_conversation_history.append({
                "role": "user",
                "sender": "Customer",
                "content": user_input
            })
            
            # Generate customer speech
            system.generate_speech(user_input, "Customer", message_count)
            
            message_count += 1
            
        except KeyboardInterrupt:
            print("\n\nEnding conversation...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    system.stitch_conversation()

if __name__ == "__main__":
    load_dotenv()
    run_creative_demo()
