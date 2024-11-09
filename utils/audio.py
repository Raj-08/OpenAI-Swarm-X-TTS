import numpy as np
import soundfile as sf

def stitch_audio_files(audio_files, output_path):
    """Combine multiple audio files into a single conversation with pauses"""
    if not audio_files:
        return
        
    # Read the first file to get parameters
    data, sample_rate = sf.read(audio_files[0])
    
    # Initialize combined audio
    combined = data
    
    # Add small pause between segments (0.5 second)
    pause_duration = int(0.5 * sample_rate)
    pause = np.zeros(pause_duration)
    
    # Concatenate all audio files with pauses
    for audio_file in audio_files[1:]:
        combined = np.concatenate([combined, pause])
        data, _ = sf.read(audio_file)
        combined = np.concatenate([combined, data])
    
    # Save combined audio
    sf.write(output_path, combined, sample_rate)
    print(f"Combined audio saved to: {output_path}")
