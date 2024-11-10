# Voice Enabled Swarm of Agents Ft OpenAI-Swarm 🐝-X-TTS 🐸

Voice Enabled Swarm of Agents aims to achieve tasks between autonomous agent entities built with OpenAI Swarm and Coqui TTS.


![Demo Screenshot](https://imgur.com/L6Y0tbB.png)
The Customer here is itself an LLM which is autonomously interacting with the swarm of agents that represent a company, which in our case is a business that sells API. 


![Demo Screenshot](https://imgur.com/MVd6sCj.png)


## Demo
Watch the demo video to see the system in action:
[!YOUTUBE](https://www.youtube.com/watch?v=UsvBG0dQjMk)


## Features

- Multiple specialized AI agents (Sales, Technical, Support, etc.)
- Voice synthesis with character-specific voices
- Dynamic conversation visualization
- Automated agent handoff based on conversation context
- Audio generation and conversation recording

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Raj-08/OpenAI-Swarm-X-TTS.git
cd OpenAI-Swarm-X-TTS
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_api_key_here
```

5. Add voice samples:
Place your voice sample files in the `voices/` directory with the following names:
- receptionist.mp3
- sales.mp3
- support.mp3
- billing.mp3
- technical.mp3
- success.mp3
- customer.mp3

## Usage

Run the demo:
```bash
python src/main.py
```

## Project Structure

- `src/`: Source code
  - `voice_system/`: Core system components
  - `utils/`: Utility functions
- `voices/`: Voice sample files
- `temp_audio/`: Temporary audio files (created at runtime)

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
