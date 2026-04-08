"""
Archive Password Cracker GUI
A simple tool to identify passwords in RAR and ZIP files.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import threading
import os
import tempfile
import shutil

# Try to import rarfile for RAR support
try:
    import rarfile
    RARFILE_AVAILABLE = True
except ImportError:
    RARFILE_AVAILABLE = False


class PasswordCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Archive Password Cracker")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.archive_file = None
        self.password_file = None
        self.cracking = False
        self.found_password = None
        self.archive_contents = []  # Store extracted archive contents
        self.temp_extract_dir = None  # Temporary extraction directory
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_frame = ttk.Frame(self.root, padding="20")
        title_frame.pack(fill="x")
        
        title_label = ttk.Label(title_frame, text="Archive Password Cracker", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Archive File Selection
        archive_frame = ttk.LabelFrame(self.root, text="Select Archive File", padding="10")
        archive_frame.pack(fill="x", padx=20, pady=10)
        
        self.archive_label = ttk.Label(archive_frame, text="No file selected", 
                                       foreground="gray")
        self.archive_label.pack(side="left", fill="x", expand=True)
        
        archive_btn = ttk.Button(archive_frame, text="Browse", 
                                command=self.select_archive)
        archive_btn.pack(side="right", padx=5)
        
        # Password File Selection
        password_frame = ttk.LabelFrame(self.root, text="Select Password List", padding="10")
        password_frame.pack(fill="x", padx=20, pady=10)
        
        self.password_label = ttk.Label(password_frame, text="No file selected", 
                                        foreground="gray")
        self.password_label.pack(side="left", fill="x", expand=True)
        
        password_btn = ttk.Button(password_frame, text="Browse", 
                                 command=self.select_password_file)
        password_btn.pack(side="right", padx=5)
        
        # Start Button
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="Start Cracking", 
                                   command=self.start_cracking)
        self.start_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                  command=self.stop_cracking, state="disabled")
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, 
                                           maximum=100, mode='indeterminate')
        self.progress_bar.pack(fill="x", padx=20, pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Ready", foreground="blue")
        self.status_label.pack(fill="x", padx=20, pady=5)
        
        # Password Result Display
        password_result_frame = ttk.LabelFrame(self.root, text="Found Password", padding="10")
        password_result_frame.pack(fill="x", padx=20, pady=5)
        
        self.password_result_label = ttk.Label(password_result_frame, text="No password found yet", 
                                              foreground="gray", font=("Courier", 11, "bold"), 
                                              wraplength=500, justify="center")
        self.password_result_label.pack(fill="x")
        
        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="Results", padding="10")
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Results text widget
        self.results_text = tk.Text(results_frame, height=10, width=60, 
                                   state="disabled", wrap="word")
        self.results_text.pack(fill="both", expand=True)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", 
                                 command=self.results_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_text.config(yscrollcommand=scrollbar.set)
        
    def select_archive(self):
        """Select an archive file (RAR or ZIP)"""
        file_types = [("Archive files", "*.rar *.zip"), 
                     ("RAR files", "*.rar"),
                     ("ZIP files", "*.zip"),
                     ("All files", "*.*")]
        
        filename = filedialog.askopenfilename(
            title="Select an archive file",
            filetypes=file_types
        )
        
        if filename:
            self.archive_file = filename
            display_name = os.path.basename(filename)
            self.archive_label.config(text=display_name, foreground="black")
            
    def select_password_file(self):
        """Select a password list file"""
        filename = filedialog.askopenfilename(
            title="Select password list file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            self.password_file = filename
            display_name = os.path.basename(filename)
            self.password_label.config(text=display_name, foreground="black")
            
    def update_results(self, message, result_type="info"):
        """Update results text widget (thread-safe)"""
        # Use after() to ensure GUI updates happen on the main thread
        def _update():
            self.results_text.config(state="normal")
            
            if result_type == "info":
                self.results_text.insert(tk.END, f"ℹ️  {message}\n")
            elif result_type == "success":
                self.results_text.insert(tk.END, f"✓ {message}\n")
                # If it's a password found message, also update the dedicated display
                if "Password found:" in message:
                    password = message.replace("Password found:", "").strip()
                    self.password_result_label.config(text=password, foreground="green")
            elif result_type == "error":
                self.results_text.insert(tk.END, f"✗ {message}\n")
                
            self.results_text.see(tk.END)
            self.results_text.config(state="disabled")
        
        self.root.after(0, _update)
        
    def start_cracking(self):
        """Start the cracking process in a separate thread"""
        if not self.archive_file:
            messagebox.showerror("Error", "Please select an archive file")
            return
            
        if not self.password_file:
            messagebox.showerror("Error", "Please select a password list file")
            return
            
        self.cracking = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Clear previous results
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state="disabled")
        self.password_result_label.config(text="Searching...", foreground="blue")
        self.found_password = None
        
        # Start cracking in a separate thread
        thread = threading.Thread(target=self.crack_password)
        thread.daemon = True
        thread.start()
        
    def stop_cracking(self):
        """Stop the cracking process"""
        self.cracking = False
        self.update_results("Cracking stopped by user", "info")
        self.root.after(0, lambda: self.status_label.config(text="Stopped", foreground="orange"))
        
    def crack_password(self):
        """Attempt to crack the archive password"""
        self.root.after(0, self.progress_bar.start)
        self.root.after(0, lambda: self.status_label.config(text="Cracking in progress...", foreground="blue"))
        
        try:
            # Determine file type
            file_ext = os.path.splitext(self.archive_file)[1].lower()
            
            # Read passwords from file
            try:
                with open(self.password_file, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords = [line.strip() for line in f if line.strip()]
            except Exception as e:
                self.update_results(f"Error reading password file: {e}", "error")
                self.restore_ui()
                return
                
            if not passwords:
                self.update_results("Password list is empty", "error")
                self.restore_ui()
                return
                
            self.update_results(f"Loaded {len(passwords)} passwords", "info")
            self.update_results(f"Testing archive: {os.path.basename(self.archive_file)}", "info")
            self.update_results("", "info")
            
            if file_ext == ".zip":
                self.crack_zip(passwords)
            elif file_ext == ".rar":
                self.crack_rar(passwords)
            else:
                self.update_results(f"Unsupported file format: {file_ext}", "error")
                
        except Exception as e:
            self.update_results(f"Unexpected error: {e}", "error")
            
        finally:
            self.restore_ui()
            
    def crack_zip(self, passwords):
        """Attempt to crack a ZIP file and extract contents"""
        try:
            zf = zipfile.ZipFile(self.archive_file)
        except Exception as e:
            self.update_results(f"Error opening ZIP file: {e}", "error")
            return
            
        if not zf.namelist():
            self.update_results("ZIP file is empty", "error")
            return
            
        test_file = zf.namelist()[0]
        
        for i, password in enumerate(passwords):
            if not self.cracking:
                break
                
            try:
                # Try to read the file with this password
                zf.setpassword(password.encode('utf-8'))
                zf.testzip()
                
                # If we get here, the password is correct
                self.found_password = password
                self.update_results(f"Password found: {password}", "success")
                self.update_results(f"Tested {i + 1} passwords", "info")
                
                # Extract and display contents
                self.extract_and_display_zip(zf, password)
                break
                
            except RuntimeError:
                # Password incorrect, continue
                if (i + 1) % 100 == 0 or i + 1 == len(passwords):
                    self.update_results(f"Tested {i + 1}/{len(passwords)} passwords...", "info")
            except Exception as e:
                self.update_results(f"Error testing password: {e}", "error")
                break
                
        if not self.found_password and self.cracking:
            self.update_results("Password not found in the list", "error")
            
    def crack_rar(self, passwords):
        """Attempt to crack a RAR file and extract contents"""
        if not RARFILE_AVAILABLE:
            self.update_results("The 'rarfile' module is not installed", "error")
            self.update_results("Install it with: pip install rarfile", "info")
            return
            
        try:
            # Open the RAR file to check if it's valid
            rf = rarfile.RarFile(self.archive_file)
            # Get the list of files
            file_list = rf.infolist()
        except rarfile.NotRarFile:
            self.update_results("Error: File is not a valid RAR archive", "error")
            return
        except rarfile.BadRarFile as e:
            self.update_results(f"Error: Cannot read RAR file - {e}", "error")
            return
        except Exception as e:
            self.update_results(f"Error opening RAR file: {e}", "error")
            return
            
        if not file_list:
            self.update_results("RAR file is empty or contains no extractable files", "error")
            return
        
        # Find the first non-directory file for password testing
        test_file = None
        for file_info in file_list:
            if not file_info.is_dir():
                test_file = file_info.filename
                break
        
        if test_file is None:
            self.update_results("RAR file contains only directories", "error")
            return
        
        self.update_results(f"Testing with file: {test_file}", "info")
        
        for i, password in enumerate(passwords):
            if not self.cracking:
                break
            
            # Create a new RarFile instance for each password test
            # This is necessary because rarfile doesn't handle password changes well
            try:
                rf = rarfile.RarFile(self.archive_file)
                rf.setpassword(password)
                
                # Try to read the test file to verify password
                try:
                    data = rf.read(test_file)
                    # If we successfully read the file, password is correct
                    self.found_password = password
                    self.update_results(f"Password found: {password}", "success")
                    self.update_results(f"Tested {i + 1} passwords", "info")
                    
                    # Extract and display contents
                    self.extract_and_display_rar(rf, password)
                    break
                    
                except rarfile.BadRarFile:
                    # Wrong password - continue to next one
                    if (i + 1) % 100 == 0 or i + 1 == len(passwords):
                        self.update_results(f"Tested {i + 1}/{len(passwords)} passwords...", "info")
                        
                except (RuntimeError, OSError) as e:
                    # Typically indicates wrong password or CRC error
                    error_msg = str(e).lower()
                    if "crc" in error_msg or "encrypted" in error_msg or "bad" in error_msg:
                        if (i + 1) % 100 == 0 or i + 1 == len(passwords):
                            self.update_results(f"Tested {i + 1}/{len(passwords)} passwords...", "info")
                    else:
                        self.update_results(f"Error testing password: {e}", "error")
                        break
                        
            except Exception as e:
                self.update_results(f"Error with password '{password}': {e}", "error")
                break
                    
        if not self.found_password and self.cracking:
            self.update_results("Password not found in the list", "error")
            
    def extract_and_display_zip(self, zf, password):
        """Extract ZIP file contents and display them"""
        try:
            # Create a temporary directory for extraction
            if self.temp_extract_dir and os.path.exists(self.temp_extract_dir):
                shutil.rmtree(self.temp_extract_dir)
            
            self.temp_extract_dir = tempfile.mkdtemp(prefix="zip_extract_")
            
            # Extract all files
            zf.setpassword(password.encode('utf-8'))
            zf.extractall(self.temp_extract_dir)
            
            self.update_results("", "info")
            self.update_results("Archive Contents:", "info")
            
            # List and display file contents
            for root, dirs, files in os.walk(self.temp_extract_dir):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, self.temp_extract_dir)
                    
                    try:
                        # Try to read as text
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        self.update_results(f"📄 {rel_path}:", "info")
                        self.update_results(f"   {content}", "info")
                        
                    except Exception as e:
                        self.update_results(f"📦 {rel_path} (binary file)", "info")
                        
        except Exception as e:
            self.update_results(f"Error extracting ZIP contents: {e}", "error")
            
    def extract_and_display_rar(self, rf, password):
        """Extract RAR file contents and display them"""
        try:
            # Create a temporary directory for extraction
            if self.temp_extract_dir and os.path.exists(self.temp_extract_dir):
                shutil.rmtree(self.temp_extract_dir)
            
            self.temp_extract_dir = tempfile.mkdtemp(prefix="rar_extract_")
            
            # Extract all files
            rf.extractall(self.temp_extract_dir, pwd=self.found_password)
            
            self.update_results("", "info")
            self.update_results("Archive Contents:", "info")
            
            # List and display file contents
            for root, dirs, files in os.walk(self.temp_extract_dir):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, self.temp_extract_dir)
                    
                    try:
                        # Try to read as text
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        self.update_results(f"📄 {rel_path}:", "info")
                        self.update_results(f"   {content}", "info")
                        
                    except Exception as e:
                        self.update_results(f"📦 {rel_path} (binary file)", "info")
                        
        except Exception as e:
            self.update_results(f"Error extracting RAR contents: {e}", "error")
            
    def restore_ui(self):
        """Restore UI to normal state (thread-safe)"""
        def _restore():
            self.progress_bar.stop()
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            
            if self.found_password:
                self.status_label.config(text="Password found!", foreground="green")
            else:
                self.status_label.config(text="Cracking completed", foreground="orange")
        
        self.root.after(0, _restore)


def main():
    root = tk.Tk()
    app = PasswordCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
