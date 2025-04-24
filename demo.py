import time
import random
import pyautogui
import pygetwindow as gw
 
def keep_vscode_active(duration_minutes=60, interval_seconds=60):
    end_time = time.time() + duration_minutes * 60
 
    print(f"Keeping VS Code active for {duration_minutes} minutes...")
 
    while time.time() < end_time:
        # Try to find and focus VS Code
        windows = gw.getWindowsWithTitle('Visual Studio Code')
        if windows:
            vscode = windows[0]
            if not vscode.isActive:
                vscode.activate()
                time.sleep(1)  # Give time to switch
 
            # Simulate light activity: move mouse or press shift
            pyautogui.press('shift')
            print(f"[{time.strftime('%H:%M:%S')}] Simulated input in VS Code.")
        else:
            print("VS Code window not found. Make sure it's open.")
 
        time.sleep(interval_seconds)
 
    print("Finished keeping VS Code active.")
 
if __name__ == "__main__":
    keep_vscode_active(duration_minutes=60)
 