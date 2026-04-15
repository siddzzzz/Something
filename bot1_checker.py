import time
import winsound
import requests
import re
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# ============== CONFIGURATION =================
# Target Date threshold
TARGET_DATE = datetime.strptime("01-Jun-2026", "%d-%b-%Y")
# checkvisaslots F-1 page
CHECK_URL = "https://checkvisaslots.com/latest-us-visa-availability/f-1-regular/"
# Define a unique notification topic name - MAKE SURE to enter this exactly in the ntfy app!
# Install 'ntfy' on your phone, click the + button, and subscribe to this name.
NTFY_TOPIC = "my_f1_visa_alerts" 
# How often to refresh (in seconds)
REFRESH_SECONDS = 60 
# ==============================================

def play_alarm():
    """Makes your laptop scream using the built in Windows sounds!"""
    print(">>> PLAYING ALARM <<<")
    # Beep(frequency, duration_ms) sometimes fails on modern laptops if motherboard speakers are disabled.
    # We will use winsound.PlaySound and standard Beeps in a mix to ensure it plays!
    for _ in range(5):
        # Play standard exclamation sound
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        time.sleep(0.5)

def ping_phone(date_str):
    """Sends a push notification to your phone using ntfy"""
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=f"Hurry! New Delhi VAC date found: {date_str}".encode('utf-8'),
            headers={
                "Title": "VISA SLOT AVAILABLE", 
                "Priority": "urgent",
                "Tags": "tada,warning"
            }
        )
        print(f"Successfully pushed notification to your phone via topic '{NTFY_TOPIC}'")
    except Exception as e:
        print(f"Failed to send push notification: {e}")

def extract_date(text):
    """
    Attempts to extract the appointment date.
    Often the 'Last Updated' date is on the same line (like today/yesterday's date).
    We extract ALL dates and pick the one that is in the FUTURE.
    """
    dates_found = []
    
    # regex 1: 15-May-2026, 15 May 2026, 1st May 2026, 01 May 26
    matches1 = re.finditer(r"(\d{1,2})(?:st|nd|rd|th)?[- ,]+([a-zA-Z]{3,})[- ,]+(\d{4}|\d{2})", text)
    # regex 2: May 15, 2026
    matches2 = re.finditer(r"([a-zA-Z]{3,})[- ,]+(\d{1,2})(?:st|nd|rd|th)?[- ,]+(\d{4}|\d{2})", text)
    
    for match in matches1:
        day, monthStr, year = match.groups()
        monthStr = monthStr[:3].capitalize()
        year = "20" + year if len(year) == 2 else year
        date_str = f"{day.zfill(2)}-{monthStr}-{year}"
        try:
            dt = datetime.strptime(date_str, "%d-%b-%Y")
            dates_found.append((dt, date_str))
        except: pass
        
    for match in matches2:
        monthStr, day, year = match.groups()
        monthStr = monthStr[:3].capitalize()
        year = "20" + year if len(year) == 2 else year
        date_str = f"{day.zfill(2)}-{monthStr}-{year}"
        try:
            dt = datetime.strptime(date_str, "%d-%b-%Y")
            dates_found.append((dt, date_str))
        except: pass
        
    # Pick the future date
    now = datetime.now()
    for dt, date_str in dates_found:
        if dt > now:
            return dt, date_str
            
    return None, None

def extract_minutes_ago(text):
    """
    Extracts the relative time like '14 mins ago' and converts it to minutes.
    """
    match = re.search(r'(\d+)\s+(min|minute|hour|day)s?', text, re.IGNORECASE)
    if match:
        val = int(match.group(1))
        unit = match.group(2).lower()
        if unit.startswith('min'):
            return val
        elif unit.startswith('hour'):
            return val * 60
        elif unit.startswith('day'):
            return val * 60 * 24
    return None

