# AI Chatbot with Together.ai API

A simple command-line chatbot powered by Together.ai's Llama 3.3 70B model with real-time streaming and typing effects.

## Features

- 🤖 **AI-powered responses** using Llama 3.3 70B Instruct Turbo
- ⚡ **Real-time streaming** with typing effect
- 🔒 **Secure API key management** with environment variables
- 💬 **Interactive command-line interface**

## Prerequisites

- Python 3.7 or higher
- Together.ai API account and API key

## Setup Instructions

### 1. Clone or Download the Repository

```bash
git clone https://github.com/affan4321/AI-Chatbot-using-together.ai-API-with-llama3.3-70b-instruct-turbo-free
cd "AI Chatbot using together.ai API with llama3.3-70b-instruct-turbo-free"
```

### 2. Create a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

#### Method 1: Using .env file (Recommended)

1. Create a `.env` file in the project root:
   ```bash
   # On Windows PowerShell
   New-Item -Path ".env" -ItemType File
   
   # On macOS/Linux
   touch .env
   ```

2. Add your Together.ai API key to the `.env` file:
   ```env
   TOGETHER_API_KEY=your_api_key_here
   ```

#### Method 2: System Environment Variables

**On Windows:**
```powershell
$env:TOGETHER_API_KEY="your_api_key_here"
```

**On macOS/Linux:**
```bash
export TOGETHER_API_KEY="your_api_key_here"
```

### 5. Get Your Together.ai API Key

1. Go to [Together.ai](https://api.together.xyz/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Generate a new API key
5. Copy the key and add it to your `.env` file

### 6. Run the Chatbot

```bash
python chatbot.py
```

## Usage

1. Start the chatbot with `python chatbot.py`
2. Type your messages and press Enter
3. The AI will respond with a realistic typing effect
4. Type `exit` to quit the chatbot

## 🔒 API Key Security Best Practices

### ✅ DO:

1. **Use .env files** - Store your API key in a `.env` file (already implemented)
2. **Add .env to .gitignore** - Prevent accidentally committing your API key
3. **Use environment variables** - Never hardcode API keys in your source code
4. **Rotate keys regularly** - Generate new API keys periodically
5. **Use different keys for different environments** (development, staging, production)

### ❌ DON'T:

1. **Never commit API keys** to version control
2. **Don't share .env files** publicly
3. **Don't hardcode keys** in source code
4. **Don't use the same key** across multiple projects
5. **Don't store keys** in plain text files that get shared

### Additional Security Measures:

1. **Create a .gitignore file:**
   ```gitignore
   .env
   __pycache__/
   *.pyc
   venv/
   .vscode/
   ```

2. **Use key restrictions** if available on Together.ai (IP restrictions, usage limits)

3. **Monitor API usage** regularly for unexpected activity

4. **Use secrets management** for production deployments (AWS Secrets Manager, Azure Key Vault, etc.)

## Project Structure

```
AI Chatbot using together.ai API with llama3.3-70b-instruct-turbo-free/
├── chatbot.py          # Main chatbot application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore file (recommended)
└── README.md          # This file
```

## Customization

### Adjust Typing Speed

In `chatbot.py`, modify the `time.sleep()` value:
```python
time.sleep(0.02)  # Slower typing
time.sleep(0.01)  # Faster typing
time.sleep(0.005) # Very fast typing
```

### Switch Models

Change the model in the `__init__` method:
```python
# Faster alternatives:
self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
self.model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
```

## Troubleshooting

### Common Issues:

1. **"API key not found"** - Ensure your `.env` file contains `TOGETHER_API_KEY=your_key`
2. **"Module not found"** - Run `pip install -r requirements.txt`
3. **"Slow responses"** - Try a smaller model or check your internet connection
4. **"Virtual environment issues"** - Ensure the virtual environment is activated

### Getting Help:

- Check Together.ai [documentation](https://docs.together.ai/)
- Verify your API key is valid and has sufficient credits
- Ensure all dependencies are properly installed

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy Chatting! **
