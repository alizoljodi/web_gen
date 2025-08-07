# 🤖 AI Chatbot - Streamlit App

A modern, interactive chatbot built with Streamlit that can be deployed on Streamlit Cloud.

## ✨ Features

- **Multiple AI Personalities**: Choose from 4 different chatbot personalities
  - 🤖 Friendly Assistant
  - 💻 Tech Expert  
  - ✨ Creative Writer
  - 🧘‍♂️ Sage Advisor

- **Modern UI**: Beautiful gradient design with custom styling
- **Chat History**: Persistent conversation history during session
- **Real-time Chat**: Instant responses with typing indicators
- **Export Functionality**: Download chat conversations as JSON
- **Statistics**: Track message counts and conversation metrics
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser** and go to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork or clone this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**

3. **Sign in with GitHub** and click "New app"

4. **Configure your app**:
   - **Repository**: Select your forked repository
   - **Branch**: `main` (or your preferred branch)
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.9 or higher

5. **Click "Deploy"** and wait for the build to complete

6. **Your app will be live** at a URL like: `https://your-app-name.streamlit.app`

## 🎯 How to Use

1. **Choose a Personality**: Use the sidebar to select your preferred AI personality
2. **Start Chatting**: Type your message in the chat input at the bottom
3. **Switch Personalities**: Change personalities anytime during the conversation
4. **Export Chats**: Download your conversation history as a JSON file
5. **Clear Chat**: Start a fresh conversation with the clear button

## 🛠️ Customization

### Adding New Personalities

To add a new personality, edit the `PERSONALITIES` dictionary in `streamlit_app.py`:

```python
"Your New Personality": {
    "description": "Description of your personality",
    "greeting": "Initial greeting message",
    "responses": [
        "Response 1",
        "Response 2",
        "Response 3"
    ]
}
```

### Modifying the UI

The app uses custom CSS for styling. You can modify the styles in the `st.markdown()` section at the top of the file.

### Enhancing Responses

The `generate_response()` function handles response generation. You can enhance it by:
- Adding more keyword detection
- Implementing more sophisticated response logic
- Integrating with external APIs
- Adding context awareness

## 📁 File Structure

```
├── streamlit_app.py      # Main application file
├── requirements.txt      # Python dependencies
├── README_STREAMLIT.md  # This file
└── .gitignore          # Git ignore file (optional)
```

## 🔧 Configuration

### Environment Variables

The app doesn't require any environment variables for basic functionality, but you can add them for enhanced features:

```bash
# Optional: Add API keys for external services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Streamlit Configuration

Create a `.streamlit/config.toml` file for custom Streamlit settings:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 🚀 Deployment Tips

1. **Keep it Simple**: Start with the basic version before adding complex features
2. **Test Locally**: Always test your app locally before deploying
3. **Monitor Logs**: Check Streamlit Cloud logs if deployment fails
4. **Update Dependencies**: Keep your requirements.txt up to date
5. **Use Environment Variables**: For sensitive data like API keys

## 🐛 Troubleshooting

### Common Issues

1. **App won't deploy**:
   - Check that `streamlit_app.py` is in the root directory
   - Verify `requirements.txt` exists and is valid
   - Ensure Python version compatibility

2. **Import errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check for typos in import statements

3. **UI not loading**:
   - Clear browser cache
   - Check browser console for errors
   - Verify CSS syntax

### Getting Help

- Check [Streamlit documentation](https://docs.streamlit.io/)
- Visit [Streamlit community](https://discuss.streamlit.io/)
- Review [Streamlit Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)

## 📈 Future Enhancements

- [ ] Integration with OpenAI API for more intelligent responses
- [ ] Voice input/output capabilities
- [ ] File upload and analysis features
- [ ] Multi-language support
- [ ] User authentication and chat history persistence
- [ ] Advanced analytics and insights
- [ ] Custom training data support

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ using Streamlit**
