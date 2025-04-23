### **AirForge**

---

#### **Overview**

**AirForge** is a Python-based tool designed for WPA/WPA2 handshake cracking. It automates the process of network scanning, handshake capturing, wordlist selection, and password cracking using `aircrack-ng`. The tool provides a user-friendly interface with multiple options for wordlist generation and selection, making it a versatile solution for penetration testers and security researchers.

---

#### **Features**

1. **Network Scanning**:
   - Scans for nearby wireless networks using `airodump-ng`.
   - Allows the user to select a target BSSID and channel.

2. **Handshake Capture**:
   - Captures WPA/WPA2 handshakes using `airodump-ng`.
   - Sends deauthentication packets with `aireplay-ng` to force handshake generation.

3. **Wordlist Selection**:
   - Offers three options for wordlist selection:
     1. Use the default `rockyou.txt`.
     2. Generate a custom wordlist based on user-provided keywords.
     3. Download a wordlist from an online source.

4. **Automatic Cracking**:
   - Runs `aircrack-ng` automatically with the selected wordlist and captured handshake.

5. **Custom Wordlist Generation**:
   - Allows users to create a tailored wordlist for targeted attacks.

---

#### **Requirements**

- Python 3.x
- Linux-based system with the following tools installed:
  - `aircrack-ng`
  - `airodump-ng`
  - `aireplay-ng`
  - `curl` (for downloading wordlists)
- `rockyou.txt` wordlist (can be installed via `wordlists` package).

---

#### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/AirForge.git
   cd AirForge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `rockyou.txt` is available:
   ```bash
   sudo apt install wordlists
   gunzip /usr/share/wordlists/rockyou.txt.gz
   ```

---

#### **Usage**

1. Run the tool with root privileges:
   ```bash
   sudo python3 Main.py
   ```

2. Follow the prompts:
   - **Network Scanning**: Select a target BSSID and channel.
   - **Handshake Capture**: The tool captures the handshake and saves it to a `.cap` file.
   - **Wordlist Selection**: Choose one of the following options:
     1. Use `rockyou.txt`.
     2. Generate a custom wordlist.
     3. Download a wordlist from an online source.
   - **Automatic Cracking**: The tool runs `aircrack-ng` with the selected wordlist and captured handshake.

---

#### **Example Workflow**

1. **Start the Tool**:
   ```bash
   sudo python3 Main.py
   ```

2. **Scan for Networks**:
   - The tool uses `airodump-ng` to scan for networks.
   - Press `Ctrl+C` when you see the desired BSSID and channel.

3. **Capture Handshake**:
   - The tool captures the handshake and saves it to `/root/Desktop/handshake-01.cap`.

4. **Select Wordlist**:
   - Choose one of the wordlist options:
     - Use `rockyou.txt`.
     - Generate a custom wordlist.
     - Download an online wordlist.

5. **Crack the Handshake**:
   - The tool runs `aircrack-ng` automatically with the selected wordlist.

---

#### **Example Output**

```plaintext
[*] Running airodump-ng to scan for networks...
[!] Stopping airodump-ng...
[?] Enter the BSSID you want to target: 50:91:E3:BC:D8:8C
[?] Enter the corresponding channel: 6
[*] Starting handshake capture...
[+] Handshake file saved to: /root/Desktop/handshake-01.cap
[*] Choosing a wordlist...
[1] Use rockyou.txt
[2] Generate a custom wordlist
[3] Download an online wordlist
[?] Choose wordlist option: 1
[*] Starting aircrack-ng to crack the handshake...
Opening /root/Desktop/handshake-01.cap
Read 100 packets...
1 handshake detected for BSSID: 50:91:E3:BC:D8:8C
```

---

#### **Disclaimer**

This tool is intended for educational purposes and authorized penetration testing only. Unauthorized use of this tool is illegal and unethical. The developers are not responsible for any misuse of this tool.

---

#### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
