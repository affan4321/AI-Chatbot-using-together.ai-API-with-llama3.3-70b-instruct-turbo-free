#!/usr/bin/env python3
"""
Simplified build script to create a standalone executable for public distribution
This script embeds the API key directly in the executable for easy distribution
"""

import subprocess
import sys
import os

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
        "chatbot.py"
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
        print("   • Works on any Windows computer")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def clean_build_files():
    """Clean up build artifacts"""
    import shutil
    
    # Remove build artifacts
    artifacts = ["build", "AI_Chatbot.spec", "__pycache__"]
    
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
        print("\n📤 Distribution Instructions:")
        print("   1. Upload 'AI_Chatbot.exe' to your preferred platform")
        print("   2. Users download and double-click to run")
        print("   3. No additional setup required!")
        
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
