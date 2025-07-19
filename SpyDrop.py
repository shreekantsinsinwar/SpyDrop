import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

THEME_BG = "#0c0c0c"
THEME_FG = "#00ff00"

class SpyDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpyDrop - Covert File Embedder")
        self.root.geometry("700x500")
        self.root.configure(bg=THEME_BG)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=THEME_BG)
        style.configure("TNotebook.Tab", background=THEME_BG, foreground=THEME_FG)
        style.map("TNotebook.Tab", background=[("selected", THEME_FG)], foreground=[("selected", THEME_BG)])

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.create_embed_tab()
        self.create_extract_tab()
        self.create_help_tab()

    def create_embed_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="🕵️ Embed Payload")

        tk.Label(tab, text="Select Carrier File (Image or PDF)", fg=THEME_FG, bg=THEME_BG).pack(pady=5)
        tk.Button(tab, text="Browse Carrier", command=self.select_carrier, bg="gray").pack()

        tk.Label(tab, text="Select Payload (.zip)", fg=THEME_FG, bg=THEME_BG).pack(pady=5)
        tk.Button(tab, text="Browse Payload", command=self.select_payload, bg="gray").pack()

        tk.Button(tab, text="💣 Embed Spy Payload", command=self.embed_payload, bg="green").pack(pady=20)

        self.carrier_path = None
        self.payload_path = None

    def create_extract_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="🧰 Extract Payload")

        tk.Label(tab, text="Choose Stealth File (Image + ZIP)", fg=THEME_FG, bg=THEME_BG).pack(pady=10)
        tk.Button(tab, text="Browse Stealth File", command=self.select_stealth_file, bg="gray").pack()

        tk.Button(tab, text="🗂 Extract", command=self.extract_payload, bg="green").pack(pady=20)

        self.stealth_file = None

    def create_help_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="📖 How to Use")

        info = """
SpyDrop - Secret Payload Hider

🕵️ Embed Payload:
- Select a cover file (image or PDF)
- Select a .zip file (payload)
- The tool will create a stealth file that looks normal but contains the payload

🧰 Extract Payload:
- Select the stealth file
- Tool will extract the .zip payload

💡 You can even open the stealth file with unzip or 7zip

⚠️ Do not use for malicious purposes
⚠️ Do not email or send these files directly — use secure channels
"""
        tk.Label(tab, text=info, fg=THEME_FG, bg=THEME_BG, justify="left", wraplength=680).pack(padx=10, pady=10)

    def select_carrier(self):
        path = filedialog.askopenfilename(title="Choose Carrier File", filetypes=[("Images and PDFs", "*.jpg *.jpeg *.png *.pdf")])
        if path:
            self.carrier_path = path
            messagebox.showinfo("Selected", f"Carrier: {os.path.basename(path)}")

    def select_payload(self):
        path = filedialog.askopenfilename(title="Choose ZIP Payload", filetypes=[("ZIP Files", "*.zip")])
        if path:
            self.payload_path = path
            messagebox.showinfo("Selected", f"Payload: {os.path.basename(path)}")

    def embed_payload(self):
        if not self.carrier_path or not self.payload_path:
            messagebox.showwarning("Missing", "Please select both carrier and payload files.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".spyfile", title="Save Stealth File As")
        if not save_path:
            return

        try:
            with open(save_path, "wb") as out:
                with open(self.carrier_path, "rb") as c:
                    shutil.copyfileobj(c, out)
                with open(self.payload_path, "rb") as p:
                    shutil.copyfileobj(p, out)
            messagebox.showinfo("Success", f"Spy payload embedded into: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def select_stealth_file(self):
        path = filedialog.askopenfilename(title="Choose Stealth File")
        if path:
            self.stealth_file = path
            messagebox.showinfo("Selected", f"Stealth file: {os.path.basename(path)}")

    def extract_payload(self):
        if not self.stealth_file:
            messagebox.showwarning("Missing", "Please choose a stealth file.")
            return

        out_dir = filedialog.askdirectory(title="Select Output Folder")
        if not out_dir:
            return

        try:
            shutil.unpack_archive(self.stealth_file, out_dir)
            messagebox.showinfo("Extracted", f"Payload extracted to {out_dir}")
        except Exception as e:
            messagebox.showerror("Failed", f"Extraction failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpyDropApp(root)
    root.mainloop()
