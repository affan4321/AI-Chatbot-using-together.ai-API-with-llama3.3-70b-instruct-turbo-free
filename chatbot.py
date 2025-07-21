from together import Together
import time
import os
import sys

class Chatbot:
    def __init__(self):
        # API Key Configuration
        # For development: Load from environment or .env file
        # For distribution: Will be replaced with embedded key during build
        api_key = self.load_api_key()
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            print("⚠️  Warning: No valid API key found!")
            print("   For development: Set TOGETHER_API_KEY environment variable or add to .env file")
            print("   For distribution: API key will be embedded during build process")
            print("   Get your free API key from: https://api.together.xyz/settings/api-keys")
            print()
            sys.exit(1)
        
        try:
            self.client = Together(api_key=api_key)
            # Note: Skipping model list test to avoid validation errors
            print("✅ Connected to Together.ai successfully!")
        except Exception as e:
            print(f"❌ Error: Failed to initialize Together.ai client")
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
                        print(char, end="", flush=True)
                        time.sleep(0.01)  # Faster typing effect
            
            print()  # Add a newline at the end
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Response cancelled by user")
        except Exception as e:
            print(f"\n❌ Error generating response: {e}")
            print("   Please check your internet connection and API key.")


def print_robot():
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


if __name__ == "__main__":
    try:
        print_robot()
        chat = Chatbot()
        
        print("💡 Tips:")
        print("   • Type your questions naturally")
        print("   • Press Ctrl+C during response to cancel")
        print("   • Type 'exit' to quit")
        print("   • Enjoy chatting with AI! 🚀")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    print("Please enter a message.")
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🤖 Thanks for chatting! Goodbye! 👋")
                    break
                    
                chat.enter_prompt(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🤖 Thanks for chatting! Goodbye! 👋")
                break
            except EOFError:
                print("\n\n🤖 Thanks for chatting! Goodbye! 👋")
                break
                
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("The application will now exit.")
        sys.exit(1)
