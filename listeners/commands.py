"""
Slash command listeners for the Slack bot.
"""
import random

def register_command_listeners(app):
    """Register all slash command listeners."""
    
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
            "Why did the database administrator break up with the developer? Too many relationship issues! 💔",
            "What's a programmer's favorite hangout place? Foo Bar! 🍻",
            "Why do Java developers wear glasses? Because they can't C#! 👓",
            "How do you comfort a JavaScript bug? You console it! 🐞"
        ]
        respond(random.choice(jokes))

    @app.command("/ping")
    def ping_command(ack, respond):
        """Simple ping command to test bot responsiveness"""
        ack()
        respond("🏓 Pong! Bot is alive and responsive!")

    @app.command("/about")
    def about_command(ack, respond):
        """Show information about the bot"""
        ack()
        about_text = """
🤖 *About This Bot*

Built with Slack Bolt for Python ⚡️
• Framework: Bolt for Python
• Features: Message responses, slash commands, events
• Status: Online and ready to help!

Type `/help` for available commands or just say "help" in a message.
        """
        respond(about_text) 