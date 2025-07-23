"""
Main entry point for Slack CLI
This file is used by 'slack run' command
"""
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Import your main bot functionality
from slackbot import app

def main():
    """Main function to start the bot"""
    # Check if required environment variables are set
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("❌ Error: SLACK_BOT_TOKEN environment variable is required")
        print("Please check your .env file and Slack app configuration")
        exit(1)
    
    if not os.environ.get("SLACK_APP_TOKEN"):
        print("❌ Error: SLACK_APP_TOKEN environment variable is required")
        print("Please check your .env file and Slack app configuration")
        exit(1)
    
    print("🚀 Starting Slackbot via Slack CLI...")
    print("Bot is running and ready to receive events!")
    
    # Start the app using Socket Mode
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

if __name__ == "__main__":
    main() 