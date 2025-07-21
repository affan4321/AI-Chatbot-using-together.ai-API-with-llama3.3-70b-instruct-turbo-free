# AI Chatbot - Standalone Executable

A simple command-line AI chatbot powered by Together.ai's Llama 3.3 70B model with real-time streaming and typing effects.

## Features

- 🤖 **AI-powered responses** using Llama 3.3 70B Instruct Turbo
- ⚡ **Real-time streaming** with typing effect
-  **Interactive command-line interface**
- 📦 **Standalone executable** - no Python installation required

## For End Users

### Download and Run

1. Download the `AI_Chatbot.exe` file from this link: https://drive.google.com/file/d/1v_10cvEuinb373NhlHG3WBea_mbI-D-h/view?usp=sharing
2. Double-click to run
3. Start chatting with the AI!
4. Type `exit` to quit

### Usage

- The chatbot will start with a welcome screen
- Type your messages and press Enter
- The AI will respond with a realistic typing effect
- Simple and intuitive interface

---

## For Developers

### Creating the Executable

If you want to build the executable yourself:

### Quick Build (Recommended)

Run the automated build script:
```bash
python build_executable.py
```

### Manual Build

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create executable:**
   ```bash
   pyinstaller --onefile --console --name "AI_Chatbot" chatbot.py
   ```

3. **Find your executable in the `dist/` folder**

### Distribution

1. Take the executable from the `dist/` folder
2. Distribute the single `.exe` file
3. Users can run it directly without any setup

### Technical Details

- **File Size:** ~50-100MB (includes Python runtime)
- **Platform:** Windows executable (create separate builds for Mac/Linux)
- **Dependencies:** All included in the executable
- **No Installation Required:** Users just run the .exe file
