import streamlit as st
import time
import random
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_personality' not in st.session_state:
    st.session_state.current_personality = "Friendly Assistant"

# Chatbot personalities
PERSONALITIES = {
    "Friendly Assistant": {
        "description": "A helpful and friendly AI assistant",
        "greeting": "Hello! I'm your friendly AI assistant. How can I help you today? 😊",
        "responses": [
            "That's interesting! Tell me more about that.",
            "I'd be happy to help you with that!",
            "That's a great question. Let me think about it...",
            "I understand what you're saying. What would you like to know?",
            "Thanks for sharing that with me!",
            "I'm here to help you with anything you need.",
            "That's a fascinating topic!",
            "I appreciate you asking that question."
        ]
    },
    "Tech Expert": {
        "description": "A knowledgeable tech enthusiast",
        "greeting": "Hey there! I'm your tech expert. Ready to dive into the latest in technology? 💻",
        "responses": [
            "From a technical perspective, that's quite interesting.",
            "Let me break down the technical aspects for you.",
            "In terms of technology, here's what you should know...",
            "That's a great technical question!",
            "The technology behind this is fascinating.",
            "Let me explain the technical details...",
            "This is a common challenge in tech.",
            "From an engineering standpoint..."
        ]
    },
    "Creative Writer": {
        "description": "An imaginative and creative AI",
        "greeting": "Hello! I'm your creative writing assistant. Let's craft something amazing together! ✨",
        "responses": [
            "That's a beautiful thought! Let me add some creative flair...",
            "What an inspiring idea! Here's how I see it...",
            "Let me paint a picture with words for you...",
            "That's the kind of creativity I love!",
            "Let's explore this idea together...",
            "Your imagination is wonderful!",
            "This reminds me of a story...",
            "Let me weave some magic into this..."
        ]
    },
    "Sage Advisor": {
        "description": "A wise and philosophical AI",
        "greeting": "Greetings, seeker of wisdom. I am here to share insights and guidance. 🧘‍♂️",
        "responses": [
            "That's a profound question that touches on deeper truths.",
            "Let me share some wisdom with you...",
            "This reminds me of an ancient saying...",
            "In the grand scheme of things...",
            "There's great wisdom in what you're asking.",
            "Let me offer you some thoughtful perspective...",
            "This is a question that has puzzled many throughout time.",
            "Consider this perspective..."
        ]
    }
}

def generate_response(user_input, personality):
    """Generate a response based on the selected personality"""
    responses = PERSONALITIES[personality]["responses"]
    
    # Simple response generation based on keywords
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
        return f"Hello! Nice to meet you! {random.choice(responses)}"
    
    elif any(word in user_input_lower for word in ["how are you", "how do you do"]):
        return f"I'm doing great, thank you for asking! {random.choice(responses)}"
    
    elif any(word in user_input_lower for word in ["name", "who are you"]):
        return f"I'm your {personality.lower()}. {random.choice(responses)}"
    
    elif any(word in user_input_lower for word in ["help", "assist"]):
        return f"I'm here to help you! {random.choice(responses)} What would you like to know?"
    
    elif any(word in user_input_lower for word in ["thank", "thanks"]):
        return f"You're very welcome! {random.choice(responses)}"
    
    elif any(word in user_input_lower for word in ["bye", "goodbye", "see you"]):
        return f"Goodbye! It was wonderful chatting with you. {random.choice(responses)}"
    
    else:
        # Generate contextual response
        if personality == "Tech Expert":
            return f"That's an interesting topic! From a technical perspective, {random.choice(responses)}"
        elif personality == "Creative Writer":
            return f"What an inspiring thought! {random.choice(responses)}"
        elif personality == "Sage Advisor":
            return f"That's a profound question. {random.choice(responses)}"
        else:
            return random.choice(responses)

def add_message(role, content, personality=None):
    """Add a message to the chat history"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "personality": personality
    })

def display_chat():
    """Display the chat messages"""
    for message in st.session_state.messages:
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

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">🤖 Chatbot Settings</div>', unsafe_allow_html=True)
    
    # Personality selector
    selected_personality = st.selectbox(
        "Choose your AI personality:",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.current_personality)
    )
    
    if selected_personality != st.session_state.current_personality:
        st.session_state.current_personality = selected_personality
        # Add personality change message
        add_message("assistant", f"Switched to {selected_personality} mode! {PERSONALITIES[selected_personality]['greeting']}", selected_personality)
        st.rerun()
    
    st.markdown(f"**Current:** {selected_personality}")
    st.markdown(f"*{PERSONALITIES[selected_personality]['description']}*")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    # Export chat
    if st.button("📤 Export Chat", type="secondary"):
        if st.session_state.messages:
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages
            }
            st.download_button(
                label="Download Chat",
                data=json.dumps(chat_data, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.markdown("---")
    
    # Chat statistics
    if st.session_state.messages:
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.markdown("**📊 Chat Statistics:**")
        st.markdown(f"• Your messages: {user_messages}")
        st.markdown(f"• AI responses: {bot_messages}")
        st.markdown(f"• Total messages: {len(st.session_state.messages)}")

# Main chat interface
st.markdown('<div class="main-header">🤖 AI Chatbot</div>', unsafe_allow_html=True)

# Welcome message if no messages yet
if not st.session_state.messages:
    add_message("assistant", PERSONALITIES[st.session_state.current_personality]["greeting"], st.session_state.current_personality)

# Display chat messages
display_chat()

# Chat input
with st.container():
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message
        add_message("user", user_input)
        
        # Generate and add bot response
        with st.spinner("🤖 Thinking..."):
            time.sleep(0.5)  # Simulate thinking time
            response = generate_response(user_input, st.session_state.current_personality)
            add_message("assistant", response, st.session_state.current_personality)
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        Made with ❤️ using Streamlit | AI Chatbot v1.0
    </div>
    """,
    unsafe_allow_html=True
)
