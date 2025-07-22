from together import Together
import time
import os
import sys
import subprocess
import locale

class Chatbot:
    def __init__(self):
        # API Key Configuration
        # For development: Load from environment or .env file
        # For distribution: Will be replaced with embedded key during build
        api_key = self.load_api_key()
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            safe_print("[WARNING] No valid API key found!")
            safe_print("   For development: Set TOGETHER_API_KEY environment variable or add to .env file")
            safe_print("   For distribution: API key will be embedded during build process")
            safe_print("   Get your free API key from: https://api.together.xyz/settings/api-keys")
            print()
            sys.exit(1)
        
        try:
            self.client = Together(api_key=api_key)
            # Note: Skipping model list test to avoid validation errors
            safe_print("[OK] Connected to Together.ai successfully!")
        except Exception as e:
            safe_print(f"[ERROR] Failed to initialize Together.ai client")
            print(f"   Details: {e}")
            print("   Please check your API key and internet connection.")
            sys.exit(1)
        
        # Model configuration
        # Using the most stable and reliable model
        self.model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
        # Alternative models (uncomment to try):
        # self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"  # Larger model
        # self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"        # Largest (may require special access)

    def load_api_key(self):
        """Load API key from environment variable or .env file"""
        # First try environment variable
        api_key = os.getenv('TOGETHER_API_KEY')
        if api_key:
            return api_key
        
        # Try to load from .env file
        if os.path.exists('.env'):
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
                            return api_key
            except Exception as e:
                print(f"Warning: Could not read .env file: {e}")
        
        # Return None if nothing found (not placeholder)
        return None

    def enter_prompt(self, message):
        self.display_response(message)

    def display_response(self, message):
        try:
            # Show thinking animation
            thinking_text = "Thinking..."
            for i, char in enumerate(thinking_text):
                print(char, end="", flush=True)
                time.sleep(0.1)  # Faster thinking animation
            
            # Make API call
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            # Clear the "Thinking..." text once we get the first response
            print("\b" * len(thinking_text), end="", flush=True)  # Move cursor back
            print(" " * len(thinking_text), end="", flush=True)   # Overwrite with spaces
            print("\b" * len(thinking_text), end="", flush=True)  # Move cursor back again
            print("Chatbot: ", end="", flush=True)
            
            # Stream response with typing effect
            for chunk in stream:
                if (chunk.choices and 
                    len(chunk.choices) > 0 and 
                    chunk.choices[0].delta and 
                    chunk.choices[0].delta.content):
                    
                    content = chunk.choices[0].delta.content
                    # Add typing effect by printing each character with a small delay
                    for char in content:
                        try:
                            print(char, end="", flush=True)
                        except (UnicodeEncodeError, UnicodeError):
                            # Handle specific Unicode characters gracefully
                            if char in ['—', '–']:  # Em dash, en dash
                                print('-', end="", flush=True)
                            elif char in ['"', '"']:  # Smart quotes
                                print('"', end="", flush=True)
                            elif char in [''', ''']:  # Smart apostrophes
                                print("'", end="", flush=True)
                            elif char == '…':  # Ellipsis
                                print('...', end="", flush=True)
                            # Handle emojis that might be blocked
                            elif ord(char) > 127:  # Non-ASCII character
                                # Check if it's a common emoji and replace
                                emoji_map = {
                                    '🤖': '[robot]', '😊': ':)', '😢': ':(', '👍': '[thumbs-up]',
                                    '❤️': '[heart]', '🎉': '[party]', '🔥': '[fire]', '⭐': '[star]',
                                    '✨': '[sparkles]', '💡': '[idea]', '🚀': '[rocket]', '🌟': '[star]'
                                }
                                replacement = emoji_map.get(char, '[emoji]')
                                print(replacement, end="", flush=True)
                            else:
                                # Skip other problematic characters
                                pass
                        time.sleep(0.01)  # Faster typing effect
            
            print()  # Add a newline at the end
            
        except KeyboardInterrupt:
            safe_print("\n\n[STOP] Response cancelled by user")
        except Exception as e:
            safe_print(f"\n[ERROR] Error generating response: {e}")
            print("   Please check your internet connection and API key.")


def configure_windows_console():
    """Configure Windows console for Unicode support (without admin privileges)"""
    if not sys.platform.startswith('win'):
        return True
    
    try:
        # Method 1: Try to reconfigure stdout without system commands
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        
        # Method 2: Set environment for current process only
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        return True
        
    except Exception:
        return False

def test_unicode_support():
    """Test if the console can display Unicode characters properly"""
    try:
        # Test with progressively complex Unicode characters
        
        # Test 1: Basic emoji
        test_char = "🤖"
        print(test_char, end="")
        print("\b \b", end="")  # Clear it
        
        # Test 2: Braille characters (used in ASCII art)
        test_char = "⠀"
        print(test_char, end="")
        print("\b \b", end="")  # Clear it
        
        # If we get here, full Unicode support is available
        return True
        
    except (UnicodeEncodeError, UnicodeError):
        return False

