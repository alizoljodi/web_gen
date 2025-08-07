import streamlit as st
import streamlit.components.v1 as components
import time
import random
import os
import tempfile
import webbrowser
from datetime import datetime
import json
import groq

# Page configuration
st.set_page_config(
    page_title="AI HTML Generator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .message-time {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .html-preview {
        border: 2px solid #667eea;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .html-container {
        border: 2px solid #667eea;
        border-radius: 0.5rem;
        margin: 1rem 0;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_personality' not in st.session_state:
    st.session_state.current_personality = "HTML Generator"

if 'generated_html' not in st.session_state:
    st.session_state.generated_html = None

if 'html_file_path' not in st.session_state:
    st.session_state.html_file_path = None

# Initialize Groq client
def get_groq_client():
    """Initialize Groq client with API key"""
    api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
    if not api_key:
        st.error("❌ Groq API key not found. Please set it in Streamlit secrets or environment variables.")
        st.info("💡 Add your Groq API key to Streamlit Cloud secrets as: GROQ_API_KEY = 'your-api-key-here'")
        return None
    
    try:
        client = groq.Groq(api_key=api_key)
        # Test the client with a simple call
        st.success("✅ Groq API key is valid")
        return client
    except Exception as e:
        st.error(f"❌ Error initializing Groq client: {str(e)}")
        return None

# HTML generation personalities
PERSONALITIES = {
    "HTML Generator": {
        "description": "Generate complete HTML websites from prompts",
        "greeting": "Hello! I'm your HTML generator. Describe the website you want to create and I'll generate it for you! 🌐",
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
    },
    "Portfolio Creator": {
        "description": "Specialized in creating portfolio websites",
        "greeting": "Hi! I'm your portfolio specialist. Let me create stunning portfolio websites for you! 🎨",
        "system_prompt": """You are an expert portfolio website designer. Create beautiful, professional portfolio websites.
        Always include:
        - Hero section with name and title
        - About section
        - Skills/technologies section
        - Projects/portfolio section
        - Contact information
        - Smooth scrolling navigation
        - Professional color schemes
        - Modern animations and transitions
        - Responsive design for all devices
        - Professional typography
        - Call-to-action buttons"""
    },
    "Business Website": {
        "description": "Create professional business websites",
        "greeting": "Hello! I'm your business website expert. Let me create professional business websites for you! 💼",
        "system_prompt": """You are an expert business website designer. Create professional, conversion-focused business websites.
        Always include:
        - Hero section with value proposition
        - Services/products section
        - About the company
        - Contact information and forms
        - Call-to-action buttons
        - Professional branding
        - Trust indicators (testimonials, certifications)
        - Mobile-responsive design
        - Fast loading optimization
        - SEO-friendly structure"""
    },
    "Creative Designer": {
        "description": "Create artistic and creative websites",
        "greeting": "Hey! I'm your creative designer. Let's make some artistic and unique websites! ✨",
        "system_prompt": """You are a creative web designer specializing in artistic and unique websites.
        Always include:
        - Creative and artistic design elements
        - Unique color schemes and typography
        - Interactive animations and effects
        - Creative layouts and positioning
        - Artistic backgrounds and patterns
        - Smooth transitions and hover effects
        - Creative navigation
        - Visual storytelling elements
        - Modern CSS techniques (grid, flexbox, animations)
        - Unique visual elements and graphics"""
    }
}

def generate_html_with_groq(prompt, personality):
    """Generate HTML using Groq API"""
    client = get_groq_client()
    if not client:
        return None, "Failed to initialize Groq client"
    
    try:
        system_prompt = PERSONALITIES[personality]["system_prompt"]
        
        # Create the full prompt
        full_prompt = f"""
        {system_prompt}
        
        User Request: {prompt}
        
        Generate a complete, functional HTML page that matches this request. 
        Include all necessary CSS and JavaScript inline. 
        Make it beautiful, modern, and fully responsive.
        """
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
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
        
        # Return the raw response without any modifications
        return html_content, None
        
    except Exception as e:
        return None, f"Error generating HTML: {str(e)}"

def save_html_file(html_content, prompt):
    """Save HTML to file for download"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            file_path = f.name
        
        return file_path, None
    except Exception as e:
        return None, f"Error saving HTML: {str(e)}"

def add_message(role, content, personality=None, html_content=None):
    """Add a message to the chat history"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "personality": personality,
        "html_content": html_content
    })

