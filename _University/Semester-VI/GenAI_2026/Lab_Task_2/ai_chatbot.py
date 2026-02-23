import google.genai as genai
from dotenv import load_dotenv
import os

class GeminiChatbot:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Gemini API Key Config
        api_key = os.getenv('GEN_AI_GEMINI_KEY')
        client = genai.Client(api_key=api_key)
        self.client = client
        self.model = 'gemini-2.5-flash'
    
    def chat(self, user_message):
        """Send a message and get a response from Gemini"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_message
        )
        return response.text
    
    def start_conversation(self):
        """Start an interactive chat session"""
        print("Gemini Chatbot started! Type 'exit' to quit.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            response = self.chat(user_input)
            print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    chatbot = GeminiChatbot()
    chatbot.start_conversation()