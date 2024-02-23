import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import psutil
import time
import subprocess
import sys

def is_process_running(process_name):
    """
    Checks if a process with the given name is currently running.
    """
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def monitor_hitman3(icon):
    """
    Monitors the 'HITMAN 3' process and waits for it to close.
    """
    while is_process_running('HITMAN3.exe'):
        time.sleep(1)
    icon.update_menu()

def end_peacock_patcher(icon):
    """
    Terminates the 'Peacock Patcher' process and its associated cmd.
    """
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'PeacockPatcher.exe'], check=True)
        subprocess.run(["TASKKILL", "/F", "/FI", "IMAGENAME eq cmd.exe", "/T"])
        icon.stop()  # Stop the icon
        sys.exit()  # Terminate the script
    except subprocess.CalledProcessError:
        icon.stop()  # Stop the icon
        sys.exit()  # Terminate the script

def on_quit(icon):
    icon.stop()
    sys.exit()

def main():
    # Reference the icon file using sys._MEIPASS
    icon_path = os.path.join(sys._MEIPASS, "icon.ico")
    image = Image.open(icon_path)
    menu = (item('Quit', on_quit),)
    icon = pystray.Icon("name", image, "HITMAN 3 Monitor", menu=menu)
    icon.menu = menu  # Update menu reference
    icon.update_menu()  # Initial menu update
    while True:
        hitman3_running = is_process_running('HITMAN3.exe')
        if hitman3_running:
            monitor_hitman3(icon)
            end_peacock_patcher(icon)
        else:
            time.sleep(10)  # Wait for 10 seconds before checking again

if __name__ == "__main__":
    main()
