import cv2
import math
import numpy as np
import moviepy.editor as mpy
from dataclasses import dataclass
from typing import List, Tuple
import contextlib
import wave

@dataclass
class VisualAgent:
    name: str
    position: Tuple[int, int]
    color: Tuple[int, int, int]

class VisualDemo:
    def __init__(self, width=1280, height=900):
        self.width = width
        self.height = height
        
        # Adjusted vertical positions to better space out agents
        center_y = height//2 - 50
        self.agents = [
            VisualAgent("Customer", (width//2, 100), (65, 105, 225)),
            VisualAgent("Receptionist", (width//2, center_y), (50, 168, 82)),
            VisualAgent("Technical Agent", (width//2 + 300, center_y), (50, 120, 168)),
            VisualAgent("Sales Agent", (width//2 - 300, center_y), (168, 50, 120)),
            VisualAgent("Support Agent", (width//2 + 200, center_y + 180), (120, 168, 50)),
            VisualAgent("Billing Agent", (width//2 - 200, center_y + 180), (168, 120, 50)),
            VisualAgent("Customer Success", (width//2, center_y + 280), (120, 50, 168))
        ]

    def create_frame(self, speaking_agent: str, current_text: str, time: float):
        # Create base image
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 245
        
        # Draw connections
        for i, agent1 in enumerate(self.agents):
            for j, agent2 in enumerate(self.agents[i+1:], i+1):
                if abs(i - j) <= 2:
                    cv2.line(img, 
                            agent1.position, 
                            agent2.position, 
                            (200, 200, 200), 
                            1)
        
        # Draw agents and animations
        for agent in self.agents:
            is_speaking = agent.name == speaking_agent
            
            # Draw wave animation for speaking agent
            if is_speaking:
                for i in range(3):
                    wave_radius = 35 + 10 + int(10 * math.sin(time * 5 + i * 2))
                    alpha = max(0, 1 - (wave_radius - 35) / 20)
                    overlay = img.copy()
                    cv2.circle(overlay, agent.position, wave_radius, (100, 100, 255), 2)
                    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            
            # Draw agent circle
            cv2.circle(img, agent.position, 35,
                      agent.color if is_speaking else (150, 150, 150), 
                      -1)
            
            # Draw agent name
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(agent.name, font, 0.7, 2)[0]
            text_x = agent.position[0] - text_size[0] // 2
            text_y = agent.position[1] + 60
            cv2.putText(img, agent.name, (text_x, text_y), 
                       font, 0.7, (0, 0, 0), 2)
        
        # Draw conversation box
        margin = 40
        box_height = 120
        box_y = self.height - box_height - margin
        
        # Draw box with rounded corners
        cv2.rectangle(img, 
                     (margin, box_y),
                     (self.width - margin, self.height - margin),
                     (255, 255, 255),
                     -1)
        cv2.rectangle(img, 
                     (margin, box_y),
                     (self.width - margin, self.height - margin),
                     (200, 200, 200),
                     2)
        
        # Add text to conversation box
        text = f"{speaking_agent}: {current_text}"
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= 100:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        y_offset = box_y + 35
        for line in lines[:3]:
            cv2.putText(img, line, (margin + 30, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            y_offset += 30
            
        return img

    def generate_video(self, conversation_data, output_path="agent_conversation_demo.mp4"):
        video_writer = cv2.VideoWriter(
            'temp_video.mp4',
            cv2.VideoWriter_fourcc(*'mp4v'),
            30,
            (self.width, self.height)
        )
        
        # Get durations of all audio files
        audio_durations = []
        for turn in conversation_data:
            if turn.get("audio_file"):
                with contextlib.closing(wave.open(turn["audio_file"], 'r')) as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    duration = frames / float(rate)
                    audio_durations.append(max(duration + 0.5, 2.0))
            else:
                audio_durations.append(2.0)
        
        # Generate frames
        for turn_idx, turn in enumerate(conversation_data):
            n_frames = int(audio_durations[turn_idx] * 30)
            
            for frame_num in range(n_frames):
                frame = self.create_frame(
                    turn["speaker"],
                    turn["text"],
                    frame_num / 30
                )
                video_writer.write(frame)
        
        video_writer.release()
        
        # Add audio
        video = mpy.VideoFileClip("temp_video.mp4")
        audio_clips = []
        current_time = 0
        
        for turn_idx, turn in enumerate(conversation_data):
            if turn.get("audio_file"):
                audio = mpy.AudioFileClip(turn["audio_file"])
                audio = audio.set_start(current_time)
                audio_clips.append(audio)
            current_time += audio_durations[turn_idx]
        
        if audio_clips:
            final_audio = mpy.CompositeAudioClip(audio_clips)
            final_video = video.set_audio(final_audio)
        else:
            final_video = video
        
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Cleanup
        video.close()
        if audio_clips:
            for clip in audio_clips:
                clip.close()
        
        try:
            import os
            os.remove("temp_video.mp4")
        except:
            pass
