import streamlit as st
import time
import random
from datetime import datetime
import json
import os
import tempfile
import webbrowser
import base64
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Lovable - Web Generator",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("groq_api", "your-groq-api-key-here"),
)

# Custom CSS for Lovable-inspired design
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        overflow: hidden;
        height: 100vh;
    }
    
    .gradient-bg {
        background: linear-gradient(135deg, #ff8c42 0%, #ff6b6b 25%, #a855f7 75%, #7c3aed 100%);
        height: 100vh;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .gradient-bg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/></filter></defs><rect width="100" height="100" filter="url(%23noise)" opacity="0.1"/></svg>');
        opacity: 0.1;
    }
    
    .main-content {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 1rem;
        box-sizing: border-box;
        max-height: 100vh;
        overflow: hidden;
        gap: 1rem;
    }
    
    .content-wrapper {
        position: relative;
        z-index: 1;
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .main-headline {
        font-size: 2.2rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.8rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .heart-icon {
        width: 20px;
        height: 20px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 10px;
    }
    
    .sub-headline {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1.5rem;
    }
    
    .chat-input-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 800px;
        width: 100%;
        margin-bottom: 1rem;
        position: relative;
        max-height: 60vh;
        overflow: hidden;
    }
    
    .chat-input {
        background: transparent;
        border: none;
        color: white;
        font-size: 1.1rem;
        width: 100%;
        outline: none;
        resize: none;
        padding-right: 60px;
        min-height: 120px;
        max-height: 70vh;
    }
    
    .chat-input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    .send-btn {
        background: linear-gradient(45deg, #ff6b6b, #a855f7);
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s;
        position: absolute;
        right: 0px;
        bottom: 50px;
        font-size: 1.1rem;
    }
    
    .send-btn:hover {
        transform: scale(1.1);
    }
    
    .processing-container {
        background: linear-gradient(135deg, #ff8c42 0%, #ff6b6b 25%, #a855f7 75%, #7c3aed 100%);
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        padding: 2rem;
    }
    
    .processing-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 600px;
        width: 100%;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-top: 3px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    .log-container {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 1rem;
        text-align: left;
        font-family: monospace;
        font-size: 0.8rem;
        max-height: 200px;
        overflow-y: auto;
        margin-top: 1rem;
    }
    
    .html-code-display {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #e5e7eb !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
        line-height: 1.4 !important;
    }
    
    .html-code-display textarea {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #e5e7eb !important;
        border: none !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @media (max-width: 768px) {
        .main-headline {
            font-size: 1.8rem;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .sub-headline {
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .chat-input-container {
            margin: 0.3rem;
            padding: 0.8rem;
            max-height: 50vh;
        }
        
        .send-btn {
            right: -0px;
            bottom: 30px;
            width: 40px;
            height: 40px;
            font-size: 1rem;
        }
        
        .main-content {
            padding: 0.8rem;
        }
    }
    
    @media (max-height: 600px) {
        .main-headline {
            font-size: 1.6rem;
            margin-bottom: 0.2rem;
        }
        
        .sub-headline {
            font-size: 0.8rem;
            margin-bottom: 0.8rem;
        }
        
        .chat-input-container {
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            max-height: 40vh;
        }
    }
    
    /* Hide Streamlit elements */
    .stApp {
        background: transparent !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #a855f7) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        color: white !important;
        font-size: 1.1rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.1) !important;
    }
    
    /* Custom text area styling */
    .stTextArea > div > div > textarea {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 1.1rem !important;
        resize: none !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""

def open_html_string_in_browser(html_string, filename_prefix="temp_html"):
    """Open HTML content in browser"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", prefix=filename_prefix, mode='w', encoding='utf-8') as tmp_file:
            tmp_file.write(html_string)
            tmp_path = tmp_file.name

        webbrowser.open_new_tab(f'file://{os.path.abspath(tmp_path)}')
        return True
    except Exception as e:
        st.error(f"Error opening browser: {e}")
        return False

def generate_html_with_groq(prompt):
    """Generate HTML content using Groq API"""
    try:
        # Create a comprehensive system prompt for HTML generation
        system_prompt = """You are an expert web developer and designer. Your task is to generate complete, functional HTML web pages based on user descriptions.
Requirements:
1. Generate complete HTML documents with proper DOCTYPE, head, and body tags
2. Include embedded CSS for modern, responsive design
3. Use beautiful gradients, modern typography, and smooth animations
4. Make the design fully responsive (mobile-first approach)
5. Include appropriate content sections based on the website type
6. Use semantic HTML with proper accessibility features
7. Include interactive elements like buttons, forms, and hover effects
8. Use a color scheme that matches the website type
9. Include features mentioned in the prompt (contact forms, pricing, gallery, etc.)
10. Make the design professional and modern
The HTML should be complete and ready to run in a browser. Include all necessary CSS inline and make it self-contained."""

        # Create the user prompt
        user_prompt = f"""Create a beautiful, modern, and responsive HTML web page based on this description: {prompt}
Generate a complete HTML document that includes:
- Modern responsive design with CSS Grid and Flexbox
- Beautiful gradients and animations
- Professional typography and spacing
- Interactive elements and hover effects
- Content that matches the website type
- Any specific features mentioned in the prompt
Make sure the HTML is complete and ready to run in a browser."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=4000,
            top_p=1,
            stream=False
        )
        
        # Extract the generated HTML content
        html_content = chat_completion.choices[0].message.content
        
        # Clean up the response
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
        
        # Ensure we have a complete HTML document
        if not html_content.strip().startswith("<!DOCTYPE html"):
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Web Page</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            color: white;
        }}
        
        .header h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .content {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        }}
        
        .btn {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
            margin: 10px;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }}
        
        .btn:hover {{
            background: #5a6fd8;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Generated Web Page</h1>
            <p>Created from your prompt: "{prompt}"</p>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer" style="text-align: center; color: white; margin-top: 2rem; opacity: 0.8;">
            <p>&copy; 2024 Generated Web Page. Created with ❤️ using AI.</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
        
    except Exception as e:
        st.error(f"Error calling Groq API: {e}")
        return None

def create_and_open_webpage(prompt):
    """Generate HTML from prompt using Groq API"""
    if not prompt or prompt.strip() == "":
        return "Please enter a prompt to generate a web page.", None
    
    # Generate HTML content using Groq API
    html_content = generate_html_with_groq(prompt)
    
    if html_content:
        # Open the HTML content in the default browser
        open_html_string_in_browser(html_content)
        return html_content, "success"
    else:
        return "Failed to generate webpage. Please check your API key and try again.", None

# Main app interface
def main():
    # Create the gradient background
    st.markdown("""
    <div class="gradient-bg">
        <div class="main-content">
            <div class="content-wrapper">
                <div class="main-headline">
                    Build something Lovable 💕
                </div>
                <div class="sub-headline">
                    Create apps and websites by chatting with AI
                </div>
                
                <div class="chat-input-container">
                    <form>
                        <textarea 
                            class="chat-input" 
                            placeholder="Ask Lovable to create a landing page..."
                            rows="3"
                            maxlength="1000"
                        ></textarea>
                        <button type="submit" class="send-btn">↑</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create the input form
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            prompt_input = st.text_area(
                label="",
                placeholder="Ask Lovable to create a landing page...",
                height=120,
                max_chars=1000,
                key="prompt_input"
            )
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            with col_btn2:
                generate_btn = st.button("↑", key="generate_btn")
    
    # Handle generation
    if generate_btn and prompt_input:
        st.session_state.current_page = "processing"
        st.session_state.prompt = prompt_input
        
        # Show processing page
        with st.container():
            st.markdown("""
            <div class="processing-container">
                <div class="processing-card">
                    <h2 style="margin-bottom: 1rem; font-size: 2rem;">🚀 The result</h2>
                    <div class="spinner"></div>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Thinking...</p>
                    <p style="font-size: 0.9rem; opacity: 0.8;">Generating your webpage with AI</p>
                    
                    <div class="log-container">
                        <div style="color: #4ade80;">✓ Initializing Groq client...</div>
                        <div style="color: #4ade80;">✓ Analyzing prompt...</div>
                        <div style="color: #fbbf24;">⏳ Calling Llama 3.1 70B model...</div>
                        <div style="color: #fbbf24;">⏳ Generating HTML content...</div>
                        <div style="color: #fbbf24;">⏳ Creating responsive design...</div>
                        <div style="color: #fbbf24;">⏳ Adding interactive elements...</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Process the generation
        with st.spinner("Generating webpage..."):
            html_content, status = create_and_open_webpage(prompt_input)
            
            if status == "success":
                st.session_state.generated_html = html_content
                st.session_state.current_page = "result"
                
                # Show success message
                st.success("🎉 Success! Your webpage has been generated and opened in a new tab!")
                
                # Show HTML code
                st.subheader("📄 Generated HTML Code")
                st.code(html_content, language="html")
                
                # Download button
                st.download_button(
                    label="📥 Download HTML File",
                    data=html_content,
                    file_name=f"generated_webpage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                
                # Back button
                if st.button("← Back to Home"):
                    st.session_state.current_page = "home"
                    st.rerun()
            else:
                st.error(html_content)
                if st.button("← Back to Home"):
                    st.session_state.current_page = "home"
                    st.rerun()

if __name__ == "__main__":
    main()
