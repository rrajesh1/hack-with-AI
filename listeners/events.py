"""
Event listeners for the Slack bot.
"""
import re

def register_event_listeners(app):
    """Register all event listeners."""
    
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

    @app.event("reaction_added")
    def handle_reaction_added(event, say):
        """Handle when reactions are added to messages"""
        reaction = event.get('reaction', '')
        
        # Respond to specific reactions
        if reaction == 'wave':
            channel = event['item']['channel']
            user = event['user']
            say(channel=channel, text=f"👋 Hey there <@{user}>! Thanks for the wave!")
        elif reaction == 'robot_face':
            channel = event['item']['channel']
            say(channel=channel, text="🤖 Beep boop! Robot detected! Thanks for the robot love!")

    @app.event("team_join")
    def handle_team_join(event, say, client):
        """Handle when new users join the team"""
        user = event["user"]
        user_id = user["id"]
        
        # Send a welcome DM to the new user
        try:
            dm_channel = client.conversations_open(users=user_id)
            welcome_message = f"""
🎉 Welcome to the team, <@{user_id}>!

I'm your friendly Slack bot assistant. Here's what I can help you with:
• Type 'help' to see available commands
• Use `/joke` for programming humor
• Use `/echo` to test message responses
• Just mention me (@bot) in any channel!

Feel free to reach out if you need anything! 🤖
            """
            client.chat_postMessage(
                channel=dm_channel["channel"]["id"],
                text=welcome_message
            )
        except Exception as e:
            # If we can't send a DM, that's okay - user might have DMs disabled
            print(f"Could not send welcome DM to {user_id}: {e}")

    # Error handling
    @app.error
    def custom_error_handler(error, body):
        """Handle errors that occur during message processing"""
        print(f"Error: {error}")
        print(f"Request body: {body}")
        
        # You could send error notifications to a specific channel here
        # or log to an external service 