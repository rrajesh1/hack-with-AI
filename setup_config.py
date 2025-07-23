#!/usr/bin/env python3
"""
Setup script to create configuration files for the Slack bot
"""
import json
import shutil
from pathlib import Path

def create_config_file():
    """Interactive setup to create config file"""
    print("🚀 Slack Bot Configuration Setup")
    print("=" * 40)
    
    # Check if config already exists
    if Path("config.json").exists():
        overwrite = input("⚠️  config.json already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Choose config format
    print("\nChoose configuration format:")
    print("1. JSON (recommended)")
    print("2. YAML")
    
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    use_yaml = choice == '2'
    
    if use_yaml:
        # Check if PyYAML is available
        try:
            import yaml
        except ImportError:
            print("\n❌ PyYAML not installed. Install with: pip install pyyaml")
            print("Falling back to JSON format...")
            use_yaml = False
    
    # Get user input
    print(f"\n📝 Enter your Slack tokens:")
    print("(You can get these from https://api.slack.com/apps)")
    
    bot_token = input("Bot Token (xoxb-...): ").strip()
    app_token = input("App Token (xapp-...): ").strip()
    
    # Validate tokens
    if not bot_token.startswith('xoxb-'):
        print("⚠️  Warning: Bot token should start with 'xoxb-'")
    
    if not app_token.startswith('xapp-'):
        print("⚠️  Warning: App token should start with 'xapp-'")
    
    # Optional settings
    print(f"\n⚙️  Optional settings:")
    bot_name = input("Bot name (default: Awesome Slackbot): ").strip() or "Awesome Slackbot"
    environment = input("Environment (development/production, default: development): ").strip() or "development"
    
    # Create config
    config = {
        "slack": {
            "bot_token": bot_token,
            "app_token": app_token
        },
        "environment": environment,
        "bot": {
            "name": bot_name,
            "version": "1.0.0",
            "debug": environment == "development"
        },
        "features": {
            "welcome_messages": True,
            "reaction_responses": True,
            "joke_commands": True
        },
        "logging": {
            "level": "DEBUG" if environment == "development" else "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
    
    # Save config
    if use_yaml:
        import yaml
        filename = "config.yaml"
        with open(filename, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    else:
        filename = "config.json"
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to {filename}")
    print(f"🔐 Remember to keep your tokens secure!")
    print(f"📁 The file {filename} has been added to .gitignore")
    
    # Copy example files if they don't exist
    if not Path("config.example.json").exists():
        if Path("config.example.json").exists():
            print("📄 Example config files are already available")
        else:
            print("📄 Creating example config files...")

def main():
    """Main setup function"""
    create_config_file()
    
    print(f"\n🎉 Setup complete! You can now run your bot with:")
    print(f"   slack run")
    print(f"   or")
    print(f"   python slackbot.py")

if __name__ == "__main__":
    main() 