import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Load bot extensions if available
try:
    from bot_extensions import register_extensions
    register_extensions(app)
    print("🔧 Bot extensions loaded successfully!")
except ImportError:
    print("ℹ️  No bot extensions found. Using basic functionality only.")
except Exception as e:
    print(f"⚠️  Warning: Could not load bot extensions: {e}")

@app.message("hello")
def message_hello(message, say):
    """Respond to 'hello' messages"""
    user = message['user']
    say(f"Hey there <@{user}>! 👋")

@app.message(re.compile("help", re.IGNORECASE))
def message_help(message, say):
    """Respond to help requests"""
    help_text = """
🤖 *Available Commands:*
• Say `hello` - I'll greet you back
• Say `help` - Shows this help message
• Use `/echo <text>` - I'll echo your text back
• Use `/joke` - I'll tell you a joke
• Mention me in any channel and I'll respond!
    """
    say(help_text)

@app.command("/echo")
def echo_command(ack, respond, command):
    """Echo command - repeats what user types"""
    ack()
    text = command['text']
    if text:
        respond(f"🔄 You said: {text}")
    else:
        respond("Please provide some text to echo! Usage: `/echo your message here`")

@app.command("/joke")
def joke_command(ack, respond):
    """Tell a random joke"""
    ack()
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 🧪",
        "Why did the programmer quit his job? He didn't get arrays! 💻",
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
        "Why did the database administrator break up with the developer? Too many relationship issues! 💔"
    ]
    import random
    respond(random.choice(jokes))

@app.event("app_mention")
def handle_app_mention_events(body, say):
    """Handle when the bot is mentioned"""
    event = body["event"]
    user = event['user']
    text = event['text']
    
    # Remove the bot mention from the text
    clean_text = re.sub(r'<@\w+>', '', text).strip()
    
    if not clean_text:
        say(f"Hi <@{user}>! You mentioned me but didn't say anything. Try saying 'help' to see what I can do! 🤖")
    else:
        say(f"Thanks for mentioning me, <@{user}>! You said: '{clean_text}'. Type 'help' to see my commands! 😊")

@app.event("member_joined_channel")
def welcome_message(event, say):
    """Welcome new members to the channel"""
    user = event['user']
    channel = event['channel']
    say(f"Welcome to the channel, <@{user}>! 🎉 I'm your friendly bot assistant. Say 'help' to see what I can do!")

# Error handling
@app.error
def custom_error_handler(error, body):
    print(f"Error: {error}")
    print(f"Request body: {body}")

# Start the app
if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("❌ Error: SLACK_BOT_TOKEN environment variable is required")
        print("Please check your .env file and Slack app configuration")
        exit(1)
    
    if not os.environ.get("SLACK_APP_TOKEN"):
        print("❌ Error: SLACK_APP_TOKEN environment variable is required")
        print("Please check your .env file and Slack app configuration")
        exit(1)
    
    print("🚀 Starting Slackbot...")
    print("Bot is running and ready to receive events!")
    
    # Start the app using Socket Mode
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start() 