# 🚀 Quick Start Guide

## 📋 Prerequisites

Before building your APK, you'll need free API keys from these providers:

1. **Gemini** (Required for text generation)
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API key"
   - Copy the key

2. **Groq** (Optional but recommended - very fast!)
   - Visit: https://console.groq.com/keys
   - Sign up/login
   - Create new API key

3. **OpenRouter** (Optional fallback)
   - Visit: https://openrouter.ai/keys
   - Sign up/login
   - Create API key

4. **Bytez** (Required for image generation)
   - Visit: https://bytez.com/api
   - Sign up and get your API key

## 🏗️ Building Your APK

### Method 1: GitHub Actions (Recommended - No Local Setup!)

1. **Fork this repository** to your GitHub account

2. **Enable GitHub Actions**:
   - Go to your fork's "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

3. **Trigger a build**:
   - Make any small change (e.g., edit README.md)
   - Commit and push to `main` branch
   - OR go to Actions → Build Android APK → Run workflow

4. **Wait for build** (~10-15 minutes)

5. **Download your APK**:
   - Go to Actions tab
   - Click on the completed workflow
   - Scroll to "Artifacts"
   - Download "AI-Content-Generator-APK"

6. **Install on your Android device**:
   - Transfer APK to your phone
   - Enable "Install from unknown sources"
   - Install the APK

### Method 2: Local Build (Requires Some Setup)

**On Linux/macOS:**
```bash
# Install buildozer
pip install buildozer

# Build the APK (first time takes ~30-60 mins)
buildozer android debug

# Find your APK
ls bin/
```

**On Windows:**
- Local building on Windows is complex
- Highly recommend using GitHub Actions instead (Method 1)
- Alternatively, use WSL2 (Windows Subsystem for Linux)

## 📱 Using the App

1. **Install the APK** on your Android device

2. **First Launch**:
   - Open the app
   - Tap ⚙️ Settings
   - Paste your API keys
   - Tap 💾 Save

3. **Generate Content**:
   - Go back to home screen
   - Enter what you want to create
   - Select platform and tone
   - Tap "Generate Text" or "Generate Image"
   - Wait a few seconds
   - Your content appears!

4. **View History**:
   - Tap 📚 History to see all your generated content

## 🎨 Example Prompts

**For Text:**
- "A motivational Monday morning post"
- "5 tips for better productivity"
- "Announcement for a new product launch"
- "Engaging question to boost audience interaction"

**For Images:**
- "Professional photo of a modern office workspace"
- "Abstract colorful background for social media"
- "Minimalist logo concept for a tech startup"
- "Futuristic cityscape at sunset"

## 🐛 Troubleshooting

**"No API keys configured" error:**
- Make sure you added at least Gemini OR Groq API key in Settings
- Check that you tapped 💾 Save after entering keys

**"All providers failed" error:**
- Verify your API keys are correct (no extra spaces)
- Check your internet connection
- Gemini free tier has rate limits - wait a minute and try again

**APK won't install:**
- Enable "Install from unknown sources" in Android settings
- Make sure you have enough storage space
- Try uninstalling any previous versions

**GitHub Actions build failed:**
- Check the build logs for errors
- Common issue: Make sure buildozer.spec is properly formatted
- Try re-running the workflow

## 💡 Tips

- Start with Gemini API key (easiest to get)
- Add Groq for faster responses
- History is saved locally - never lost!
- Each API provider has free tier limits
- Test different tones for different content styles

## 🔒 Privacy Note

- All API keys stay on YOUR device only
- No tracking or analytics in this app
- Your prompts only go to the AI providers you choose
- History stored in local SQLite database

---

Need help? Check the main README.md or create an issue!
