import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import webbrowser
from threading import Thread
import platform
import os


class WarpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WARP GUI - Unoffcial")
        self.root.geometry("500x700")
        self.root.resizable(False, False)

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        self.create_header()

        # Status panel
        self.create_status_panel()

        # Connection controls
        self.create_connection_controls()

        # Registration management
        self.create_registration_panel()

        # Log output
        self.create_log_panel()

        # Initial status check
        self.check_warp_status()

        # Footer info panel
        self.create_footer_panel()

    def create_footer_panel(self):
        """Create centered footer with project info and GitHub link"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))

        # Centered info text
        info_text = "WARP GUI - Unofficial v1.0"
        info_label = ttk.Label(
            footer_frame, text=info_text, font=("Segoe UI", 8), foreground="gray"
        )
        info_label.pack(pady=(2, 0))  # padding top and no bottom

        # GitHub link (also centered)
        github_link = ttk.Label(
            footer_frame,
            text="GitHub Repository",
            font=("Segoe UI", 8, "underline"),
            foreground="blue",
            cursor="hand2",
        )
        github_link.pack(pady=(0, 5))  # padding bottom

        github_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://github.com/yourusername/warp-gui"),
        )

    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 9))
        self.style.configure(
            "TLabelframe", background="#f5f5f5", font=("Segoe UI", 10, "bold")
        )
        self.style.configure("TButton", font=("Segoe UI", 9), padding=6)
        self.style.configure("Green.TButton", foreground="white", background="#4CAF50")
        self.style.configure("Red.TButton", foreground="white", background="#F44336")
        self.style.configure("Blue.TButton", foreground="white", background="#2196F3")
        self.style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"))
        self.style.map("Green.TButton", background=[("active", "#45a049")])
        self.style.map("Red.TButton", background=[("active", "#d32f2f")])
        self.style.map("Blue.TButton", background=[("active", "#1976D2")])

    def create_header(self):
        """Create the header section with title and install button"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title_label = ttk.Label(
            header_frame,
            text="Cloudflare Warp Manager",
            font=("Segoe UI", 12, "bold"),
            background="#f5f5f5",
        )
        title_label.pack(side=tk.LEFT)

        install_btn = ttk.Button(
            header_frame,
            text="Install Warp (Linux)",
            command=self.open_install_page,
            style="Blue.TButton",
        )
        install_btn.pack(side=tk.RIGHT)

    def create_status_panel(self):
        """Create the connection status panel"""

        # Use the custom style for LabelFrame
        status_frame = ttk.LabelFrame(
            self.main_frame, text="Connection Status", style="Status.TLabelframe"
        )
        status_frame.pack(fill=tk.X, pady=5)

        self.status_icon = tk.Label(
            status_frame, text="🔴", font=("Segoe UI", 24), background="#3b1d0b"
        )
        self.status_icon.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(
            status_frame, text="Checking Warp status...", style="Status.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.account_label = ttk.Label(
            status_frame, text="Account: Unknown", style="Status.TLabel"
        )
        self.account_label.pack(side=tk.RIGHT, padx=10)

    def create_connection_controls(self):
        """Create connection control buttons"""
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.connect_btn = ttk.Button(
            btn_frame,
            text="Connect",
            command=self.connect_warp,
            style="Green.TButton",
            state=tk.DISABLED,
        )
        self.connect_btn.pack(side=tk.LEFT, expand=True, padx=5)

        self.disconnect_btn = ttk.Button(
            btn_frame,
            text="Disconnect",
            command=self.disconnect_warp,
            style="Red.TButton",
            state=tk.DISABLED,
        )
        self.disconnect_btn.pack(side=tk.LEFT, expand=True, padx=5)

        refresh_btn = ttk.Button(
            btn_frame, text="Refresh Status", command=self.check_warp_status
        )
        refresh_btn.pack(side=tk.LEFT, expand=True, padx=5)

    def create_registration_panel(self):
        """Create registration management panel"""
        reg_frame = ttk.LabelFrame(self.main_frame, text="Registration Management")
        reg_frame.pack(fill=tk.X, pady=5)

        # First row of buttons
        row1 = ttk.Frame(reg_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Button(
            row1,
            text="Show Registration",
            command=lambda: self.run_command("warp-cli registration show"),
        ).pack(side=tk.LEFT, expand=True, padx=2)

        ttk.Button(
            row1,
            text="New Registration",
            command=lambda: self.run_command("warp-cli registration new"),
        ).pack(side=tk.LEFT, expand=True, padx=2)

        ttk.Button(
            row1,
            text="Delete Registration",
            command=lambda: self.run_command("warp-cli registration delete"),
        ).pack(side=tk.LEFT, expand=True, padx=2)

        # Second row of buttons
        row2 = ttk.Frame(reg_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Button(
            row2,
            text="Organization Info",
            command=lambda: self.run_command("warp-cli registration organization"),
        ).pack(side=tk.LEFT, expand=True, padx=2)

        ttk.Button(
            row2,
            text="List Devices",
            command=lambda: self.run_command("warp-cli registration devices"),
        ).pack(side=tk.LEFT, expand=True, padx=2)

        ttk.Button(row2, text="Update License", command=self.update_license).pack(
            side=tk.LEFT, expand=True, padx=2
        )

    def create_log_panel(self):
        """Create the log output panel"""
        log_frame = ttk.LabelFrame(self.main_frame, text="Command Output")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.log_text = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, font=("Consolas", 9), height=12
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

        # Add clear button
        btn_frame = ttk.Frame(log_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log).pack(
            side=tk.RIGHT
        )

    def open_install_page(self):
        """Open the Cloudflare Warp download page"""
        webbrowser.open("https://pkg.cloudflareclient.com")

    def check_warp_status(self):
        """Check and update the current Warp status"""

        def run_check():
            self.log_message("Checking Warp status...")

            # Check if warp-cli is installed
            if not self.is_warp_installed():
                self.update_status("Warp CLI not installed", "🔴")
                self.connect_btn.config(state=tk.DISABLED)
                self.disconnect_btn.config(state=tk.DISABLED)
                self.log_message(
                    "Error: warp-cli not found. Please install Cloudflare Warp."
                )
                return

            # Check connection status
            result = self.run_command("warp-cli status", show_output=False)
            if "Connected" in result:
                self.update_status("Connected", "🟢")
                self.connect_btn.config(state=tk.DISABLED)
                self.disconnect_btn.config(state=tk.NORMAL)
            elif "Disconnected" in result:
                self.update_status("Disconnected", "🔴")
                self.connect_btn.config(state=tk.NORMAL)
                self.disconnect_btn.config(state=tk.DISABLED)
            else:
                self.update_status("Status unknown", "🟠")

            # Check registration status
            reg_result = self.run_command(
                "warp-cli registration show", show_output=False
            )
            if "Missing registration" in reg_result:
                self.account_label.config(text="Account: Not registered")
            else:
                self.account_label.config(text=f"{reg_result.splitlines()[0]}")

        Thread(target=run_check, daemon=True).start()

    def is_warp_installed(self):
        """Check if warp-cli is installed"""
        try:
            subprocess.run(
                ["warp-cli", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except:
            return False

    def connect_warp(self):
        """Connect to Warp service"""

        def run_connect():
            self.run_command("warp-cli connect")
            self.root.after(1000, self.check_warp_status)

        Thread(target=run_connect, daemon=True).start()

    def disconnect_warp(self):
        """Disconnect from Warp service"""

        def run_disconnect():
            self.run_command("warp-cli disconnect")
            self.root.after(1000, self.check_warp_status)

        Thread(target=run_disconnect, daemon=True).start()

    def update_license(self):
        """Update license key with dialog prompt"""
        license_key = tk.simpledialog.askstring(
            "Update License Key", "Enter your new license key:", parent=self.root
        )
        if license_key:
            self.run_command(f"warp-cli registration license {license_key}")

    def run_command(self, command, show_output=True):
        """Execute a shell command and handle output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output = result.stdout.strip() or result.stderr.strip()

            if show_output:
                self.log_message(f"> {command}\n{output}")

            return output

        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {command}\nError: {e.stderr.strip()}"
            if show_output:
                self.log_message(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            if show_output:
                self.log_message(error_msg)
            return error_msg

    def update_status(self, text, icon):
        """Update the status label and icon"""
        self.status_label.config(text=text)
        self.status_icon.config(text=icon)

    def log_message(self, message):
        """Add a message to the log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        """Clear the log output"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = WarpGUI(root)
    root.mainloop()