def run_bot():
    print("=" * 50)
    print("     US VISA F-1 TRACKER STARTING    ")
    print("=" * 50)
    print(f"Target: Must find a date BEFORE {TARGET_DATE.strftime('%d-%b-%Y')}")
    print(f"Phone Notifications: Subscribe to 'ntfy.sh/{NTFY_TOPIC}' on your ntfy app!")
    print("Opening Chrome...\n")
    
    # Initialize Chrome with undetected-chromedriver to bypass Cloudflare
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    driver.get(CHECK_URL)

    last_seen_date_str_vac = None
    last_context_nd = None
    last_minutes_ago_nd = None
    last_date_str_nd = None

    while True:
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] Checking page for New Delhi dates...")
        
        try:
            # Wait for content to load. Using 8 seconds to be safe with cloudflare/React rendering
            time.sleep(8) 
            
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            lines = body_text.split('\n')
            
            # --- Check NEW DELHI VAC ---
            found_dt_vac = None
            date_str_vac = None
            for i, line in enumerate(lines):
                if "new delhi vac" in line:
                    context = " ".join(lines[i:i+20])
                    found_dt_vac, date_str_vac = extract_date(context)
                    if found_dt_vac:
                        break
                        
            if found_dt_vac:
                print(f" -> Spotted NEW DELHI VAC! Earliest future date parsed: {date_str_vac}")

                is_updated_vac = False
                if last_seen_date_str_vac is not None and date_str_vac != last_seen_date_str_vac:
                    is_updated_vac = True

                last_seen_date_str_vac = date_str_vac
                
                if found_dt_vac < TARGET_DATE:
                    print("\n" + "*"*50)
                    print(f"  MATCH FOUND! New Delhi VAC {date_str_vac} IS EARLIER THAN {TARGET_DATE.strftime('%d-%b-%Y')}!")
                    print("*"*50)
                    ping_phone(f"VAC: {date_str_vac} (Target Met!)")
                    play_alarm()
                elif is_updated_vac:
                    print("\n" + "*"*50)
                    print(f"  UPDATE DETECTED! New Delhi VAC date changed to {date_str_vac}!")
                    print("*"*50)
                    ping_phone(f"VAC Update: {date_str_vac}")
                    play_alarm()
                else:
                    print(f" -> Ignore VAC. {date_str_vac} is unfortunately past our target ({TARGET_DATE.strftime('%d-%b-%Y')}) and identical to last seen.")
            else:
                 print(" -> 'NEW DELHI VAC' valid future date not found.")

            # --- Check NEW DELHI (Interview) ---
            found_dt_nd = None
            date_str_nd = None
            context_nd = None
            
            for i, line in enumerate(lines):
                if "new delhi" in line and "vac" not in line:
                    # Grab the next 10 lines to get date and relative time
                    context_nd = " ".join(lines[i:i+10])
                    found_dt_nd, date_str_nd = extract_date(context_nd)
                    break
                    
            if context_nd:
                new_mins = extract_minutes_ago(context_nd)
                
                if date_str_nd:
                    print(f" -> Spotted NEW DELHI (Interview)! Earliest future date parsed: {date_str_nd} (Updated ~{new_mins} mins ago)")
                else:
                    print(f" -> Spotted NEW DELHI (Interview), no valid future date. (Updated ~{new_mins} mins ago)")
                    
                is_real_update = False
                
                # Check 1: Did the date change entirely?
                if last_date_str_nd is not None and date_str_nd != last_date_str_nd:
                    is_real_update = True
                    
                # Check 2: Did the relative time drop?
                if last_minutes_ago_nd is not None and new_mins is not None:
                    if new_mins < last_minutes_ago_nd:
                        is_real_update = True
                
                last_context_nd = context_nd
                last_minutes_ago_nd = new_mins
                last_date_str_nd = date_str_nd
                
                if is_real_update:
                    print("\n" + "*"*50)
                    print(f"  UPDATE DETECTED! New Delhi (Interview) has a fresh update!")
                    print("*"*50)
                    msg = f"Interview Update! Date: {date_str_nd}" if date_str_nd else "Interview Update (no exact date)"
                    ping_phone(msg)
                    play_alarm()
            else:
                print(" -> 'NEW DELHI' (Interview) was not found in the page text right now.")
                
        except Exception as e:
            print(f" -> Encountered an issue reading the page structure: {e}")
            
        print(f" -> Waiting {REFRESH_SECONDS} seconds before the next check...")
        time.sleep(REFRESH_SECONDS)
        
        try:
            driver.refresh()
        except:
            pass

if __name__ == "__main__":
    run_bot()
