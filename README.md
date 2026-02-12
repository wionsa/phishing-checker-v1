# Phishing Checker V1 🛡️

A professional tool designed to detect phishing threats in emails using a hybrid approach: AI-driven semantic analysis (GPT-4) and global threat intelligence (VirusTotal)

---

## 🛠 Installation & Setup

Follow these steps to deploy the project on a new machine

### 📦 Step 1: Backend Deployment

1.  **Clone the repository**
    ```bash
    git clone https://github.com/wionsa/phishing-checker-v1.git
    cd phishing-checker-v1
    ```

2.  **Environment Setup**
    ```bash
    # Update system and install dependencies
    sudo apt update && sudo apt install python3-pip python3-venv -y

    # Initialize virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Python packages
    pip install -r requirements.txt
    ```

3.  **SSL Configuration (HTTPS)**
    > [!IMPORTANT]
    > The extension requires a secure connection to communicate with the Flask backend
    
    ```bash
    mkdir ssl
    openssl req -x509 -newkey rsa:4096 -nodes -out ssl/server.crt -keyout ssl/server.key -days 365
    ```
    *(Press **Enter** for all prompts during certificate generation)*

4.  **Environment Variables**
    Create a `.env` file and add your VirusTotal API key:
    ```text
    VT_API_KEY=your_real_virustotal_key_here
    ```

5.  **Run the Server**
    ```bash
    python3 app.py
    ```

---

### 🧩 Step 2: Chrome Extension Installation

1.  **Open Extensions Page:** Go to `chrome://extensions/` in Chrome
2.  **Enable Developer Mode:** Toggle the switch in the **top right corner**
3.  **Load the Extension:** Click **Load unpacked** and select the `chrome-checker` folder
4.  **SSL Trust (Crucial):** Visit `https://127.0.0.1:5555/` and click **Advanced ➔ Proceed to 127.0.0.1 (unsafe)** to allow the extension to connect

---

## 🚀 How to Use

There are two ways to analyze potential threats:

### Option A: Automatic Gmail Analysis
1. Open any email in your **Gmail** account
2. Click the blue **"Check for Phishing"** button that appears in the Gmail interface
3. The system will automatically extract the sender's email, message body, and links
4. A new tab will open, showing the final safety report

### Option B: Manual Check (Web Interface)
1. Click on the **Phishing Checker extension icon** in your browser toolbar
2. Navigate to the **Manual Check** page (or go to `https://127.0.0.1:5555/index`)
3. Manually enter the sender's address, text, and URLs, or **upload a file** for scanning
4. Click **"Run Analysis"** to receive the results