def test_emoji_support():
    """Specifically test emoji support (separate from basic Unicode)"""
    try:
        # Test a simple emoji
        test_emoji = "🤖"
        
        # Try to print and immediately capture if it works
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            print(test_emoji, end="")
        
        # If no exception, emojis should work
        return True
        
    except (UnicodeEncodeError, UnicodeError, Exception):
        return False

def print_robot():
    """Print robot ASCII art with intelligent fallback for Windows security restrictions"""
    # Configure console (non-privileged methods only)
    configure_windows_console()
    
    # Test Unicode and emoji support separately
    unicode_supported = test_unicode_support()
    emoji_supported = test_emoji_support() if unicode_supported else False
    
    # Decision tree based on capabilities
    if emoji_supported:
        # Full emoji + Unicode support
        try:
            print("""
    🤖 AI CHATBOT POWERED BY TOGETHER.AI 🤖
               by Muhammad Affan
    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⡏⠉⠉⣉⠭⢍⠉⠉⡩⠽⢍⠉⠉⠉⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢰⠈⡇⠀⠀⣿⣷⡄⡇⠸⣿⣷⠀⠇⠀⠀⡇⢳⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢸⣴⠓⠢⡀⠈⠛⠊⠀⠀⠈⠛⠈⠀⡠⠒⢳⢸⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠈⢹⠀⠀⠈⠂⠀⠒⠒⠒⠀⠀⠐⠋⠀⠀⢸⠁⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠸⠤⣤⡤⠤⢤⣤⣤⣤⣤⣤⠤⢤⣤⠤⠼⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢠⠎⢡⣛⣶⣾⣷⣿⣶⣶⣾⣶⣛⠊⠑⡄⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⡸⣄⢸⡇⠀⣷⠀⠀⠀⢰⠀⠀⢸⡄⢀⢧⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣜⠀⢨⢻⡧⠴⠘⠷⣀⠴⠏⡿⠦⢼⠿⠅⠀⣡⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⡰⣁⡹⠃⢸⣇⠀⠀⠀⠋⠀⠀⠁⠀⢠⡄⠈⢯⣈⠧⡀⠀⠀⠀
    ⠀⣠⠶⢎⠀⢨⠇⠀⢸⢬⠛⣽⣿⣿⣿⣿⣟⣽⢫⡄⠀⠀⡇⠀⢸⠢⢄⠀
    ⡔⢁⠤⡀⢹⠁⠀⠀⠸⣬⠯⠬⠿⣭⠭⡭⠭⠬⠭⡅⠀⠀⠈⡏⠁⡠⡄⢡
    ⠳⢁⠜⣠⠏⠀⠀⠀⠀⡱⠤⠤⠤⢞⣈⠧⠤⠤⠴⡃⠀⠀⠀⠑⢄⠱⡈⠚
    ⠀⠈⠉⠁⠀⠀⠀⠀⠀⢹⠒⠒⠒⢪⢠⡗⠒⠒⠒⡅⠀⠀⠀⠀⠀⠉⠁⠀
    ⠀⠀⠀⠀⠀⠀⠀⢀⠠⠜⠛⠻⠭⣵⢰⡯⠭⠛⠛⠢⢄⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠰⠁⠀⠀⠀⠀⠀⢸⢼⠀⠀⠀⠀⠀⠀⠑⡄⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀
    
    Welcome to your AI Assistant!
    Type 'exit' to quit the conversation.
    """)
            return
        except:
            emoji_supported = False
    
    if unicode_supported and not emoji_supported:
        # Unicode support but emojis blocked (Windows security context)
        print("""
    [AI] CHATBOT POWERED BY TOGETHER.AI [AI]
               by Muhammad Affan
    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⡏⠉⠉⣉⠭⢍⠉⠉⡩⠽⢍⠉⠉⠉⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢰⠈⡇⠀⠀⣿⣷⡄⡇⠸⣿⣷⠀⠇⠀⠀⡇⢳⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢸⣴⠓⠢⡀⠈⠛⠊⠀⠀⠈⠛⠈⠀⡠⠒⢳⢸⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠈⢹⠀⠀⠈⠂⠀⠒⠒⠒⠀⠀⠐⠋⠀⠀⢸⠁⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠸⠤⣤⡤⠤⢤⣤⣤⣤⣤⣤⠤⢤⣤⠤⠼⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢠⠎⢡⣛⣶⣾⣷⣿⣶⣶⣾⣶⣛⠊⠑⡄⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⡸⣄⢸⡇⠀⣷⠀⠀⠀⢰⠀⠀⢸⡄⢀⢧⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣜⠀⢨⢻⡧⠴⠘⠷⣀⠴⠏⡿⠦⢼⠿⠅⠀⣡⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⡰⣁⡹⠃⢸⣇⠀⠀⠀⠋⠀⠀⠁⠀⢠⡄⠈⢯⣈⠧⡀⠀⠀⠀
    ⠀⣠⠶⢎⠀⢨⠇⠀⢸⢬⠛⣽⣿⣿⣿⣿⣟⣽⢫⡄⠀⠀⡇⠀⢸⠢⢄⠀
    ⡔⢁⠤⡀⢹⠁⠀⠀⠸⣬⠯⠬⠿⣭⠭⡭⠭⠬⠭⡅⠀⠀⠈⡏⠁⡠⡄⢡
    ⠳⢁⠜⣠⠏⠀⠀⠀⠀⡱⠤⠤⠤⢞⣈⠧⠤⠤⠴⡃⠀⠀⠀⠑⢄⠱⡈⠚
    ⠀⠈⠉⠁⠀⠀⠀⠀⠀⢹⠒⠒⠒⢪⢠⡗⠒⠒⠒⡅⠀⠀⠀⠀⠀⠉⠁⠀
    ⠀⠀⠀⠀⠀⠀⠀⢀⠠⠜⠛⠻⠭⣵⢰⡯⠭⠛⠛⠢⢄⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠰⠁⠀⠀⠀⠀⠀⢸⢼⠀⠀⠀⠀⠀⠀⠑⡄⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀
    
    Welcome to your AI Assistant!
    Type 'exit' to quit the conversation.
    
    Note: Beautiful Unicode art displayed! (Emojis disabled by Windows security)
    """)
    else:
        # Full ASCII fallback
        print("""
    *** AI CHATBOT POWERED BY TOGETHER.AI ***
                by Muhammad Affan
    
                 .---.
                /     \\
               | () () |
                \\  ^  /
                 |||||
               ___|___
              |       |
              | ROBOT |
              |   AI  |
              |_______|
               |  |  |
               |  |  |
              === ===
         
    Welcome to your AI Assistant!
    Type 'exit' to quit the conversation.
    
    Note: Using ASCII graphics for maximum compatibility.
    The chatbot will work perfectly!
    """)

