# Appointment Availability Utility Suite

This repository contains a suite of automation tools designed to monitor appointment availability and maintain active sessions on scheduling portals. The suite consists of two primary components: a Python-based availability tracker and a JavaScript-based session maintenance script.

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** (for the Checker bot)
- **Google Chrome** installed (required for undetected-chromedriver)
- **ntfy** app installed on your phone (optional, for mobile notifications)

---

## 🤖 Bot 1: Availability Tracker (`bot1_checker.py`)

This Python script monitors a specific tracking website for new slot openings. It uses an undetected version of ChromeDriver to bypass bot detection and provides both local audio alerts and mobile push notifications.

### Features
- **Smart Parsing**: Automatically extracts future dates from unstructured text content.
- **Audio Alarms**: Plays a system sound alert on your computer when a criteria-met slot is found.
- **Mobile Notifications**: Integrates with [ntfy.sh](https://ntfy.sh) to send instant alerts to your phone.
- **Auto-Refresh**: Periodically refreshes the page to check for real-time updates.

### Setup
1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your parameters at the top of `bot1_checker.py`:
   - `TARGET_DATE`: Set your desired date threshold.
   - `NTFY_TOPIC`: Set a unique name for your mobile notifications.
   - `REFRESH_SECONDS`: Frequency of checks.

### Running the Bot
```bash
python bot1_checker.py
```

---

## 🟢 Bot 2: Session Keep-Alive (`bot2_keepalive.js`)

A lightweight JavaScript snippet designed to be run directly in the browser console. It prevents session timeouts on scheduling portals by simulating user activity.

### Features
- **Visual Interface**: Adds a small, unobtrusive dashboard to the bottom-right of your browser window.
- **Intelligent Toggling**: Cycles through location options (e.g., New Delhi and Mumbai) to trigger a state change on the server.
- **Safe Interval**: Toggles every 30 seconds to ensure the session remains active without overloading the server.
- **Manual Override**: Includes a "Stop Bot" button to immediately cease automation for manual intervention.

### How to Use
1. Log in to your scheduling portal and navigate to the main dashboard or slot selection page.
2. Press `F12` (or `Right Click` > `Inspect`) and navigate to the **Console** tab.
3. Copy the entire contents of `bot2_keepalive.js`.
4. Paste it into the console and press `Enter`.
5. You will see a green "Running" status indicator on your screen.

---

## 🔔 Setting Up Mobile Notifications

To receive alerts on your phone:
1. Download the **ntfy** app (Android/iOS).
2. Click the **+** (Subscribe) button.
3. Enter the same `NTFY_TOPIC` name you defined in `bot1_checker.py`.
4. Ensure the bot is running, and you will receive notifications immediately when slots are detected!

---

## ⚖️ Disclaimer
These tools are for educational and personal assistance purposes only. Use responsibly and ensure compliance with the terms of service of any website you interact with.
