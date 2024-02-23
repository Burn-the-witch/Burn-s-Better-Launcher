import tkinter as tk
from tkinter import filedialog, messagebox, IntVar
from subprocess import Popen, CREATE_NEW_CONSOLE
from PIL import Image, ImageTk
import os
import json
import subprocess
import sys
from ctypes import windll

class DarkModeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hitman Launcher")
        self.master.geometry("912x516")
        self.master.resizable(True, True)  # Allow resizing

        # Bind event for window resizing
        self.master.bind("<Configure>", self.resize_background)

        # Remove the title bar
        self.master.overrideredirect(True)
        self.set_appwindow()

        # Load the custom font with scaled size and bold
        self.custom_font = ("medium_NeueHaasGrotesk.ttf", 18, "bold")

        # Load the background image
        self.background_image = Image.open(os.path.join(sys._MEIPASS, "background.png"))  # Modify path
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a canvas for the background image with transparency
        self.background_canvas = tk.Canvas(self.master, bg=self.master["background"], highlightthickness=0)
        self.background_canvas.create_image(0, 0, anchor="nw", image=self.background_photo)
        self.background_canvas.pack(fill="both", expand=True)

        # Create transparent buttons with background color
        self.button_bg_color = "#580D12"  # Background color for buttons
        self.button_fg_color = "white"    # Foreground color for buttons

        # Load icon images with scaling
        icon_size = 40
        icon_dir = sys._MEIPASS  # Modify path
        self.retail_icon = Image.open(os.path.join(icon_dir, "retail_icon.png")).resize((icon_size, icon_size))
        self.retail_icon = ImageTk.PhotoImage(self.retail_icon)
        self.peacock_icon = Image.open(os.path.join(icon_dir, "peacock_icon.png")).resize((icon_size, icon_size))
        self.peacock_icon = ImageTk.PhotoImage(self.peacock_icon)
        self.smf_icon = Image.open(os.path.join(icon_dir, "smf_icon.png")).resize((icon_size, icon_size))
        self.smf_icon = ImageTk.PhotoImage(self.smf_icon)
        self.deploy_icon = Image.open(os.path.join(icon_dir, "deploy_icon.png")).resize((icon_size, icon_size))
        self.deploy_icon = ImageTk.PhotoImage(self.deploy_icon)
        self.settings_icon = Image.open(os.path.join(icon_dir, "settings_icon.png")).resize((icon_size, icon_size))
        self.settings_icon = ImageTk.PhotoImage(self.settings_icon)
        self.quit_icon = Image.open(os.path.join(icon_dir, "quit_icon.png")).resize((icon_size, icon_size))
        self.quit_icon = ImageTk.PhotoImage(self.quit_icon)

        # Define buttons with icons and padding
        padding = 10  # Padding between icon and text
        self.launch_retail_button = tk.Button(self.background_canvas, text="Play (Retail)", image=self.retail_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.launch_retail, highlightthickness=0, bd=0, font=self.custom_font)
        self.launch_peacock_button = tk.Button(self.background_canvas, text="Play (Peacock)", image=self.peacock_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.launch_peacock, highlightthickness=0, bd=0, font=self.custom_font)
        self.launch_smf_button = tk.Button(self.background_canvas, text="Open SMF", image=self.smf_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.launch_smf, highlightthickness=0, bd=0, font=self.custom_font)
        self.deploy_mods_button = tk.Button(self.background_canvas, text="Deploy Mods", image=self.deploy_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.deploy_mods, highlightthickness=0, bd=0, font=self.custom_font)
        self.settings_button = tk.Button(self.background_canvas, text="Settings", image=self.settings_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.open_settings_window, highlightthickness=0, bd=0, font=self.custom_font)
        self.quit_button = tk.Button(self.background_canvas, text="Quit", image=self.quit_icon, compound="left", padx=padding, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color, command=self.master.destroy, highlightthickness=0, bd=0, font=self.custom_font)

        # Place buttons on canvas
        self.launch_retail_button.place(relx=0.1, rely=0.35, anchor="w")
        self.launch_peacock_button.place(relx=0.1, rely=0.45, anchor="w")
        self.launch_smf_button.place(relx=0.1, rely=0.55, anchor="w")
        self.deploy_mods_button.place(relx=0.1, rely=0.65, anchor="w")
        self.settings_button.place(relx=0.1, rely=0.75, anchor="w")
        self.quit_button.place(relx=0.1, rely=0.85, anchor="w")

        # Center the window after widgets are placed
        self.center_window()

        # Default directories
        self.hitman_location = ""
        self.peacock_location = ""
        self.smf_location = ""

        # Initialize variables for launch options
        self.launch_after_deploy_retail = IntVar(value=0)
        self.launch_after_deploy_peacock = IntVar(value=0)

        self.load_config()  # Load configuration from JSON file

        # Flag to track if cockblocker has been launched
        self.cockblocker_launched = False

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x_offset = (self.master.winfo_screenwidth() - width) // 2
        y_offset = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    def resize_background(self, event=None):
        # Resize the background image to fit the window size
        self.background_image_resized = self.background_image.resize((self.master.winfo_width(), self.master.winfo_height()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image_resized)
        self.background_canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

    def load_config(self):
        try:
            with open("config.json", "r") as file:
                data = json.load(file)
                self.hitman_location = data.get("hitman_location", "")
                self.peacock_location = data.get("peacock_location", "")
                self.smf_location = data.get("smf_location", "")
                self.launch_after_deploy_retail.set(data.get("launch_after_deploy_retail", 0))
                self.launch_after_deploy_peacock.set(data.get("launch_after_deploy_peacock", 0))
        except FileNotFoundError:
            pass
    
    def save_config(self):
        data = {
            "hitman_location": self.hitman_location,
            "peacock_location": self.peacock_location,
            "smf_location": self.smf_location,
            "launch_after_deploy_retail": self.launch_after_deploy_retail.get(),
            "launch_after_deploy_peacock": self.launch_after_deploy_peacock.get()
        }
        with open("config.json", "w") as file:
            json.dump(data, file)
        
    def open_settings_window(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        
        # Function to set Hitman location
        def set_hitman_location():
            directory = filedialog.askdirectory(initialdir=self.hitman_location, title="Select Hitman Location")
            if directory:
                self.hitman_location = directory
                hitman_location_var.set(directory)
                
        # Function to set Peacock location
        def set_peacock_location():
            directory = filedialog.askdirectory(initialdir=self.peacock_location, title="Select Peacock Location")
            if directory:
                self.peacock_location = directory
                peacock_location_var.set(directory)
        
        # Function to set SMF location
        def set_smf_location():
            directory = filedialog.askdirectory(initialdir=self.smf_location, title="Select SMF Location")
            if directory:
                self.smf_location = directory
                smf_location_var.set(directory)
        
        # Hitman Location selection
        tk.Label(settings_window, text="Hitman Location:").pack(anchor="w")
        hitman_location_var = tk.StringVar()
        hitman_location_var.set(self.hitman_location)
        hitman_entry = tk.Entry(settings_window, textvariable=hitman_location_var, state="readonly")
        hitman_entry.pack(fill="x", padx=10, pady=(0, 5), anchor="w")
        tk.Button(settings_window, text="Select Directory", command=set_hitman_location).pack(anchor="w")
        
        # Peacock Location selection
        tk.Label(settings_window, text="Peacock Location:").pack(anchor="w")
        peacock_location_var = tk.StringVar()
        peacock_location_var.set(self.peacock_location)
        peacock_entry = tk.Entry(settings_window, textvariable=peacock_location_var, state="readonly")
        peacock_entry.pack(fill="x", padx=10, pady=(0, 5), anchor="w")
        tk.Button(settings_window, text="Select Directory", command=set_peacock_location).pack(anchor="w")

        # SMF Location selection
        tk.Label(settings_window, text="SMF Location:").pack(anchor="w")
        smf_location_var = tk.StringVar()
        smf_location_var.set(self.smf_location)
        smf_entry = tk.Entry(settings_window, textvariable=smf_location_var, state="readonly")
        smf_entry.pack(fill="x", padx=10, pady=(0, 5), anchor="w")
        tk.Button(settings_window, text="Select Directory", command=set_smf_location).pack(anchor="w")

        # Launch options for Hitman after deploying mods
        tk.Label(settings_window, text="Launch Hitman after deploying mods:").pack(anchor="w")
        tk.Checkbutton(settings_window, text="Retail", variable=self.launch_after_deploy_retail, onvalue=1, offvalue=0).pack(anchor="w")
        tk.Checkbutton(settings_window, text="Peacock", variable=self.launch_after_deploy_peacock, onvalue=1, offvalue=0).pack(anchor="w")
        
        # Button to save settings and exit
        tk.Button(settings_window, text="Save Settings", command=lambda: [self.save_config(), settings_window.destroy()]).pack()
        
    def launch_retail(self):
        if self.hitman_location:
            launcher_path = os.path.join(self.hitman_location, "Launcher.old.exe")
            if os.path.exists(launcher_path):
                Popen([launcher_path, "-skip_launcher"], cwd=self.hitman_location)
                self.save_config()  # Save configuration to JSON file
                self.close_peacock()  # Close Peacock processes
                self.master.destroy()  # Destroy main window
            else:
                messagebox.showerror("Error", "Launcher.old.exe not found in selected Hitman Location.")
        else:
            messagebox.showerror("Error", "Please select Hitman Location.")
    
    def launch_peacock(self):
        if self.hitman_location and self.peacock_location:
            launcher_path = os.path.join(self.hitman_location, "Launcher.old.exe")
            peacock_cmd_path = os.path.join(self.peacock_location, "Start Server.cmd")
            peacock_patcher_path = os.path.join(self.peacock_location, "PeacockPatcher.exe")
            
            if os.path.exists(launcher_path) and os.path.exists(peacock_cmd_path) and os.path.exists(peacock_patcher_path):
                Popen([launcher_path, "-skip_launcher"], cwd=self.hitman_location)
                self.close_peacock()  # Close Peacock processes
                Popen(peacock_cmd_path, cwd=self.peacock_location, creationflags=CREATE_NEW_CONSOLE)
                Popen(peacock_patcher_path, cwd=self.peacock_location)
                if not self.cockblocker_launched:
                    self.launch_cockblocker()  # Launch Cockblocker only if it hasn't been launched yet
                    self.cockblocker_launched = True  # Set flag to indicate Cockblocker has been launched
                self.save_config()  # Save configuration to JSON file
                self.master.destroy()  # Destroy main window
            else:
                messagebox.showerror("Error", "One or more required files not found in selected directories.")
        else:
            messagebox.showerror("Error", "Please select both Hitman and Peacock locations.")

    def launch_smf(self):
        if self.hitman_location and self.smf_location:
            launcher_path = os.path.join(self.smf_location, "Mod Manager.cmd")
            if os.path.exists(launcher_path):
                Popen(launcher_path, cwd=self.smf_location)
                self.save_config()  # Save configuration to JSON file
                self.master.destroy()  # Destroy main window
            else:
                messagebox.showerror("Error", "Mod Manager.cmd not found in selected SMF Location.")
        else:
            messagebox.showerror("Error", "Please select both Hitman and SMF locations.")

    def deploy_mods(self):
        if self.smf_location:
            deploy_path = os.path.join(self.smf_location, "Deploy.exe")
            if os.path.exists(deploy_path):
                process = Popen(deploy_path, cwd=self.smf_location, creationflags=CREATE_NEW_CONSOLE)
                process.wait()  # Wait for deploy.exe to finish
                # Check if either option for launching Hitman after deploying mods is selected
                if self.launch_hitman_after_deploy("Retail"):
                    self.launch_hitman("Retail")
                elif self.launch_hitman_after_deploy("Peacock"):
                    self.launch_hitman("Peacock")
            else:
                messagebox.showerror("Error", "Deploy.exe not found in selected SMF Location.")
        else:
            messagebox.showerror("Error", "Please select SMF Location.")
    
    def close_peacock(self):
        subprocess.run(["TASKKILL", "/F", "/FI", "IMAGENAME eq cmd.exe", "/T"])
        subprocess.run(["TASKKILL", "/F", "/FI", "IMAGENAME eq PeacockPatcher.exe", "/T"])

    def launch_hitman_after_deploy(self, option):
        if option == "Retail":
            return self.launch_after_deploy_retail.get() == 1
        elif option == "Peacock":
            return self.launch_after_deploy_peacock.get() == 1
        else:
            return False

    def launch_hitman(self, option):
        if option == "Retail":
            self.launch_retail()
        elif option == "Peacock":
            self.launch_peacock()

    def set_appwindow(self):
        self.master.attributes("-toolwindow", True)  # Make the window a tool window
        self.master.attributes("-topmost", True)    # Set the window to be always on top
        self.master.attributes("-topmost", False)   # Disable always on top to allow it to appear in the taskbar

    def launch_cockblocker(self):
        if self.hitman_location:
            cockblocker_path = os.path.join(self.hitman_location, "cockblocker.exe")
            if os.path.exists(cockblocker_path):
                Popen([cockblocker_path], cwd=self.hitman_location)

def main():
    root = tk.Tk()
    app = DarkModeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
