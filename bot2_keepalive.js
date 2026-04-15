// =======================================================
// Bot 2: US Visa Scheduling Session Keep-Alive
// =======================================================
// Instructions:
// 1. Open your Chrome tab with the US Visa Scheduling page.
// 2. Press F12 to open Developer Tools.
// 3. Go to the "Console" tab.
// 4. Paste this ENTIRE code and hit Enter.
// =======================================================

console.log("Starting Visa Keep-Alive Bot...");
console.log("This will toggle the OFC post between New Delhi and Mumbai every 5 minutes to keep the session alive.");

let isRunning = true;

// Create a small visual UI so you know it's running, and can stop it easily!
const panel = document.createElement("div");
panel.id = "visa-keepalive-panel";
panel.style.position = "fixed";
panel.style.bottom = "20px";
panel.style.right = "20px";
panel.style.backgroundColor = "rgba(0, 0, 0, 0.85)";
panel.style.color = "white";
panel.style.padding = "15px";
panel.style.borderRadius = "8px";
panel.style.zIndex = "999999";
panel.style.fontFamily = "sans-serif";
panel.style.boxShadow = "0px 4px 6px rgba(0,0,0,0.3)";
panel.innerHTML = `
    <div style="margin-bottom: 10px;">
        <span style="font-size: 16px; font-weight: bold;">Visa Keep-Alive</span>
        <span id="botStatus" style="font-size: 16px; margin-left: 10px;">🟢 Running</span>
    </div>
    <div style="font-size: 12px; margin-bottom: 10px; color: #ccc;">
        Toggling dropdown every 5 mins.<br>
        Next toggle in ~5 minutes.
    </div>
    <button id="stopBotBtn" style="padding: 6px 12px; cursor: pointer; background-color: #ff4757; color: white; border: none; border-radius: 4px; font-weight: bold;">Stop Bot</button>
`;

// Append to body if not already there
if(document.getElementById("visa-keepalive-panel")) {
    document.getElementById("visa-keepalive-panel").remove();
}
document.body.appendChild(panel);

document.getElementById("stopBotBtn").addEventListener("click", () => {
    isRunning = false;
    document.getElementById("botStatus").innerText = "🔴 Stopped";
    document.getElementById("botStatus").style.color = "#ff4757";
    document.getElementById("stopBotBtn").style.display = "none";
    console.log("Visa Bot stopped. You can use the site manually now without any interruptions.");
    clearInterval(intervalId);
});

function togglePost() {
    if (!isRunning) return;
    
    // Find all select elements
    let selects = document.querySelectorAll("select");
    let targetSelect = null;
    
    // Look for the select element that contains both New Delhi and Mumbai as options
    for (let s of selects) {
        let text = s.innerText.toLowerCase();
        if (text.includes("new delhi") && text.includes("mumbai")) {
            targetSelect = s;
            break;
        }
    }
    
    if (targetSelect) {
        // Find option values dynamically
        let optMumbai = Array.from(targetSelect.options).find(o => o.text.toLowerCase().includes("mumbai"));
        let optDelhi = Array.from(targetSelect.options).find(o => o.text.toLowerCase().includes("new delhi"));
        
        if (optMumbai && optDelhi) {
            let currentText = targetSelect.options[targetSelect.selectedIndex].text.toLowerCase();
            
            // Toggle
            if (currentText.includes("new delhi")) {
                targetSelect.value = optMumbai.value;
                console.log(`[${new Date().toLocaleTimeString()}] Toggled position to: Mumbai`);
            } else {
                targetSelect.value = optDelhi.value;
                console.log(`[${new Date().toLocaleTimeString()}] Toggled position to: New Delhi`);
            }
            
            // Let the website (React/Angular) know the dropdown physically changed
            targetSelect.dispatchEvent(new Event('change', { bubbles: true }));
            targetSelect.dispatchEvent(new Event('input', { bubbles: true }));
        }
    } else {
        console.log(`[${new Date().toLocaleTimeString()}] Could not find the dropdown for OFC Post. Let me know if the page structure changed!`);
    }
}

// 5 minutes = 300,000 ms. 5 minutes is slow enough to not get blocked, but fast enough to keep session alive.
const intervalId = setInterval(togglePost, 30 * 1000);
console.log("Active! Keeping your session alive...");
