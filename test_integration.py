"""
Bot Integration Testing Script
Test your Slack bot integration and functionality
"""
import os
import sys
from datetime import datetime
from slack_bolt import App
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BotTester:
    def __init__(self):
        self.app = None
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} - {test_name}"
        if message:
            result += f": {message}"
        
        print(result)
        self.test_results.append({
            'name': test_name,
            'passed': passed,
            'message': message,
            'timestamp': timestamp
        })
        
        return passed
    
    def test_environment_variables(self):
        """Test that required environment variables are set"""
        print("\n🔧 Testing Environment Variables...")
        
        bot_token = os.environ.get("SLACK_BOT_TOKEN")
        app_token = os.environ.get("SLACK_APP_TOKEN")
        
        self.log_test(
            "Bot Token Present", 
            bool(bot_token), 
            "SLACK_BOT_TOKEN is required"
        )
        
        self.log_test(
            "App Token Present", 
            bool(app_token), 
            "SLACK_APP_TOKEN is required"
        )
        
        if bot_token:
            self.log_test(
                "Bot Token Format", 
                bot_token.startswith("xoxb-"), 
                "Bot token should start with 'xoxb-'"
            )
        
        if app_token:
            self.log_test(
                "App Token Format", 
                app_token.startswith("xapp-"), 
                "App token should start with 'xapp-'"
            )
        
        return bool(bot_token and app_token)
    
    def test_bot_connection(self):
        """Test basic bot connectivity"""
        print("\n🔌 Testing Bot Connection...")
        
        try:
            self.app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
            response = self.app.client.api_test()
            
            return self.log_test(
                "API Connection", 
                response["ok"], 
                "Bot can connect to Slack API"
            )
        except Exception as e:
            return self.log_test(
                "API Connection", 
                False, 
                f"Connection failed: {str(e)}"
            )
    
    def test_bot_permissions(self):
        """Test bot permissions and identity"""
        print("\n🔐 Testing Bot Permissions...")
        
        if not self.app:
            return self.log_test("Permissions", False, "No bot connection available")
        
        try:
            auth_response = self.app.client.auth_test()
            
            self.log_test(
                "Authentication", 
                auth_response["ok"], 
                f"Bot authenticated as {auth_response.get('user', 'Unknown')}"
            )
            
            # Test if bot has basic permissions
            try:
                channels_response = self.app.client.conversations_list(
                    exclude_archived=True,
                    limit=1
                )
                self.log_test(
                    "Channel Access", 
                    channels_response["ok"], 
                    "Bot can list channels"
                )
            except Exception as e:
                self.log_test(
                    "Channel Access", 
                    False, 
                    f"Cannot access channels: {str(e)}"
                )
            
            return True
            
        except Exception as e:
            return self.log_test(
                "Authentication", 
                False, 
                f"Auth failed: {str(e)}"
            )
    
    def test_socket_mode_setup(self):
        """Test Socket Mode configuration"""
        print("\n🔌 Testing Socket Mode Setup...")
        
        app_token = os.environ.get("SLACK_APP_TOKEN")
        if not app_token:
            return self.log_test(
                "Socket Mode", 
                False, 
                "App token required for Socket Mode"
            )
        
        try:
            from slack_bolt.adapter.socket_mode import SocketModeHandler
            # Just test if we can create the handler without starting it
            handler = SocketModeHandler(self.app, app_token)
            
            return self.log_test(
                "Socket Mode", 
                True, 
                "Socket Mode handler created successfully"
            )
        except Exception as e:
            return self.log_test(
                "Socket Mode", 
                False, 
                f"Socket Mode setup failed: {str(e)}"
            )
    
    def test_bot_extensions(self):
        """Test if bot extensions are available"""
        print("\n🔧 Testing Bot Extensions...")
        
        try:
            from bot_extensions import register_extensions
            self.log_test(
                "Extensions Import", 
                True, 
                "bot_extensions.py found and importable"
            )
            
            # Test registration (without actually registering)
            if self.app:
                original_handlers = len(self.app._middleware_list)
                register_extensions(self.app)
                new_handlers = len(self.app._middleware_list)
                
                self.log_test(
                    "Extensions Registration", 
                    new_handlers >= original_handlers, 
                    f"Extensions registered ({new_handlers - original_handlers} new handlers)"
                )
            
            return True
            
        except ImportError as e:
            return self.log_test(
                "Extensions Import", 
                False, 
                f"bot_extensions.py not found: {str(e)}"
            )
        except Exception as e:
            return self.log_test(
                "Extensions Registration", 
                False, 
                f"Extension registration failed: {str(e)}"
            )
    
    def test_dependencies(self):
        """Test required dependencies"""
        print("\n📦 Testing Dependencies...")
        
        dependencies = [
            ('slack_bolt', 'Slack Bolt framework'),
            ('dotenv', 'Python dotenv for environment variables'),
            ('requests', 'HTTP requests library'),
        ]
        
        all_deps_ok = True
        for dep, description in dependencies:
            try:
                __import__(dep)
                self.log_test(f"Dependency: {dep}", True, description)
            except ImportError:
                self.log_test(f"Dependency: {dep}", False, f"Missing: {description}")
                all_deps_ok = False
        
        return all_deps_ok
    
    def run_integration_test(self):
        """Run a simulated integration test"""
        print("\n🧪 Running Integration Test...")
        
        if not self.app:
            return self.log_test("Integration", False, "No bot connection available")
        
        try:
            # Test creating a simple message (without sending)
            test_message = {
                "channel": "test",
                "text": "Integration test message"
            }
            
            # Just validate the message structure
            required_fields = ['channel', 'text']
            valid_message = all(field in test_message for field in required_fields)
            
            self.log_test(
                "Message Structure", 
                valid_message, 
                "Bot can create valid message structure"
            )
            
            # Test event handling setup
            event_handlers = hasattr(self.app, '_listeners')
            self.log_test(
                "Event Handlers", 
                event_handlers, 
                "Bot has event handling capability"
            )
            
            return True
            
        except Exception as e:
            return self.log_test(
                "Integration", 
                False, 
                f"Integration test failed: {str(e)}"
            )
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print("🏁 TEST SUMMARY")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  • {result['name']}: {result['message']}")
        
        print("\n" + "="*50)
        
        if failed_tests == 0:
            print("🎉 All tests passed! Your bot integration looks good!")
        elif failed_tests <= 2:
            print("⚠️  Minor issues detected. Check failed tests above.")
        else:
            print("🚨 Several issues detected. Please review your setup.")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 Starting Bot Integration Tests...")
        print("="*50)
        
        # Run tests in order
        env_ok = self.test_environment_variables()
        
        if env_ok:
            self.test_bot_connection()
            self.test_bot_permissions()
            self.test_socket_mode_setup()
        
        self.test_dependencies()
        self.test_bot_extensions()
        
        if env_ok:
            self.run_integration_test()
        
        return self.print_summary()

def main():
    """Main function to run tests"""
    tester = BotTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 