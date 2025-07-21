#!/usr/bin/env python3
"""
Simplified build script to create a standalone executable for public distribution
This script automatically embeds your API key from .env file into the executable
"""

import subprocess
import sys
import os
import shutil

def load_api_key():
    """Load API key from .env file"""
    api_key = None
    
    # Try to load from .env file
    if os.path.exists('.env'):
        print("🔑 Loading API key from .env file...")
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('TOGETHER_API_KEY='):
                        api_key = line.strip().split('=', 1)[1].strip()
                        # Remove quotes if present
                        if api_key.startswith('"') and api_key.endswith('"'):
                            api_key = api_key[1:-1]
                        elif api_key.startswith("'") and api_key.endswith("'"):
                            api_key = api_key[1:-1]
                        break
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    
    # Try to load from environment variable
    if not api_key:
        api_key = os.getenv('TOGETHER_API_KEY')
        if api_key:
            print("🔑 Loading API key from environment variable...")
    
    if not api_key:
        print("❌ Error: No API key found!")
        print("   Please add TOGETHER_API_KEY to your .env file or environment variables")
        return None
    
    if len(api_key) < 10:
        print("❌ Error: API key seems invalid (too short)")
        return None
    
    print("✅ API key loaded successfully")
    return api_key

def embed_api_key_in_chatbot(api_key):
    """Create a version of chatbot.py with embedded API key"""
    print("🔧 Embedding API key into chatbot...")
    
    try:
        # Read original chatbot.py with UTF-8 encoding to handle Unicode characters
        with open('chatbot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First, add sys import for exit() function
        if 'import sys' not in content:
            content = content.replace('import os', 'import os\nimport sys')
        
        # Replace exit(1) with sys.exit(1) in all instances
        content = content.replace('exit(1)', 'sys.exit(1)')
        
        # Replace the API key loading method with direct embedding
        old_api_call = "        api_key = self.load_api_key()"
        new_api_call = f"        api_key = '{api_key}'"
        
        if old_api_call in content:
            content = content.replace(old_api_call, new_api_call)
            
            # Also remove the load_api_key method definition
            load_method_start = "    def load_api_key(self):"
            load_method_end = "        return 'YOUR_API_KEY_HERE'"
            
            start_pos = content.find(load_method_start)
            if start_pos != -1:
                end_pos = content.find(load_method_end, start_pos)
                if end_pos != -1:
                    end_pos = content.find('\n', end_pos) + 1
                    content = content[:start_pos] + content[end_pos:]
        else:
            # Fallback: replace any occurrence of placeholder
            content = content.replace("'YOUR_API_KEY_HERE'", f"'{api_key}'")
            content = content.replace('"YOUR_API_KEY_HERE"', f'"{api_key}"')
        
        # Remove warning blocks about placeholder API keys
        warning_patterns = [
            '''        if api_key == 'YOUR_API_KEY_HERE':
            print("⚠️  Warning: Using placeholder API key. Please set your actual API key.")
            print("   For development: Set TOGETHER_API_KEY environment variable")
            print("   For distribution: Replace 'YOUR_API_KEY_HERE' in the code with your key")
            print()''',
            '''if api_key == 'YOUR_API_KEY_HERE':
            print("⚠️  Warning: Using placeholder API key. Please set your actual API key.")
            print("   For development: Set TOGETHER_API_KEY environment variable")
            print("   For distribution: Replace 'YOUR_API_KEY_HERE' in the code with your key")
            print()'''
        ]
        
        for pattern in warning_patterns:
            if pattern in content:
                content = content.replace(pattern, "        # API key is embedded for distribution")
        
        # Write to temporary file for building with UTF-8 encoding
        with open('chatbot_build.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ API key embedded successfully")
        print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")  # Show partial key for verification
        print("🔧 Fixed sys.exit() imports")
        return True
        
    except Exception as e:
        print(f"❌ Error embedding API key: {e}")
        return False

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def build_standalone_executable():
    """Build a standalone executable with embedded API key"""
    print("🔨 Building standalone executable...")
    
    # Command to create a single, standalone executable
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file
        "--console",                    # Keep console window
        "--name", "AI_Chatbot",         # Custom name
        "--clean",                      # Clean build
        "--noconfirm",                  # Overwrite without asking
        "chatbot_build.py"              # Use the modified file with embedded API key
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Standalone executable created successfully!")
        print("📁 Location: dist/AI_Chatbot.exe")
        print("📦 File size: ~50-100MB (includes everything needed)")
        print("🎉 Ready for public distribution!")
        print("\n📋 Distribution Notes:")
        print("   • Users just need to download and run the .exe file")
        print("   • No Python installation required")
        print("   • No setup or configuration needed")
        print("   • API key is embedded - no .env file needed")
        print("   • Works on any Windows computer")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def clean_build_files():
    """Clean up build artifacts"""
    # Remove build artifacts
    artifacts = ["build", "AI_Chatbot.spec", "__pycache__", "chatbot_build.py"]
    
    for artifact in artifacts:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                shutil.rmtree(artifact)
                print(f"🧹 Cleaned up {artifact}/")
            else:
                os.remove(artifact)
                print(f"🧹 Cleaned up {artifact}")

def main():
    print("🚀 AI Chatbot - Public Distribution Builder")
    print("=" * 50)
    
    # Check if chatbot.py exists
    if not os.path.exists("chatbot.py"):
        print("❌ Error: chatbot.py not found in current directory")
        print("   Make sure you're running this script in the project folder")
        return
    
    # Load API key from .env or environment
    api_key = load_api_key()
    if not api_key:
        return
    
    # Embed API key into chatbot
    if not embed_api_key_in_chatbot(api_key):
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_standalone_executable():
        # Clean up build files
        clean_build_files()
        
        print("\n🎉 BUILD COMPLETE!")
        print("🎯 Your executable is ready for public distribution:")
        print("   📁 File: dist/AI_Chatbot.exe")
        print("   💾 Size: ~50-100MB")
        print("   🖥️  Platform: Windows")
        print("   📦 Dependencies: All included")
        print("   🔑 API Key: Embedded (no .env file needed)")
        print("\n📤 Distribution Instructions:")
        print("   1. Upload 'AI_Chatbot.exe' to your preferred platform")
        print("   2. Users download and double-click to run")
        print("   3. No additional setup required!")
        print("   4. Users don't need API keys or .env files!")
        
    else:
        # Clean up even if build failed
        clean_build_files()
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