def safe_print(text):
    """Print text with smart Unicode/emoji handling for Windows security contexts"""
    try:
        # First try normal printing
        print(text)
    except (UnicodeEncodeError, UnicodeError):
        # If that fails, use fallback
        print_with_fallback(text)

def print_with_fallback(text):
    """Print text with emoji/Unicode fallback"""
    # Replace emojis with text equivalents
    fallback_text = text.replace('🤖', '[AI]')
    fallback_text = fallback_text.replace('✅', '[OK]')
    fallback_text = fallback_text.replace('❌', '[ERROR]')
    fallback_text = fallback_text.replace('⚠️', '[WARNING]')
    fallback_text = fallback_text.replace('💡', '[TIP]')
    fallback_text = fallback_text.replace('🚀', '[GO]')
    fallback_text = fallback_text.replace('👋', '[WAVE]')
    fallback_text = fallback_text.replace('⏹️', '[STOP]')
    fallback_text = fallback_text.replace('🔑', '[KEY]')
    fallback_text = fallback_text.replace('📦', '[PACKAGE]')
    fallback_text = fallback_text.replace('🎉', '[PARTY]')
    fallback_text = fallback_text.replace('💻', '[COMPUTER]')
    fallback_text = fallback_text.replace('🌍', '[WORLD]')
    fallback_text = fallback_text.replace('🎨', '[ART]')
    
    try:
        print(fallback_text)
    except (UnicodeEncodeError, UnicodeError):
        # Last resort: ASCII only
        ascii_text = ''.join(char if ord(char) < 128 else '?' for char in fallback_text)
        print(ascii_text)

# Global flag to detect emoji support
_emoji_support_detected = None

def detect_emoji_support():
    """Detect and cache emoji support status"""
    global _emoji_support_detected
    
    if _emoji_support_detected is not None:
        return _emoji_support_detected
    
    _emoji_support_detected = test_emoji_support()
    return _emoji_support_detected


if __name__ == "__main__":
    try:
        print_robot()
        chat = Chatbot()
        
        safe_print("[TIP] Tips:")
        print("   • Type your questions naturally")
        print("   • Press Ctrl+C during response to cancel")
        print("   • Type 'exit' to quit")
        safe_print("   • Enjoy chatting with AI! [GO]")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    print("Please enter a message.")
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    safe_print("[AI] Thanks for chatting! Goodbye! [WAVE]")
                    break
                    
                chat.enter_prompt(user_input)
                
            except KeyboardInterrupt:
                safe_print("\n\n[AI] Thanks for chatting! Goodbye! [WAVE]")
                break
            except EOFError:
                safe_print("\n\n[AI] Thanks for chatting! Goodbye! [WAVE]")
                break
                
    except Exception as e:
        safe_print(f"\n[ERROR] Fatal error: {e}")
        print("The application will now exit.")
        sys.exit(1)
