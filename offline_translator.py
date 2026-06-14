import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os

# Import offline translation engine
try:
    import argostranslate.package
    import argostranslate.translate
except ImportError:
    pass

class OfflineTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline English to Hindi Translator")
        self.root.geometry("800x600")
        self.root.minsize(650, 500)
        
        self.model_loaded = False
        
        self.create_widgets()
        
        # Start core engine initialization in a background thread to keep GUI responsive
        threading.Thread(target=self.initialize_translation_engine, daemon=True).start()

    def create_widgets(self):
        # Main Layout container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # --- English Input ---
        lbl_input = ttk.Label(main_frame, text="English Source Text:", font=('Segoe UI', 10, 'bold'))
        lbl_input.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.txt_input = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=('Segoe UI', 11), height=6)
        self.txt_input.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # --- Middle Action Control Strip ---
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        self.btn_translate = ttk.Button(control_frame, text="Translate Offline ➔", command=self.trigger_translation, state=tk.DISABLED)
        self.btn_translate.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_clear = ttk.Button(control_frame, text="Clear", command=self.clear_text)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        self.btn_copy = ttk.Button(control_frame, text="Copy Result", command=self.copy_to_clipboard)
        self.btn_copy.pack(side=tk.RIGHT, padx=5)

        # --- Hindi Output ---
        lbl_output = ttk.Label(main_frame, text="Hindi Translation Output:", font=('Segoe UI', 10, 'bold'))
        lbl_output.grid(row=3, column=0, sticky="w", pady=(10, 5))
        
        self.txt_output = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=('Mangal', 13), height=6)
        self.txt_output.grid(row=4, column=0, sticky="nsew", pady=(0, 5))
        
        # --- Status Indicator ---
        self.lbl_status = ttk.Label(main_frame, text=" Status: Booting core systems...", relief=tk.SUNKEN, anchor=tk.W, font=('Segoe UI', 9, 'italic'))
        self.lbl_status.grid(row=5, column=0, sticky="ew", pady=(10, 0))

    def update_status(self, text):
        self.lbl_status.config(text=f" Status: {text}")

    def initialize_translation_engine(self):
        """Downloads/Installs the local translation model files on the first boot."""
        try:
            self.update_status("Checking local language packages...")
            
            from_code = "en"
            to_code = "hi"

            # Check if English-to-Hindi is already installed locally
            installed_packages = argostranslate.package.get_installed_packages()
            has_pack = any(p.from_code == from_code and p.to_code == to_code for p in installed_packages)

            if not has_pack:
                self.update_status("First-time setup: Downloading offline translation pairs (requires internet once)...")
                argostranslate.package.update_package_index()
                available_packages = argostranslate.package.get_available_packages()
                
                # Locate English to Hindi pair
                package_to_install = next(
                    filter(
                        lambda x: x.from_code == from_code and x.to_code == to_code,
                        available_packages
                    ), None
                )
                
                if package_to_install:
                    argostranslate.package.install_from_path(package_to_install.download())
                else:
                    raise Exception("Could not find English to Hindi translation payload in package repository index.")

            self.model_loaded = True
            self.btn_translate.config(state=tk.NORMAL)
            self.update_status("Ready (Completely Offline Mode Active)")
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to load language packs:\n{str(e)}\n\nMake sure you are connected to the internet on the *very first boot* to download the language files.")
            self.update_status("Engine Initialization Failure")

    def trigger_translation(self):
        """Dispatches the translation parsing process into a thread to prevent interface freeze."""
        source_text = self.txt_input.get("1.0", tk.END).strip()
        if not source_text:
            return
            
        self.update_status("Translating meaning locally...")
        self.btn_translate.config(state=tk.DISABLED)
        
        threading.Thread(target=self.process_translation, args=(source_text,), daemon=True).start()

    def process_translation(self, text):
        try:
            # Perform direct local semantic translation evaluation
            translated_text = argostranslate.translate.translate(text, "en", "hi")
            
            # Send content back into the main GUI pipeline thread safely
            self.root.after(0, self.display_result, translated_text)
        except Exception as e:
            self.root.after(0, self.handle_error, str(e))

    def display_result(self, result):
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, result)
        self.btn_translate.config(state=tk.NORMAL)
        self.update_status("Translation Complete")

    def handle_error(self, error_msg):
        messagebox.showerror("Translation Process Error", f"An internal error occurred:\n{error_msg}")
        self.btn_translate.config(state=tk.NORMAL)
        self.update_status("Ready")

    def clear_text(self):
        self.txt_input.delete("1.0", tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.update_status("Ready")

    def copy_to_clipboard(self):
        output = self.txt_output.get("1.0", tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            self.update_status("Copied successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineTranslatorApp(root)
    root.mainloop()