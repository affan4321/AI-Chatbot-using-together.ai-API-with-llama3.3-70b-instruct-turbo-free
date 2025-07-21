from together import Together
import time
import os
import sys
import locale
import codecs

class Chatbot:
    def __init__(self):
        # API Key Configuration
        # For development: Load from environment or .env file
        # For distribution: Will be replaced with embedded key during build
        api_key = self.load_api_key()
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            safe_print("⚠️  Warning: No valid API key found!")
            safe_print("   For development: Set TOGETHER_API_KEY environment variable or add to .env file")
            safe_print("   For distribution: API key will be embedded during build process")
            safe_print("   Get your free API key from: https://api.together.xyz/settings/api-keys")
            print()
            sys.exit(1)
        
        try:
            self.client = Together(api_key=api_key)
            # Note: Skipping model list test to avoid validation errors
            safe_print("✅ Connected to Together.ai successfully!")
        except Exception as e:
            safe_print(f"❌ Error: Failed to initialize Together.ai client")
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
        
        # Return placeholder if nothing found
        return 'YOUR_API_KEY_HERE'

    def get_response(self, message):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

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
                        except UnicodeEncodeError:
                            # Replace problematic Unicode with safe alternatives
                            if ord(char) > 127:  # Non-ASCII character
                                print('?', end="", flush=True)
                            else:
                                print(char, end="", flush=True)
                        time.sleep(0.01)  # Faster typing effect
            
            print()  # Add a newline at the end
            
        except KeyboardInterrupt:
            safe_print("\n\n⏹️  Response cancelled by user")
        except Exception as e:
            safe_print(f"\n❌ Error generating response: {e}")
            print("   Please check your internet connection and API key.")


def configure_console_encoding():
    """Configure console to support UTF-8 and emojis"""
    try:
        # Try to set UTF-8 encoding for Windows console
        if sys.platform.startswith('win'):
            # Enable UTF-8 support in Windows console
            os.system('chcp 65001 >nul 2>&1')
            
            # Set stdout encoding to UTF-8
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8')
            elif hasattr(sys.stdout, 'buffer'):
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
                
        return True
    except Exception:
        return False

def print_robot():
    """Print robot ASCII art with fallback for incompatible terminals"""
    # Try to configure UTF-8 encoding
    utf8_supported = configure_console_encoding()
    
    try:
        if utf8_supported:
            # Full Unicode version with emojis
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
        else:
            raise Exception("UTF-8 not supported")
            
    except Exception:
        # Fallback ASCII version for older/incompatible terminals
        print("""
    *** AI CHATBOT POWERED BY TOGETHER.AI ***
                by Muhammad Affan
    
           .---.
          /     \\
         | () () |
          \\  ^  /
           |||||
           |||||
           
        .-""""""-.
       /          \\
      |   Robot    |
      |  Assistant |
       \\          /
        '-.......-'
         
    Welcome to your AI Assistant!
    Type 'exit' to quit the conversation.
    """)

def safe_print(text, emoji_fallback=True):
    """Print text with emoji fallback for incompatible terminals"""
    try:
        print(text)
    except UnicodeEncodeError:
        if emoji_fallback:
            # Replace common emojis with text equivalents
            fallback_text = text.replace('🤖', '[AI]')
            fallback_text = fallback_text.replace('✅', '[OK]')
            fallback_text = fallback_text.replace('❌', '[ERROR]')
            fallback_text = fallback_text.replace('⚠️', '[WARNING]')
            fallback_text = fallback_text.replace('💡', '[TIP]')
            fallback_text = fallback_text.replace('🚀', '[GO]')
            fallback_text = fallback_text.replace('👋', '[WAVE]')
            fallback_text = fallback_text.replace('⏹️', '[STOP]')
            print(fallback_text)
        else:
            print(text.encode('ascii', 'replace').decode('ascii'))


if __name__ == "__main__":
    try:
        print_robot()
        chat = Chatbot()
        
        safe_print("💡 Tips:")
        print("   • Type your questions naturally")
        print("   • Press Ctrl+C during response to cancel")
        print("   • Type 'exit' to quit")
        safe_print("   • Enjoy chatting with AI! 🚀")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    print("Please enter a message.")
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    safe_print("🤖 Thanks for chatting! Goodbye! 👋")
                    break
                    
                chat.enter_prompt(user_input)
                
            except KeyboardInterrupt:
                safe_print("\n\n🤖 Thanks for chatting! Goodbye! 👋")
                break
            except EOFError:
                safe_print("\n\n🤖 Thanks for chatting! Goodbye! 👋")
                break
                
    except Exception as e:
        safe_print(f"\n❌ Fatal error: {e}")
        print("The application will now exit.")
        sys.exit(1)
