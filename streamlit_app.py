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
    page_title="Build something lovable",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: #333;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
        font-size: 1.1rem;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    
    .user-message {
        background-color: #f0f0f0;
        border-left: 4px solid #007bff;
    }
    
    .bot-message {
        background-color: #f8f9fa;
        border-left: 4px solid #28a745;
    }
    
    .message-time {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .chat-input-container {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stTextInput > div > div > input {
        border: none;
        outline: none;
        font-size: 1rem;
        padding: 0.5rem;
    }
    
    .stButton > button {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #0056b3;
    }
    
    .html-preview {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 4rem;
        padding: 1rem;
    }
    
    /* Hide sidebar */
    .css-1d391kg {
        display: none;
    }
    
    /* Center the main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
    }

    .download-section {
        margin-top: 1rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 0.5rem;
        width: 100%;
        box-sizing: border-box;
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

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'current_html' not in st.session_state:
    st.session_state.current_html = None

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
        return client
    except Exception as e:
        st.error(f"❌ Error initializing Groq client: {str(e)}")
        return None

# HTML generation personalities
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
    
    # If HTML content is provided, open it in browser
    if html_content:
        try:
            file_path, error = save_and_open_html(html_content, content)
            if file_path:
                st.success("🌐 Generated website opened in new browser tab!")
            else:
                st.warning(f"⚠️ Could not open browser: {error}")
        except Exception as e:
            st.warning(f"⚠️ Could not open browser: {str(e)}")

def display_chat():
    """Display the chat messages"""
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message user-message">
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
                <div class="message bot-message">
                    <div style="flex-grow: 1;">
                        <strong>{personality}:</strong><br>
                        {message["content"]}
                        <div class="message-time">{message["timestamp"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Main interface
if not st.session_state.show_results:
    # Initial page - ChatGPT style
    st.markdown('<div class="main-header">💕 Build something lovable</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Describe the website you want to create and I\'ll generate it for you!</div>', unsafe_allow_html=True)

    # Display chat messages
    display_chat()

    # Chat input at bottom
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input("", placeholder="Describe the website you want to create...", key="chat_input", label_visibility="collapsed")

    with col2:
        submit_button = st.button("Generate", key="submit_button")

    if submit_button and user_input:
        # Add user message
        add_message("user", user_input)
        
        # Generate HTML with Groq
        with st.spinner("🤖 Generating your website..."):
            html_content, error = generate_html_with_groq(user_input, st.session_state.current_personality)
            
            if html_content:
                st.session_state.current_html = html_content
                st.session_state.show_results = True
                st.rerun()
            else:
                response = f"❌ Sorry, I couldn't generate the website. Error: {error}"
                add_message("assistant", response, st.session_state.current_personality)
        
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Results page - Two column layout
    st.markdown("""
    <style>
        .results-header {
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            color: #333;
        }
        
        .chat-column {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            height: 80vh;
            overflow-y: auto;
        }
        
        .results-column {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            height: 80vh;
            overflow-y: auto;
        }
        
        .back-button {
            margin-bottom: 1rem;
        }
        
        .download-section {
            margin-top: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 0.5rem;
            width: 100%;
            box-sizing: border-box;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Chat", key="back_button"):
        st.session_state.show_results = False
        st.rerun()
    
    st.markdown('<div class="results-header">🌐 Generated Website Results</div>', unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        #st.markdown('<div class="chat-column">', unsafe_allow_html=True)
        st.markdown("**💬 Continue Chat**")
        st.markdown("---")
        
        # Display chat messages
        display_chat()
        
        # Chat input for continuing conversation
        user_input = st.text_input("", placeholder="Ask for modifications or improvements...", key="continue_chat_input", label_visibility="collapsed")
        col_input1, col_input2 = st.columns([3, 1])
        
        with col_input2:
            continue_button = st.button("Send", key="continue_button")
        
        if continue_button and user_input:
            add_message("user", user_input)
            
            # Generate updated HTML
            with st.spinner("🤖 Updating your website..."):
                html_content, error = generate_html_with_groq(user_input, st.session_state.current_personality)
                
                if html_content:
                    response = f"✅ Website updated successfully!"
                    add_message("assistant", response, st.session_state.current_personality, html_content)
                    st.session_state.current_html = html_content
                    st.rerun()
                else:
                    response = f"❌ Sorry, I couldn't update the website. Error: {error}"
                    add_message("assistant", response, st.session_state.current_personality)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        #st.markdown('<div class="results-column">', unsafe_allow_html=True)
        st.markdown("**🌐 Generated Website**")
        st.markdown("---")
        
        if st.session_state.current_html:
            # Display the generated HTML
            try:
                components.html(st.session_state.current_html, height=600, scrolling=True)
            except Exception as e:
                st.error(f"Error rendering HTML: {str(e)}")
                st.info("HTML content is available for download below.")
            
            # Download section
            st.markdown('<div class="download-section">', unsafe_allow_html=True)
            st.markdown("**📥 Download Options**")
            
            # Download button
            try:
                st.download_button(
                    label="📥 Download HTML File",
                    data=st.session_state.current_html,
                    file_name=f"generated_website_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    key="download_btn_results"
                )
            except Exception as e:
                st.error(f"Error creating download button: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No website generated yet. Start a conversation to see results here.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit and Groq | Build something lovable
</div>
""", unsafe_allow_html=True)
