# 🚀 AI Content Generator - Mobile App

A powerful Android app for generating AI-powered social media content on the go! No backend hosting required - just install and use.

## ✨ Features

- **🤖 AI Text Generation** - Create engaging posts for Twitter, LinkedIn, Instagram, Facebook
- **🎨 AI Image Generation** - Generate stunning images with Bytez AI
- **🎭 Multiple Tones** - Professional, Casual, Enthusiastic, Formal, Funny, Inspirational
- **📚 History** - Save and review all your generated content
- **🔐 Private** - All API keys stored locally on your device
- **☁️ No Server Needed** - Works entirely through third-party APIs

## 🔑 Supported AI Providers (All FREE!)

1. **Gemini** (Google AI Studio) - [Get free API key](https://aistudio.google.com/app/apikey)
2. **Groq** - [Get free API key](https://console.groq.com/keys)
3. **OpenRouter** - [Get free API key](https://openrouter.ai/keys)
4. **Bytez** (Images) - [Get free API key](https://bytez.com/api)

## 📦 Installation

### Option 1: Download Pre-built APK (Easiest)
1. Go to [Releases](../../releases)
2. Download the latest `AI-Content-Generator-debug.apk`
3. Install on your Android device

### Option 2: Build from Source

#### Prerequisites
- Python 3.9+
- Git

#### Local Build (Requires Build Tools)
```bash
# Clone the repository
git clone <your-repo-url>
cd what

# Install buildozer
pip install buildozer

# Build APK (will download Android SDK/NDK automatically)
buildozer android debug

# Find your APK in bin/ folder
```

#### Cloud Build (No Local Setup Required!)
1. Fork this repository to your GitHub account
2. Push any changes to the `main` branch
3. Go to **Actions** tab in your GitHub repository
4. Wait for the build to complete (~10-15 minutes)
5. Download the APK from **Artifacts**

## 🎯 How to Use

1. **Install the APK** on your Android device
2. **Open the app** and go to ⚙️ Settings
3. **Add your API keys**:
   - Get free keys from the providers listed above
   - Paste them in the respective fields
   - Click 💾 Save
4. **Go back** to home screen
5. **Enter your prompt** (e.g., "A motivational post about productivity")
6. **Select platform** and **tone**
7. **Click Generate Text** or **Generate Image**
8. **Copy and share** your content! 🎉

## 📱 Screenshots

### Home Screen
Beautiful, modern UI with dark theme and smooth animations

### Settings
Securely store your API keys (never leaves your device)

### History
Review all your generated content anytime

## 🛠️ Tech Stack

- **Python 3.9** - Core language
- **Kivy 2.3.0** - Mobile UI framework
- **SQLite** - Local database for settings and history
- **Requests** - HTTP client for API calls
- **Buildozer** - APK packaging tool
- **GitHub Actions** - Automated cloud builds

## 🔒 Privacy

- All API keys are stored **locally** on your device
- No data is sent to any server except the AI provider APIs you choose
- Your prompts and generated content are stored in a local SQLite database
- No analytics, tracking, or third-party services

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - feel free to use this project however you like!

## 🌟 Credits

Built with ❤️ using free AI services:
- Google Gemini
- Groq
- OpenRouter
- Bytez

---

**Made for creators, by creators** 🎨✨
