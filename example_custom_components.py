"""
Example of using custom models and views with the Factory pattern

This file demonstrates how to extend the application with custom components
using the factory pattern, making it easy to swap implementations.
"""

from factory import app_factory, BaseModel, BaseView
import streamlit as st

# Example custom model
class CustomHTMLGenerator(BaseModel):
    """Custom HTML generator with different personality"""
    
    def __init__(self):
        self.personality = "Custom Generator"
    
    def generate_html(self, prompt):
        """Generate custom HTML response"""
        return f"<html><body><h1>Custom: {prompt}</h1></body></html>", None

# Example custom view
class CustomChatView(BaseView):
    """Custom chat view with different styling"""
    
    def display_header(self):
        st.markdown('<div style="color: blue; font-size: 24px;">Custom Chat Interface</div>', 
                   unsafe_allow_html=True)
    
    def display_chat(self, messages):
        for message in messages:
            st.write(f"[{message.role}]: {message.content}")

# Example of how to register and use custom components
def setup_custom_components():
    """Register custom components with the factory"""
    
    # Register custom model
    app_factory.register_custom_model("CustomHTMLGenerator", CustomHTMLGenerator)
    
    # Register custom view
    app_factory.register_custom_view("CustomChatView", CustomChatView)
    
    print("Custom components registered successfully!")
    print(f"Available models: {app_factory.get_available_models()}")
    print(f"Available views: {app_factory.get_available_views()}")

def demonstrate_custom_usage():
    """Demonstrate how to use custom components"""
    
    # Create custom model instance
    custom_generator = app_factory.create_model("CustomHTMLGenerator")
    html_content, error = custom_generator.generate_html("Hello World")
    print(f"Custom generator output: {html_content}")
    
    # Create custom view instance
    custom_chat_view = app_factory.create_view("CustomChatView")
    print(f"Custom chat view created: {type(custom_chat_view)}")

if __name__ == "__main__":
    # Setup custom components
    setup_custom_components()
    
    # Demonstrate usage
    demonstrate_custom_usage()
