import streamlit as st
from factory import app_factory

class AppController:
    """Main controller that coordinates the application"""
    
    def __init__(self):
        self.session = app_factory.create_model("ChatSession")
        self.html_generator = app_factory.create_model("HTMLGenerator")
        self.file_manager = app_factory.create_model("FileManager")
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
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
        
        if 'show_published' not in st.session_state:
            st.session_state.show_published = False
    
    def _sync_session_state(self):
        """Sync controller state with Streamlit session state"""
        # Update session state with controller state
        st.session_state.messages = [msg.to_dict() for msg in self.session.messages]
        st.session_state.current_personality = self.session.current_personality
        st.session_state.generated_html = self.session.generated_html
        st.session_state.html_file_path = self.session.html_file_path
        st.session_state.show_results = self.session.show_results
        st.session_state.current_html = self.session.current_html
        st.session_state.show_published = self.session.show_published
    
    def _load_from_session_state(self):
        """Load controller state from Streamlit session state"""
        # Convert dict messages back to Message objects
        self.session.messages = []
        for msg_dict in st.session_state.messages:
            message = app_factory.create_model(
                "Message",
                role=msg_dict["role"],
                content=msg_dict["content"],
                personality=msg_dict.get("personality"),
                html_content=msg_dict.get("html_content")
            )
            self.session.messages.append(message)
        
        self.session.current_personality = st.session_state.current_personality
        self.session.generated_html = st.session_state.generated_html
        self.session.html_file_path = st.session_state.html_file_path
        self.session.show_results = st.session_state.show_results
        self.session.current_html = st.session_state.current_html
        self.session.show_published = st.session_state.show_published
    
    def add_message(self, role, content, personality=None, html_content=None):
        """Add a message to the chat history"""
        message = app_factory.create_model("Message", role, content, personality, html_content)
        self.session.add_message(message)
        
        # If HTML content is provided, open it in browser
        if html_content:
            try:
                file_path, error = self.file_manager.save_and_open_html(html_content, content)
                if file_path:
                    st.success("🌐 Generated website opened in new browser tab!")
                else:
                    st.warning(f"⚠️ Could not open browser: {error}")
            except Exception as e:
                st.warning(f"⚠️ Could not open browser: {str(e)}")
        
        self._sync_session_state()
    
    def generate_html(self, prompt):
        """Generate HTML using the AI model"""
        try:
            html_content, error = self.html_generator.generate_html(prompt, self.session.current_personality)
            
            if html_content:
                self.session.current_html = html_content
                self.session.show_results = True
                return html_content, None
            else:
                return None, error
                
        except Exception as e:
            return None, f"Error generating HTML: {str(e)}"
    
    def update_website(self, prompt):
        """Update existing website with new prompt"""
        try:
            html_content, error = self.html_generator.generate_html(prompt, self.session.current_personality)
            
            if html_content:
                self.session.current_html = html_content
                return html_content, None
            else:
                return None, error
                
        except Exception as e:
            return None, f"Error updating HTML: {str(e)}"
    
    def publish_website(self):
        """Publish the current website"""
        self.session.show_published = True
        self._sync_session_state()
    
    def go_back_to_editor(self):
        """Go back to editor from published view"""
        self.session.show_published = False
        self._sync_session_state()
    
    def go_back_to_chat(self):
        """Go back to chat from results view"""
        self.session.show_results = False
        self._sync_session_state()
    
    def get_download_filename(self):
        """Get filename for download"""
        return self.file_manager.get_download_filename()
    
    def run(self):
        """Main application loop"""
        # Load state from session
        self._load_from_session_state()
        
        # Apply CSS styles
        css_styles = app_factory.create_view("CSSStyles")
        st.markdown(css_styles.get_main_styles(), unsafe_allow_html=True)
        
        # Page configuration
        st.set_page_config(
            page_title="Build something lovable",
            page_icon="💕",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Main application flow
        if self.session.show_published:
            self._show_published_page()
        elif self.session.show_results:
            self._show_results_page()
        else:
            self._show_chat_page()
        
        # Footer
        footer_view = app_factory.create_view("FooterView")
        footer_view.display_footer()
    
    def _show_chat_page(self):
        """Display the main chat page"""
        chat_view = app_factory.create_view("ChatView")
        chat_view.display_header()
        chat_view.display_chat(self.session.messages)
        
        user_input, submit_button = chat_view.display_chat_input()
        
        if submit_button and user_input:
            # Add user message
            self.add_message("user", user_input)
            
            # Generate HTML with AI
            with st.spinner("🤖 Generating your website..."):
                html_content, error = self.generate_html(user_input)
                
                if html_content:
                    response = f"✅ Website generated successfully!"
                    self.add_message("assistant", response, self.session.current_personality, html_content)
                    st.rerun()
                else:
                    response = f"❌ Sorry, I couldn't generate the website. Error: {error}"
                    self.add_message("assistant", response, self.session.current_personality)
                    st.rerun()
    
    def _show_results_page(self):
        """Display the results page"""
        # Apply results-specific styles
        css_styles = app_factory.create_view("CSSStyles")
        st.markdown(css_styles.get_results_styles(), unsafe_allow_html=True)
        
        # Back button
        results_view = app_factory.create_view("ResultsView")
        if results_view.display_back_button():
            self.go_back_to_chat()
            st.rerun()
        
        results_view.display_results_header()
        
        # Two column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Chat column
            results_view.display_chat_column(
                self.session.messages,
                self._handle_continue_chat
            )
        
        with col2:
            # Results column
            results_view.display_results_column(
                self.session.current_html,
                self.publish_website,
                self.get_download_filename
            )
    
    def _show_published_page(self):
        """Display the published page"""
        # Apply published-specific styles
        css_styles = app_factory.create_view("CSSStyles")
        st.markdown(css_styles.get_published_styles(), unsafe_allow_html=True)
        
        # Back button
        published_view = app_factory.create_view("PublishedView")
        if published_view.display_back_button():
            self.go_back_to_editor()
            st.rerun()
        
        published_view.display_published_header()
        published_view.display_published_website(self.session.current_html)
    
    def _handle_continue_chat(self, user_input):
        """Handle continuing chat in results view"""
        self.add_message("user", user_input)
        
        # Generate updated HTML
        with st.spinner("🤖 Updating your website..."):
            html_content, error = self.update_website(user_input)
            
            if html_content:
                response = f"✅ Website updated successfully!"
                self.add_message("assistant", response, self.session.current_personality, html_content)
                st.rerun()
            else:
                response = f"❌ Sorry, I couldn't update the website. Error: {error}"
                self.add_message("assistant", response, self.session.current_personality)
                st.rerun()
