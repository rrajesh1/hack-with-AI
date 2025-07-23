# 🤖 Slackbot with Python

A modern Slackbot built with Python using the Slack Bolt framework. This bot can respond to messages, handle slash commands, and interact with users in your Slack workspace.

## ✨ Features

- **Message Responses**: Responds to keywords like "hello" and "help"
- **Slash Commands**: 
  - `/echo` - Echoes back your message
  - `/joke` - Tells random programming jokes
- **Mentions**: Responds when mentioned in channels
- **Welcome Messages**: Greets new channel members
- **Error Handling**: Robust error handling and logging

## 🚀 Quick Start

### 1. Create a Slack App

1. Go to [api.slack.com](https://api.slack.com) and click "Create New App"
2. Choose "From scratch"
3. Name your app (e.g., "My Awesome Bot") and select your workspace
4. Click "Create App"

### 2. Configure Bot Permissions

1. In your app settings, go to **"OAuth & Permissions"**
2. Under "Scopes" → "Bot Token Scopes", add these permissions:
   ```
   app_mentions:read
   channels:read
   chat:write
   commands
   users:read
   ```
3. Click **"Install to Workspace"** and authorize the app
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

### 3. Enable Socket Mode

1. Go to **"Socket Mode"** in your app settings
2. Click **"Enable Socket Mode"**
3. Create an App-Level Token:
   - Name: "Socket Mode Token"
   - Scope: `connections:write`
4. Copy the **"App-Level Token"** (starts with `xapp-`)

### 4. Configure Event Subscriptions

1. Go to **"Event Subscriptions"**
2. Enable Events
3. Subscribe to these bot events:
   ```
   app_mention
   member_joined_channel
   message.channels
   message.groups
   message.im
   message.mpim
   ```

### 5. Create Slash Commands

1. Go to **"Slash Commands"**
2. Create two commands:
   
   **Command 1:**
   - Command: `/echo`
   - Description: "Echo back your message"
   - Usage Hint: `[your message]`
   
   **Command 2:**
   - Command: `/joke`
   - Description: "Get a random programming joke"

### 6. Set Up Your Development Environment

1. **Clone and navigate to your project:**
   ```bash
   cd hack-with-AI
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your tokens:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_APP_TOKEN=xapp-your-actual-app-token
   ```

5. **Run the bot:**
   ```bash
   python slackbot.py
   ```

You should see:
```
🚀 Starting Slackbot...
Bot is running and ready to receive events!
```

## 🎯 How to Use

### In Slack:

1. **Direct Messages:**
   - Type `hello` → Bot greets you
   - Type `help` → Shows available commands

2. **Slash Commands:**
   - `/echo Hello World!` → Bot responds with "🔄 You said: Hello World!"
   - `/joke` → Bot tells a random programming joke

3. **Mentions:**
   - `@YourBot what's up?` → Bot responds to your mention

4. **Channel Events:**
   - Bot welcomes new members when they join a channel

## 🛠️ Customization

### Adding New Commands

Edit `slackbot.py` to add new functionality:

```python
@app.command("/newcommand")
def new_command(ack, respond):
    ack()
    respond("This is my new command!")
```

### Adding Message Responses

```python
@app.message("keyword")
def respond_to_keyword(message, say):
    say("Response to the keyword!")
```

### Adding Events

```python
@app.event("event_name")
def handle_event(event, say):
    # Handle the event
    pass
```

## 📋 Project Structure

```
hack-with-AI/
├── slackbot.py          # Main bot application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your actual environment variables (not in git)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🔧 Troubleshooting

### Common Issues:

1. **"SLACK_BOT_TOKEN environment variable is required"**
   - Make sure your `.env` file exists and has the correct tokens

2. **Bot doesn't respond to messages**
   - Check that Event Subscriptions are enabled
   - Verify bot has proper permissions
   - Make sure bot is added to the channel

3. **Slash commands don't work**
   - Ensure slash commands are created in your Slack app settings
   - Check that the command names match exactly

4. **"Invalid token" errors**
   - Verify your tokens are correct and haven't expired
   - Bot token should start with `xoxb-`
   - App token should start with `xapp-`

### Enable Debug Mode:

Add to your `.env` file:
```env
ENVIRONMENT=development
```

## 📚 Resources

- [Slack Bolt for Python Documentation](https://slack.dev/bolt-python/concepts)
- [Slack API Documentation](https://api.slack.com/)
- [Socket Mode Guide](https://api.slack.com/apis/connections/socket)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy Bot Building! 🚀**