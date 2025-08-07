# 🌐 AI HTML Generator - Streamlit App

A powerful AI-powered HTML generator built with Streamlit and Groq API that creates complete websites from text prompts and automatically opens them in your browser.

## ✨ Features

- **AI-Powered HTML Generation**: Uses Groq's Llama 3.1 70B model to generate complete HTML pages
- **Multiple Specialized Personalities**: Choose from 4 different AI personalities
  - 🌐 HTML Generator (General purpose)
  - 🎨 Portfolio Creator (Portfolio websites)
  - 💼 Business Website (Professional business sites)
  - ✨ Creative Designer (Artistic and unique designs)

- **Automatic Browser Opening**: Generated websites open automatically in your browser
- **Modern UI**: Beautiful gradient design with custom styling
- **Real-time Generation**: Instant HTML generation with progress indicators
- **Download Functionality**: Download generated HTML files
- **Responsive Design**: Works perfectly on all devices
- **Chat History**: Persistent conversation history during session
- **Export Functionality**: Download chat conversations as JSON

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

1. **Choose a Personality**: Use the sidebar to select your preferred AI personality
2. **Describe Your Website**: Type a detailed description of the website you want to create
   - Example: "Create a modern portfolio website for a photographer"
   - Example: "Build a restaurant landing page with menu and contact form"
   - Example: "Generate an e-commerce site for selling handmade jewelry"
3. **Generate**: Press Enter to start generation
4. **Watch the Magic**: See real-time progress as AI generates your webpage
5. **View Results**: The generated page opens automatically in your browser
6. **Download**: Save the HTML file for further customization

## 🛠️ Customization

### Adding New Personalities

To add a new personality, edit the `PERSONALITIES` dictionary in `streamlit_app.py`:

```python
"Your New Personality": {
    "description": "Description of your personality",
    "greeting": "Initial greeting message",
    "system_prompt": """Your specialized system prompt for this personality.
    Include specific instructions for the type of websites this personality should create."""
}
```

### Modifying the UI

The app uses custom CSS for styling. You can modify the styles in the `st.markdown()` section at the top of the file.

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
- [ ] Voice input for website descriptions
- [ ] Image generation for websites
- [ ] Advanced SEO optimization

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ using Streamlit and Groq**
