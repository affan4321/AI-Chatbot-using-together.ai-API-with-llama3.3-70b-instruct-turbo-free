#!/usr/bin/env python3
"""
AI Chatbot Build Script - Simple and Reliable
Creates a standalone executable with embedded API key
"""

import subprocess
import sys
import os
import shutil

def load_api_key():
    """Load API key from .env file"""
    api_key = None
    
    if os.path.exists('.env'):
        print("🔑 Loading API key from .env file...")
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('TOGETHER_API_KEY='):
                        api_key = line.strip().split('=', 1)[1].strip()
                        if api_key.startswith('"') and api_key.endswith('"'):
                            api_key = api_key[1:-1]
                        elif api_key.startswith("'") and api_key.endswith("'"):
                            api_key = api_key[1:-1]
                        break
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
            return None
    
    if not api_key:
        print("❌ Error: No API key found!")
        return None
    
    print("✅ API key loaded successfully")
    return api_key

def prepare_distribution_file(api_key):
    """Create a distribution version with embedded API key"""
    print("📝 Creating distribution version...")
    
    with open('chatbot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replacements
    content = content.replace('return None', f'return "{api_key}"')
    content = content.replace(
        "if not api_key or api_key == 'YOUR_API_KEY_HERE':",
        "if False:  # Disabled for distribution"
    )
    
    with open('chatbot_dist.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Distribution file created")
    return 'chatbot_dist.py'

def build_executable():
    """Build the standalone executable"""
    print("🔨 Building standalone executable...")
    
    api_key = load_api_key()
    if not api_key:
        return False
    
    dist_file = prepare_distribution_file(api_key)
    
    # Simple build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--console',
        '--name', 'AI_Chatbot',
        '--distpath', 'dist',
        '--clean',
        '--noconfirm',
        dist_file
    ]
    
    print("⚡ Running PyInstaller...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Check file
            exe_path = os.path.join('dist', 'AI_Chatbot.exe')
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📦 Executable size: {size_mb:.1f} MB")
                print(f"📁 Location: {os.path.abspath(exe_path)}")
            
            # Clean up
            for cleanup in [dist_file, 'AI_Chatbot.spec']:
                if os.path.exists(cleanup):
                    os.remove(cleanup)
                    print(f"🧹 Cleaned up: {cleanup}")
            
            if os.path.exists('build'):
                shutil.rmtree('build')
                print("🧹 Cleaned up build directory")
            
            print()
            print("🎉 SUCCESS! Your executable is ready for distribution!")
            print("📦 The executable includes:")
            print("   ✅ Embedded API key (no setup needed)")
            print("   ✅ All dependencies included")
            print("   ✅ Unicode/emoji support with fallback")
            print("   ✅ Works on all Windows systems")
            return True
        else:
            print("❌ Build failed!")
            print("Error:", result.stderr[:500])
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out!")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Chatbot Build Script")
    print("=" * 30)
    
    # Check dependencies
    try:
        import PyInstaller
        print("✅ PyInstaller is available")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    try:
        import together
        print("✅ Together.ai library is available")
    except ImportError:
        print("❌ Together library not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'together'])
    
    success = build_executable()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Test the executable on this machine")
        print("2. Upload to your preferred hosting service")
        print("3. Share the download link")
        print("4. Users download and run - no setup needed!")
        sys.exit(0)
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)
