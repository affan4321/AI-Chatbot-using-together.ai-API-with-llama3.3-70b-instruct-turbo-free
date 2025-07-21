# AI Chatbot - Standalone Executable

A simple command-line AI chatbot powered by Together.ai's Llama 3.3 70B model with real-time streaming and typing effects.

## Features

- 🤖 **AI-powered responses** using Llama 3.3 70B Instruct Turbo
- ⚡ **Real-time streaming** with typing effect
-  **Interactive command-line interface**
- 📦 **Standalone executable** - no Python installation required

## For End Users

### Download and Run

1. Download the `AI_Chatbot.exe` file from this link: https://drive.google.com/file/d/1UgJJRJsZ_HzrPlFnwIYM2ozTj2DA5Vbm/view?usp=sharing
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

To build the executable with embedded API key for public distribution:

### Quick Build (Recommended)

1. **Run the setup and build script:**
   ```bash
   python setup_and_build.py
   ```

2. **Enter your Together.ai API key when prompted**

3. **Find your executable in the `dist/` folder**

### Manual Build

1. **Install dependencies:**
   ```bash
   pip install together pyinstaller
   ```

2. **Edit chatbot.py and replace `YOUR_API_KEY_HERE` with your actual API key**

3. **Create executable:**
   ```bash
   pyinstaller --onefile --console --name "AI_Chatbot" chatbot.py
   ```

4. **Find your executable in the `dist/` folder**

### Distribution

1. Take the executable from the `dist/` folder
2. Upload to your preferred hosting (Google Drive, GitHub Releases, etc.)
3. Share the download link
4. Users download and run immediately - no setup needed!

### Technical Details

- **File Size:** ~50-100MB (includes Python runtime and dependencies)
- **Platform:** Windows executable (create separate builds for Mac/Linux)
- **API Key:** Embedded directly in executable
- **Dependencies:** All included
- **User Requirements:** None - just download and run

### Security Note

⚠️ **Important:** Your API key will be embedded in the executable. Monitor your API usage and consider rate limiting on your Together.ai account.
