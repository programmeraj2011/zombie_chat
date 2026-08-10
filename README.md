# 🧟 ZOMBIE // CHAT

> TALK. SHARE. SURVIVE.

A lightweight local-network chat system built with **Python and Flask**.

Zombie Chat lets people connected to the same local network send messages and share images without requiring the internet.

---

## ✨ Features

- 💬 Local network chat
- 🧟 Persistent user handles
- 🖼️ Image sharing
- 📱 Mobile-friendly UI
- 🔄 Automatic message refresh
- ⚡ Lightweight Flask backend
- 🎨 Retro hacker-style interface
- 💾 LocalStorage-based handle memory
- 🌐 Works across devices on the same network
- 🚫 No camera or HTTPS required
- 👥 Multiple users can connect to the same server

---

## 📸 Screenshots

### 🧟 Main Interface

![Zombie Chat Main Interface](screenshots/home.png)

### 💬 Chat Interface

![Zombie Chat Chat](screenshots/chat.png)

---

# 🚀 Installation

## 📋 Requirements

You need:

- Python 3.x
- Git
- A modern web browser
- Wi-Fi/local network for multiple devices

---

## 1. Clone the Repository

```bash
git clone https://github.com/programmeraj2011/zombie_chat.git
```

---

## 2. Enter the Project

```bash
cd zombie_chat
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses:

```text
Flask
Werkzeug
```

---

# ▶️ Running Zombie Chat

Start the server:

```bash
python chat.py
```

You should see:

```text
==================================================
       🧟 ZOMBIE // CHAT
==================================================

Local:
http://127.0.0.1:5000

For other devices:
http://YOUR-PC-IP:5000

Camera: DISABLED
Image upload: ENABLED

==================================================
```

---

## 🌐 Open on Your Computer

Open:

```text
http://127.0.0.1:5000
```

You can also use:

```text
http://localhost:5000
```

---

# 📡 Use Zombie Chat on Multiple Devices

Zombie Chat can work across devices connected to the same local network.

### Step 1 — Start the Server

On your computer:

```bash
python chat.py
```

### Step 2 — Find Your Local IP

On Windows:

```bash
ipconfig
```

Look for:

```text
IPv4 Address
```

Example:

```text
192.168.1.5
```

### Step 3 — Connect Your Phone

Connect your phone to the same Wi-Fi network.

Open:

```text
http://192.168.1.5:5000
```

Replace `192.168.1.5` with the IP address of your computer.

---

# 🧟 Persistent Handles

The first time you open Zombie Chat, you enter your handle.

Example:

```text
programmer_aj
```

Your handle is saved using browser **LocalStorage**.

When you open the website again, you don't need to enter it again.

You can change it using the **CHANGE** button.

Your handle may be reset if browser site data or LocalStorage is cleared.

---

# 🖼️ Image Sharing

Zombie Chat supports image uploads directly from the chat interface.

Click:

```text
+ IMAGE
```

Choose an image and send it with your message.

Uploaded images are stored in:

```text
uploads/
```

Uploaded files are excluded from Git using `.gitignore`.

---

# 💬 Messaging

Messages are handled by the Flask backend.

The frontend automatically checks for new messages every few seconds.

The current chat history is stored in server memory.

Therefore:

> Restarting the Flask server clears the current chat history.

---

# 🛠️ Tech Stack

### Backend

- 🐍 Python
- 🌶️ Flask
- Werkzeug

### Frontend

- HTML
- CSS
- JavaScript

### Browser APIs

- 💾 LocalStorage
- 🌐 Fetch API

---

# 📁 Project Structure

```text
zombie_chat/
│
├── chat.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
│
├── uploads/
│   └── .gitkeep
│
└── screenshots/
    ├── home.png
    └── chat.png
```

---

# 📦 requirements.txt

```text
Flask
Werkzeug
```

Install them with:

```bash
pip install -r requirements.txt
```

---

# 🔧 Troubleshooting

## Flask is not installed

Run:

```bash
pip install -r requirements.txt
```

---

## `python` is not recognized

Try:

```bash
python3 chat.py
```

If that doesn't work, install Python and add it to your PATH.

---

## Other devices cannot connect

Check that:

- Both devices are connected to the same Wi-Fi
- Zombie Chat is running
- You are using the correct local IP
- Port `5000` is allowed through Windows Firewall

Example:

```text
http://192.168.1.5:5000
```

---

## Images are not uploading

Make sure the `uploads/` directory exists:

```text
uploads/
```

The project automatically creates it when the server starts.

---

## Chat history disappeared

Zombie Chat currently stores messages in server memory.

Restarting:

```bash
python chat.py
```

will clear the existing chat history.

---

# 🔒 Privacy & Security

Zombie Chat is designed for local-network experimentation.

It does not currently provide:

- User authentication
- End-to-end encryption
- Database storage
- Production-grade security

Do not expose the Flask development server directly to the public internet without adding appropriate security controls.

---

# ⚠️ Disclaimer

Zombie Chat is an experimental project created for learning, experimentation, and local-network communication.

It uses Flask's development server and is not intended to be a production-ready chat service.

---

# 🤝 Contributing

Contributions and ideas are welcome.

You can:

1. Fork the repository
2. Create a branch
3. Make your changes
4. Commit your changes
5. Open a pull request

Example:

```bash
git checkout -b feature/new-feature
```

```bash
git add .
```

```bash
git commit -m "Add new feature"
```

```bash
git push origin feature/new-feature
```

---

# 👨‍💻 Creator

## Aditya Jaiswal

Built with:

```text
Python + Flask + JavaScript + ☕ + 🧟
```

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.

---

## 🧟 ZOMBIE // CHAT

> **TALK. SHARE. SURVIVE.**

Built for local networks.  
Built for experimentation.  
Built without depending on the internet.