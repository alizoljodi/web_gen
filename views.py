import streamlit as st
import streamlit.components.v1 as components
from factory import BaseView

class CSSStyles(BaseView):
    """Contains all CSS styling for the application"""
    
    @staticmethod
    def get_main_styles():
        return """
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
            
            .publish-button {
                background-color: #dc3545 !important;
                color: white !important;
                border: none !important;
                border-radius: 0.5rem !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                transition: background 0.3s ease !important;
            }
            
            .publish-button:hover {
                background-color: #c82333 !important;
            }
        </style>
        """
    
    @staticmethod
    def get_published_styles():
        return """
        <style>
            .published-header {
                font-size: 2rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
                color: #333;
            }
            
            .published-container {
                background: white;
                border: 1px solid #ddd;
                border-radius: 0.5rem;
                padding: 1rem;
                height: 90vh;
                overflow: hidden;
            }
            
            .tab-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #ddd;
            }
            
            .back-button {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 0.5rem;
                padding: 0.5rem 1rem;
                font-weight: 500;
                cursor: pointer;
            }
            
            .back-button:hover {
                background: #5a6268;
            }
        </style>
        """
    
    @staticmethod
    def get_results_styles():
        return """
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
        """

class ChatView(BaseView):
    """Handles chat interface display"""
    
    @staticmethod
    def display_header():
        """Display the main header"""
        st.markdown('<div class="main-header">💕 Build something lovable</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Describe the website you want to create and I\'ll generate it for you!</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_chat(messages):
        """Display the chat messages"""
        for message in messages:
            with st.container():
                if message.role == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <div style="flex-grow: 1;">
                            <strong>You:</strong><br>
                            {message.content}
                            <div class="message-time">{message.timestamp}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    personality = message.personality or "Assistant"
                    st.markdown(f"""
                    <div class="message bot-message">
                        <div style="flex-grow: 1;">
                            <strong>{personality}:</strong><br>
                            {message.content}
                            <div class="message-time">{message.timestamp}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    @staticmethod
    def display_chat_input():
        """Display the chat input interface"""
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input("", placeholder="Describe the website you want to create...", key="chat_input", label_visibility="collapsed")

        with col2:
            submit_button = st.button("Generate", key="submit_button")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return user_input, submit_button

class ResultsView(BaseView):
    """Handles results page display"""
    
    @staticmethod
    def display_results_header():
        """Display the results page header"""
        st.markdown('<div class="results-header">🌐 Generated Website Results</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_back_button():
        """Display back button"""
        return st.button("← Back to Chat", key="back_button")
    
    @staticmethod
    def display_chat_column(messages, on_continue_chat):
        """Display the chat column in results view"""
        st.markdown("**💬 Continue Chat**")
        st.markdown("---")
        
        # Display chat messages
        ChatView.display_chat(messages)
        
        # Chat input for continuing conversation
        user_input = st.text_input("", placeholder="Ask for modifications or improvements...", key="continue_chat_input", label_visibility="collapsed")
        col_input1, col_input2 = st.columns([3, 1])
        
        with col_input2:
            continue_button = st.button("Send", key="continue_button")
        
        if continue_button and user_input:
            on_continue_chat(user_input)
        
        return user_input, continue_button
    
    @staticmethod
    def display_results_column(html_content, on_publish, on_download):
        """Display the results column in results view"""
        # Header with Publish button
        col_header1, col_header2 = st.columns([3, 1])
        
        with col_header1:
            st.markdown("**🌐 Generated Website**")
        
        with col_header2:
            publish_button = st.button("🚀 Publish", key="publish_button", help="Publish your website")
            if publish_button:
                on_publish()
        
        st.markdown("---")
        
        if html_content:
            # Display the generated HTML
            try:
                components.html(html_content, height=800, width=1000, scrolling=True)
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
                    data=html_content,
                    file_name=on_download(),
                    mime="text/html",
                    key="download_btn_results"
                )
            except Exception as e:
                st.error(f"Error creating download button: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No website generated yet. Start a conversation to see results here.")

class PublishedView(BaseView):
    """Handles published page display"""
    
    @staticmethod
    def display_published_header():
        """Display the published page header"""
        st.markdown('<div class="published-header">🚀 Published Website</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_back_button():
        """Display back button"""
        return st.button("← Back to Editor", key="back_to_editor")
    
    @staticmethod
    def display_published_website(html_content):
        """Display the published website"""
        if html_content:
            try:
                components.html(html_content, height=800, width=1400, scrolling=True)
            except Exception as e:
                st.error(f"Error rendering HTML: {str(e)}")
                st.info("HTML content is available for download below.")
        else:
            st.info("No website to display.")

class FooterView(BaseView):
    """Handles footer display"""
    
    @staticmethod
    def display_footer():
        """Display the footer"""
        st.markdown("""
        <div class="footer">
            This is a demo of the website builder.
        </div>
        """, unsafe_allow_html=True)
