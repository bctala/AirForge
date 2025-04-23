### **Updated README: AirForge**

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
     1. Choose from all saved wordlists in the system (e.g., `/usr/share/wordlists/`).
     2. Generate a custom wordlist based on user-provided keywords.
     3. Download a wordlist from an online source.

4. **Automatic Cracking**:
   - Runs `aircrack-ng` automatically with the selected wordlist and captured handshake.

5. **Custom Wordlist Generation**:
   - Allows users to create a tailored wordlist for targeted attacks.

6. **BSSID Extraction**:
   - Automatically extracts the BSSID from an existing `.cap` file if the user provides one, eliminating the need to manually input the BSSID.

---

#### **Requirements**

- Python 3.x
- Linux-based system with the following tools installed:
  - `aircrack-ng`
  - `airodump-ng`
  - `aireplay-ng`
  - `curl` (for downloading wordlists)
- Wordlists stored in `/usr/share/wordlists/` (e.g., `rockyou.txt`).

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

3. Ensure wordlists are available:
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
   - **Existing `.cap` File**: If you already have a `.cap` file, provide its path, and the tool will extract the BSSID automatically.
   - **Network Scanning**: If no `.cap` file is provided, the tool scans for networks and allows you to select a target BSSID and channel.
   - **Handshake Capture**: The tool captures the handshake and saves it to a `.cap` file.
   - **Wordlist Selection**: Choose one of the following options:
     1. Select from all saved wordlists in the system.
     2. Generate a custom wordlist.
     3. Download a wordlist from an online source.
   - **Automatic Cracking**: The tool runs `aircrack-ng` with the selected wordlist and captured handshake.

---

#### **Example Workflow**

1. **Start the Tool**:
   ```bash
   sudo python3 Main.py
   ```

2. **Use an Existing `.cap` File**:
   - The tool asks:
     ```plaintext
     [?] Do you want to use an existing .cap file? (y/n): y
     [?] Enter the full path to the .cap file: /root/Desktop/handshake-01.cap
     [+] Using existing .cap file: /root/Desktop/handshake-01.cap
     [*] Extracting BSSID from the .cap file...
     [+] Extracted BSSID: 50:91:E3:BC:D8:8C
     ```

3. **Scan for Networks** (if no `.cap` file is provided):
   - The tool uses `airodump-ng` to scan for networks.
   - Press `Ctrl+C` when you see the desired BSSID and channel.

4. **Capture Handshake**:
   - The tool captures the handshake and saves it to `/root/Desktop/handshake-01.cap`.

5. **Select Wordlist**:
   - Choose one of the wordlist options:
     - Select from saved wordlists (e.g., `rockyou.txt`, `fasttrack.txt`).
     - Generate a custom wordlist.
     - Download an online wordlist.

6. **Crack the Handshake**:
   - The tool runs `aircrack-ng` automatically with the selected wordlist:
     ```plaintext
     [*] Starting aircrack-ng to crack the handshake...
     Opening /root/Desktop/handshake-01.cap
     Read 100 packets...
     1 handshake detected for BSSID: 50:91:E3:BC:D8:8C
     ```

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
[1] Select from saved wordlists
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

---

#### **Based On**

This project incorporates code from [WordlistGenerator](https://github.com/lamaAlshuhail/WordlistGenerator), originally developed by @lamaAlshuhail.