def display_chat():
    """Display the chat messages"""
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div style="flex-grow: 1;">
                        <strong>You:</strong><br>
                        {message["content"]}
                        <div class="message-time">{message["timestamp"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                personality = message.get("personality", "Assistant")
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div style="flex-grow: 1;">
                        <strong>{personality}:</strong><br>
                        {message["content"]}
                        <div class="message-time">{message["timestamp"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show HTML preview if available
                if message.get("html_content"):
                    # Success message
                    st.markdown("""
                    <div class="success-message">
                        ✅ HTML generated successfully! View the website below.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display HTML in Streamlit with a simple container
                    st.markdown('<div class="html-container">', unsafe_allow_html=True)
                    try:
                        components.html(message["html_content"], height=600, scrolling=True)
                    except Exception as e:
                        st.error(f"Error rendering HTML: {str(e)}")
                        st.info("HTML content is available for download below.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download button
                    try:
                        st.download_button(
                            label="📥 Download HTML File",
                            data=message["html_content"],
                            file_name=f"generated_website_{message['timestamp'].replace(':', '-')}.html",
                            mime="text/html",
                            key=f"download_btn_{i}"
                        )
                    except Exception as e:
                        st.error(f"Error creating download button: {str(e)}")
                    
                    # Show HTML code in a simple text area
                    st.markdown("**📄 HTML Code:**")
                    st.code(message["html_content"], language="html")
                    
                    st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">🌐 HTML Generator</div>', unsafe_allow_html=True)
    
    # Personality selector
    selected_personality = st.selectbox(
        "Choose your AI personality:",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.current_personality),
        key="personality_selector"
    )
    
    if selected_personality != st.session_state.current_personality:
        st.session_state.current_personality = selected_personality
        # Add personality change message
        add_message("assistant", f"Switched to {selected_personality} mode! {PERSONALITIES[selected_personality]['greeting']}", selected_personality)
        st.rerun()
    
    st.markdown(f"**Current:** {selected_personality}")
    st.markdown(f"*{PERSONALITIES[selected_personality]['description']}*")
    
    st.markdown("---")
    
    # API Key Status
    groq_client = get_groq_client()
    if groq_client:
        st.success("✅ Groq API connected")
        
        # Test API button
        if st.button("🧪 Test Groq API", key="test_api"):
            try:
                with st.spinner("Testing Groq API..."):
                    test_response = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": "Say hello"}],
                        model="llama3-70b-8192",
                        max_tokens=50
                    )
                    test_result = test_response.choices[0].message.content
                    st.success(f"✅ API Test Successful! Response: {test_result}")
            except Exception as e:
                st.error(f"❌ API Test Failed: {str(e)}")
    else:
        st.error("❌ Groq API not configured")
        st.info("Add your Groq API key to Streamlit secrets or environment variables")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Export chat
    if st.button("📤 Export Chat", type="secondary", key="export_chat"):
        if st.session_state.messages:
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages
            }
            st.download_button(
                label="Download Chat",
                data=json.dumps(chat_data, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_chat"
            )
    
    st.markdown("---")
    
    # Chat statistics
    if st.session_state.messages:
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        html_generated = len([m for m in st.session_state.messages if m.get("html_content")])
        
        st.markdown("**📊 Chat Statistics:**")
        st.markdown(f"• Your messages: {user_messages}")
        st.markdown(f"• AI responses: {bot_messages}")
        st.markdown(f"• HTML pages generated: {html_generated}")
        st.markdown(f"• Total messages: {len(st.session_state.messages)}")

# Main chat interface
st.markdown('<div class="main-header">🌐 AI HTML Generator</div>', unsafe_allow_html=True)

# Welcome message if no messages yet
if not st.session_state.messages:
    add_message("assistant", PERSONALITIES[st.session_state.current_personality]["greeting"], st.session_state.current_personality)

# Display chat messages
display_chat()

# Chat input
with st.container():
    user_input = st.chat_input("Describe the website you want to create...", key="chat_input")
    
    if user_input:
        # Add user message
        add_message("user", user_input)
        
        # Generate HTML with Groq
        with st.spinner("🤖 Generating your website..."):
            html_content, error = generate_html_with_groq(user_input, st.session_state.current_personality)
            
            if html_content:
                response = f"✅ Your website has been generated successfully! You can view it below and download the HTML file."
                add_message("assistant", response, st.session_state.current_personality, html_content)
            else:
                response = f"❌ Sorry, I couldn't generate the website. Error: {error}"
                add_message("assistant", response, st.session_state.current_personality)
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        Made with ❤️ using Streamlit and Groq | AI HTML Generator v1.0
    </div>
    """,
    unsafe_allow_html=True
)
