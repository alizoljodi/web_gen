# 💕 Lovable - Web Generator

A beautiful Streamlit app that generates complete HTML web pages using AI. Built with the same stunning UI as the original Gradio app.

## ✨ Features

- **AI-Powered Web Generation**: Uses Groq's Llama 3.1 70B model to generate complete HTML pages
- **Beautiful UI**: Stunning gradient design with glassmorphism effects
- **Real-time Generation**: Instant HTML generation with progress indicators
- **Browser Integration**: Automatically opens generated pages in your browser
- **Download Functionality**: Download generated HTML files
- **Responsive Design**: Works perfectly on all devices
- **Modern Styling**: Professional gradients, animations, and typography

## 🚀 Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Groq API key**:
   ```bash
   export groq_api="your-groq-api-key-here"
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork or clone this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**

3. **Sign in with GitHub** and click "New app"

4. **Configure your app**:
   - **Repository**: Select your forked repository
   - **Branch**: `main` (or your preferred branch)
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.9 or higher

5. **Add your Groq API key** in the Streamlit Cloud secrets:
   - Go to your app settings
   - Add secret: `groq_api = "your-groq-api-key-here"`

6. **Click "Deploy"** and wait for the build to complete

7. **Your app will be live** at a URL like: `https://your-app-name.streamlit.app`

## 🎯 How to Use

1. **Enter a Prompt**: Describe the website you want to create
   - Example: "Create a modern portfolio website for a photographer"
   - Example: "Build a restaurant landing page with menu and contact form"
   - Example: "Generate an e-commerce site for selling handmade jewelry"

2. **Click Generate**: Press the ↑ button to start generation

3. **Watch the Magic**: See real-time progress as AI generates your webpage

4. **View Results**: The generated page opens automatically in your browser

5. **Download**: Save the HTML file for further customization

## 🛠️ Customization

### Modifying the UI

The app uses custom CSS for the beautiful gradient design. You can modify the styles in the `st.markdown()` section at the top of the file.

### Enhancing Generation

The `generate_html_with_groq()` function handles HTML generation. You can enhance it by:
- Modifying the system prompt for different styles
- Adding more specific instructions for certain website types
- Integrating with other AI models
- Adding more interactive features

### Environment Variables

```bash
# Required for Groq API
groq_api=your-groq-api-key-here
```

## 📁 File Structure

```
├── streamlit_app.py      # Main application file
├── requirements.txt      # Python dependencies
├── README_STREAMLIT.md  # This file
├── .streamlit/config.toml # Streamlit configuration
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Streamlit Configuration

The `.streamlit/config.toml` file contains optimal settings:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🚀 Deployment Tips

1. **API Key Security**: Always use Streamlit Cloud secrets for API keys
2. **Test Locally**: Always test your app locally before deploying
3. **Monitor Usage**: Keep track of your Groq API usage
4. **Error Handling**: The app includes fallback HTML for API failures
5. **Performance**: The app is optimized for fast generation

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**:
   - Check that your Groq API key is set correctly
   - Verify the key has sufficient credits
   - Test the key with a simple API call

2. **Generation Fails**:
   - Check the browser console for errors
   - Verify your prompt is clear and specific
   - Try a simpler prompt first

3. **Browser Doesn't Open**:
   - Check if pop-ups are blocked
   - Verify the HTML file is created in temp directory
   - Try manually opening the generated file

### Getting Help

- Check [Streamlit documentation](https://docs.streamlit.io/)
- Visit [Streamlit community](https://discuss.streamlit.io/)
- Review [Groq API documentation](https://console.groq.com/docs)

## 📈 Future Enhancements

- [ ] Multiple AI model support
- [ ] Template-based generation
- [ ] CSS framework integration
- [ ] Real-time collaboration
- [ ] Version control for generated pages
- [ ] Advanced customization options
- [ ] Integration with hosting platforms

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ using Streamlit and Groq**
