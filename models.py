import os
import tempfile
import webbrowser
from datetime import datetime
import groq
import streamlit as st

from factory import BaseModel

class Message(BaseModel):
    """Represents a chat message"""
    def __init__(self, role, content, personality=None, html_content=None):
        self.role = role
        self.content = content
        self.timestamp = datetime.now().strftime("%H:%M")
        self.personality = personality
        self.html_content = html_content
    
    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "personality": self.personality,
            "html_content": self.html_content
        }

class ChatSession(BaseModel):
    """Manages chat session state"""
    def __init__(self):
        self.messages = []
        self.current_personality = "HTML Generator"
        self.generated_html = None
        self.html_file_path = None
        self.show_results = False
        self.current_html = None
        self.show_published = False
    
    def add_message(self, message):
        """Add a message to the chat history"""
        self.messages.append(message)
    
    def get_messages(self):
        """Get all messages"""
        return self.messages
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages = []

class HTMLGenerator(BaseModel):
    """Handles HTML generation using Groq API"""
    
    PERSONALITIES = {
        "HTML Generator": {
            "description": "Generate complete HTML websites from prompts",
            "greeting": "Ask me anything about the website you want to create and I'll generate it for you!",
            "system_prompt": """You are an expert web developer and designer. Generate complete, functional HTML pages based on user prompts. 
            Always include:
            - Complete HTML structure with proper DOCTYPE
            - Modern CSS styling with gradients, animations, and responsive design
            - JavaScript for interactivity
            - Meta tags for SEO
            - Viewport settings for mobile responsiveness
            - Beautiful, modern design with professional styling
            - Interactive elements and smooth animations
            - Color schemes that match the theme
            - Fonts from Google Fonts
            - Icons from Font Awesome or similar
            
            Make the design modern, beautiful, and fully functional. Include all necessary CSS and JavaScript inline."""
        }
    }
    
    def __init__(self):
        self.client = None
    
    def get_groq_client(self):
        """Initialize Groq client with API key"""
        api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
        if not api_key:
            raise ValueError("Groq API key not found. Please set it in Streamlit secrets or environment variables.")
        
        try:
            self.client = groq.Groq(api_key=api_key)
            return self.client
        except Exception as e:
            raise Exception(f"Error initializing Groq client: {str(e)}")
    
    def generate_html(self, prompt, personality):
        """Generate HTML using Groq API"""
        if not self.client:
            self.get_groq_client()
        
        try:
            system_prompt = self.PERSONALITIES[personality]["system_prompt"]
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": f"Create a complete HTML website for: {prompt}"
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                max_tokens=4000
            )
            
            html_content = chat_completion.choices[0].message.content
            return html_content, None
            
        except Exception as e:
            return None, f"Error generating HTML: {str(e)}"

class FileManager(BaseModel):
    """Handles file operations"""
    
    @staticmethod
    def save_and_open_html(html_content, prompt):
        """Save HTML to file and open in browser"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                file_path = f.name
            
            # Open in browser
            webbrowser.open(f'file://{file_path}')
            
            return file_path, None
        except Exception as e:
            return None, f"Error saving/opening HTML: {str(e)}"
    
    @staticmethod
    def get_download_filename():
        """Generate filename for download"""
        return f"generated_website_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
