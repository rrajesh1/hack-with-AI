"""
Message event listeners for the Slack bot.
"""
import re
import random

def register_message_listeners(app):
    """Register all message-related event listeners."""
    
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

    @app.message("goodbye")
    def message_goodbye(say):
        """Respond to goodbye messages with random farewells"""
        responses = ["Adios", "Au revoir", "Farewell", "See you later!", "Until next time!"]
        parting = random.choice(responses)
        say(f"{parting}! 👋")

    @app.message(re.compile("thanks|thank you", re.IGNORECASE))
    def message_thanks(message, say):
        """Respond to thanks"""
        user = message['user']
        responses = [
            f"You're welcome, <@{user}>! 😊",
            f"Happy to help, <@{user}>! 🎉",
            f"No problem at all, <@{user}>! ✨",
            f"Anytime, <@{user}>! 🤖"
        ]
        say(random.choice(responses)) 