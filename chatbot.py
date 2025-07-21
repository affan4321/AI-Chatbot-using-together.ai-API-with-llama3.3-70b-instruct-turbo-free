from together import Together
from dotenv import load_dotenv
import time

load_dotenv()

class Chatbot:
    def __init__(self):
        self.client = Together()
        # Faster alternative models (uncomment to try):
        # self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"  # Smaller, faster
        # self.model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"          # Even faster
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"      # Current (largest)

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
            thinkText = "Thinking..."
            for i in range(11):
                print(thinkText[i], end="", flush=True)
                time.sleep(0.2)


            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            # Clear the "Thinking..." text once we get the first response
            print("\b" * 11, end="", flush=True)  # Clear "Thinking..."
            print(" " * 11, end="", flush=True)   # Overwrite with spaces
            print("\b" * 11, end="", flush=True)  # Move cursor back
            print("Chatbot: ", end="", flush=True)
            
            for chunk in stream:
                if (chunk.choices and 
                    len(chunk.choices) > 0 and 
                    chunk.choices[0].delta and 
                    chunk.choices[0].delta.content):
                    
                    content = chunk.choices[0].delta.content
                    # Add typing effect by printing each character with a small delay
                    for char in content:
                        print(char, end="", flush=True)
                        time.sleep(0.02)  # Adjust this value to control typing speed
            
            print()  # Add a newline at the end
            
        except Exception as e:
            print(f"\nStreaming error: {e}")



if __name__ == "__main__":
    chat = Chatbot()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        chat.enter_prompt(user_input)
