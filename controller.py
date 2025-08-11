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
    
    def _validate_messages(self, messages, delays):
        """Validate and sanitize messages and delays to prevent errors"""
        if not messages or len(messages) == 0:
            # Return default messages if none provided
            messages = [("⏳ Processing...", "🔄 Working on your request...")]
            delays = [1.5]
            return messages, delays
        
        # Ensure all messages have the correct format (spinner_text, info_text)
        validated_messages = []
        for msg in messages:
            if isinstance(msg, tuple) and len(msg) >= 2:
                validated_messages.append(msg)
            else:
                # Skip malformed messages
                continue
        
        if not validated_messages:
            # If no valid messages, use defaults
            validated_messages = [("⏳ Processing...", "🔄 Working on your request...")]
            delays = [1.5]
        else:
            # Ensure delays list matches messages list
            if len(delays) != len(validated_messages):
                delays = [1.5] * len(validated_messages)
        
        return validated_messages, delays
    
    def _show_progressive_messages(self, placeholder, messages, delays=None):
        """Show progressive messages in a queue with custom delays"""
        # Validate and sanitize messages and delays
        messages, delays = self._validate_messages(messages, delays)
        
        total_steps = len(messages)
        
        for i, (spinner_text, info_text, delay) in enumerate(zip(messages, delays)):
            current_step = i + 1
            
            with placeholder.container():
                # Show queue status
                self._show_queue_status(current_step, total_steps, spinner_text.split("...")[0])
                
                with st.spinner(spinner_text):
                    # Extract the processing type from the spinner text
                    if "Processing" in spinner_text:
                        self._show_processing_message("analyzing", info_text.split(": ")[-1] if ": " in info_text else info_text)
                    elif "Generating" in spinner_text:
                        self._show_processing_message("generating", info_text.split(": ")[-1] if ": " in info_text else info_text)
                    elif "Updating" in spinner_text:
                        self._show_processing_message("updating", info_text.split(": ")[-1] if ": " in info_text else info_text)
                    elif "Publishing" in spinner_text:
                        self._show_processing_message("publishing", info_text.split(": ")[-1] if ": " in info_text else info_text)
                    else:
                        st.info(info_text)
                    
                    import time
                    time.sleep(delay)
    
    def _get_generation_messages(self):
        """Get messages for website generation process"""
        return [
            ("📝 Processing your request...", "🔄 Analyzing your website requirements...", 1.5),
            ("🤖 Generating your website...", "🎨 Creating beautiful HTML with modern design...", 2.0),
        ]
    
    def _get_update_messages(self):
        """Get messages for website update process"""
        return [
            ("📝 Processing your update request...", "🔄 Analyzing your website update requirements...", 1.5),
            ("🤖 Updating your website...", "🎨 Applying changes to your website...", 2.0),
        ]
    
    def _get_publishing_messages(self):
        """Get messages for website publishing process"""
        return [
            ("🚀 Publishing your website...", "📤 Preparing your website for publication..."),
            ("✅ Success!", "🌐 Your website is now live and ready!"),
        ]
    
    def _get_generation_messages_with_delays(self):
        """Get messages for website generation process with delays"""
        messages = [
            ("📝 Processing your request...", "🔄 Analyzing your website requirements..."),
            ("🤖 Generating your website...", "🎨 Creating beautiful HTML with modern design..."),
        ]
        delays = [1.5, 2.0]
        
        # Validate that messages and delays have the same length
        if len(messages) != len(delays):
            st.warning("⚠️ Message and delay count mismatch, using default delays")
            delays = [1.5] * len(messages)
        
        return messages, delays
    
    def _get_update_messages_with_delays(self):
        """Get messages for website update process with delays"""
        messages = [
            ("📝 Processing your update request...", "🔄 Analyzing your website update requirements..."),
            ("🤖 Updating your website...", "🎨 Applying changes to your website..."),
        ]
        delays = [1.5, 2.0]
        
        # Validate that messages and delays have the same length
        if len(messages) != len(delays):
            st.warning("⚠️ Message and delay count mismatch, using default delays")
            delays = [1.5] * len(messages)
        
        return messages, delays
    
    def _show_queue_status(self, current_step, total_steps, step_name):
        """Show queue status with progress indicator"""
        progress = current_step / total_steps
        st.progress(progress)
        st.caption(f"Step {current_step} of {total_steps}: {step_name}")
    
    def _show_processing_message(self, processing_type, message):
        """Show different types of processing messages with appropriate styling"""
        processing_styles = {
            "analyzing": ("🔍 Analyzing", "info"),
            "generating": ("🎨 Generating", "info"),
            "updating": ("🔄 Updating", "info"),
            "publishing": ("🚀 Publishing", "info"),
        }
        
        title, style = processing_styles.get(processing_type, ("⏳ Processing", "info"))
        
        if style == "info":
            st.info(f"{title}: {message}")
        else:
            st.info(f"{title}: {message}")
    
    def _show_success_message(self, success_type, message):
        """Show different types of success messages with appropriate styling"""
        success_styles = {
            "generation": ("🎉 Website Generated Successfully!", "success"),
            "update": ("🎉 Website Updated Successfully!", "success"),
            "publishing": ("🚀 Website Published!", "success"),
        }
        
        title, style = success_styles.get(success_type, ("✅ Success!", "success"))
        
        if style == "success":
            st.success(f"{title} {message}")
            st.balloons()
        else:
            st.success(f"{title} {message}")
    
    def _show_publishing_messages(self, placeholder):
        """Show publishing messages with appropriate delays"""
        publishing_messages = [
            ("🚀 Publishing your website...", "📤 Preparing your website for publication..."),
            ("✅ Success!", "🌐 Your website is now live and ready!"),
        ]
        publishing_delays = [1.0, 0.5]
        
        self._show_progressive_messages(placeholder, publishing_messages, publishing_delays)
    
    def _show_error_message(self, error_type, error_message):
        """Show different types of error messages with appropriate styling"""
        error_styles = {
            "generation": ("❌ Website Generation Failed", "error"),
            "update": ("❌ Website Update Failed", "error"),
            "api": ("⚠️ API Connection Issue", "warning"),
            "validation": ("⚠️ Input Validation Error", "warning"),
        }
        
        title, style = error_styles.get(error_type, ("❌ Error", "error"))
        
        if style == "error":
            st.error(f"{title}: {error_message}")
        elif style == "warning":
            st.warning(f"{title}: {error_message}")
        else:
            st.error(f"{title}: {error_message}")
    
    def _show_chat_page(self):
        """Display the main chat page"""
        chat_view = app_factory.create_view("ChatView")
        chat_view.display_header()
        chat_view.display_chat(self.session.messages)
        
        user_input, submit_button = chat_view.display_chat_input()
        
        if submit_button and user_input:
            # Add user message
            self.add_message("user", user_input)
            
            # Progressive message queue for different stages
            progress_placeholder = st.empty()
            
            # Define the message stages with delays
            generation_messages, generation_delays = self._get_generation_messages_with_delays()
            
            # Show progressive messages
            try:
                self._show_progressive_messages(progress_placeholder, generation_messages, generation_delays)
            except Exception as e:
                st.warning(f"⚠️ Progress display issue: {str(e)}")
                # Fallback to simple spinner
                with st.spinner("🤖 Generating your website..."):
                    import time
                    time.sleep(2.0)
            
            # Generate the HTML content
            html_content, error = self.generate_html(user_input)
            
            # Clear the progress messages
            progress_placeholder.empty()
            
            if html_content:
                # Stage 3: Publishing
                with st.spinner("🚀 Publishing your website..."):
                    self._show_success_message("generation", "Your website is ready!")
                    self.add_message("assistant", "✅ Website generated successfully!", self.session.current_personality, html_content)
                    
                    # Show publishing completion message
                    st.success("🎉 Your website is ready! Check the results tab to see it.")
                    st.rerun()
            else:
                self._show_error_message("generation", error)
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
        
        # Progressive message queue for updating website
        progress_placeholder = st.empty()
        
        # Define the update message stages with delays
        update_messages, update_delays = self._get_update_messages_with_delays()
        
        # Show progressive messages
        try:
            self._show_progressive_messages(progress_placeholder, update_messages, update_delays)
        except Exception as e:
            st.warning(f"⚠️ Progress display issue: {str(e)}")
            # Fallback to simple spinner
            with st.spinner("🤖 Updating your website..."):
                import time
                time.sleep(2.0)
        
        # Update the website
        html_content, error = self.update_website(user_input)
        
        # Clear the progress messages
        progress_placeholder.empty()
        
        if html_content:
            # Stage 3: Publishing updated website
            with st.spinner("🚀 Publishing updated website..."):
                self._show_success_message("update", "Your website has been updated!")
                self.add_message("assistant", "✅ Website updated successfully!", self.session.current_personality, html_content)
                
                # Show publishing completion message
                st.success("🎉 Your website has been updated! Check the results tab to see the changes.")
                st.rerun()
        else:
            self._show_error_message("update", error)
            response = f"❌ Sorry, I couldn't update the website. Error: {error}"
            self.add_message("assistant", response, self.session.current_personality)
            st.rerun()
