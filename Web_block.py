import tkinter as tk
from tkinter import messagebox
import time
import threading
import os

# List of social media websites to block
SOCIAL_MEDIA_SITES = [
    "www.facebook.com",
    "www.instagram.com",
    "www.twitter.com",
    "www.youtube.com",
    "www.reddit.com",
    "www.tiktok.com"
]

# Path to the hosts file
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" 

# IP address to redirect blocked sites to
REDIRECT_IP = "127.0.0.1"

# Global variable to store selected websites
selected_sites = []

def block_websites():
    """Block selected social media websites by modifying the hosts file."""
    try:
        with open(HOSTS_PATH, "r+") as file:
            content = file.read()
            for site in selected_sites:
                if site not in content:
                    file.write(f"{REDIRECT_IP} {site}\n")
        messagebox.showinfo("Success", "Selected social media sites blocked!")
    except PermissionError:
        messagebox.showerror("Error", "Run the program as Administrator!")

def unblock_websites():
    """Unblock all social media websites by removing entries from the hosts file."""
    try:
        with open(HOSTS_PATH, "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(site in line for site in SOCIAL_MEDIA_SITES):
                    file.write(line)
            file.truncate()
        messagebox.showinfo("Success", "All social media sites unblocked!")
    except PermissionError:
        messagebox.showerror("Error", "Run the program as Administrator!")

def start_timer(duration):
    """Start a timer and update the UI countdown."""
    block_websites()
    for remaining in range(duration * 60, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_label.config(text=f"Time Left: {mins:02}:{secs:02}")
        time.sleep(1)
    timer_label.config(text="")  # Clear timer when done
    unblock_websites()
    messagebox.showinfo("Timer Complete", "Social media sites are unblocked!")


def on_start_button_click():
    """Handle the start button click event."""
    global selected_sites
    selected_sites = [site for site, var in site_vars.items() if var.get()]
    if not selected_sites:
        messagebox.showerror("Error", "Please select at least one social media site!")
        return
    try:
        duration = int(duration_entry.get())
        if duration <= 0:
            messagebox.showerror("Error", "Duration must be greater than 0!")
            return
        threading.Thread(target=start_timer, args=(duration,)).start()
        messagebox.showinfo("Timer Started", f"Selected social media will be blocked for {duration} minutes.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# Create the main GUI window
root = tk.Tk()
root.title("Social Media Blocker")
root.geometry("800x600")
timer_label = tk.Label(root, text="", font=("Arial", 12), fg="red", anchor="e")
timer_label.place(relx=0.95, rely=0.05, anchor="ne")  # Places timer in the top-right corner


# Add widgets
tk.Label(root, text="Select social media sites to block:", font=("Arial", 12, "bold")).pack(pady=5)


# Create checkboxes for each social media site
site_vars = {site: tk.BooleanVar() for site in SOCIAL_MEDIA_SITES}
for site in SOCIAL_MEDIA_SITES:
    tk.Checkbutton(root, text=site, variable=site_vars[site], font=("Arial", 10)).pack(anchor="w", padx=10)



tk.Label(root, text="Enter duration (in minutes):", font=("Arial", 12, "bold")).pack(pady=5)
duration_entry = tk.Entry(root, font=("Arial", 12), width=10)
duration_entry.pack(pady=10)
start_button = tk.Button(root, text="Start Blocking", command=on_start_button_click, font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white")
start_button.pack(pady=10)
# Run the GUI
root.mainloop()
