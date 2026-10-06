import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
import re
from db import insert_ips, insert_domains, insert_hashes
from api_pusher import push_ips, push_domains, push_hashes

class ThreatFeedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("THREAT FEED SYSTEM")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='light blue')
        style.configure('TLabel', background='light blue', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('Status.TLabel', font=('Arial', 9), foreground='#333')

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(main_frame, text="THREAT FEED SYSTEM", font=('Arial', 14, 'bold'))
        header.pack(pady=(0, 10))

        input_frame = ttk.LabelFrame(main_frame, text="PASTE IPs/HASHES/DOMAINS HERE", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)

        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD, font=('Consolas', 10))
        self.input_text.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        submit_btn = ttk.Button(button_frame, text="SUBMIT", command=self.process_threats)
        submit_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(button_frame, text="RESET", command=self.reset_input)
        reset_btn.pack(side=tk.LEFT, padx=5)

        status_frame = ttk.LabelFrame(main_frame, text="STATUS MESSAGES", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.status_log = tk.Text(status_frame, height=10, wrap=tk.WORD, font=('Arial', 9), state='disabled', bg='black', fg='white')
        self.status_log.pack(fill=tk.BOTH, expand=True)

        self.input_text.insert(tk.END, "192[.]168[.]1[.]1, malicious.com\n8.8.8.8\na94a8fe5ccb19ba61c4c0873d391e987982fbbd3")

    def reset_input(self):
        self.input_text.delete("1.0", tk.END)
        self.add_status("🔄 Input reset successfully!", "yellow")

    def analyze_threats(self, data):
        cleaned_data = (
            data.replace("[.]", ".")
                .replace("[:]", ".")
                .replace("[dot]", ".")
                .replace("(dot)", ".")
                .replace("(.)", ".")
                .replace("{.}", ".")
        )

        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        hash_pattern = r'\b[a-fA-F0-9]{16,64}\b'

        ips = list(set(re.findall(ip_pattern, cleaned_data)))
        domains = list(set(re.findall(domain_pattern, cleaned_data)))
        hashes = list(set(re.findall(hash_pattern, data)))

        return ips, domains, hashes

    def process_threats(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        if not input_data:
            messagebox.showwarning("Empty Input", "Please paste threat data first")
            return

        self.add_status("🟡 Cleaning data...", "yellow")

        thread = threading.Thread(
            target=self._process_threats_background,
            args=(input_data,),
            daemon=True
        )
        thread.start()

    def _process_threats_background(self, data):
        import time
        time.sleep(1)

        clean_ips, clean_domains, clean_hashes = self.analyze_threats(data)
        self.add_status(f"🟢 {len(clean_ips)} IPs | {len(clean_hashes)} Hashes | {len(clean_domains)} Domains found", "green")
        time.sleep(1)

        self.add_status("🟡 Adding to database...", "yellow")
        try:
            insert_ips(clean_ips)
            insert_domains(clean_domains)
            insert_hashes(clean_hashes)
            self.add_status("🟢 Data saved successfully!", "green")
        except Exception as e:
            self.add_status(f"🔴 Error saving data: {str(e)}", "red")
        time.sleep(1)

        self.show_sectioned_tables(clean_ips, clean_domains, clean_hashes)

        self.add_status("🟡 Pushing to firewall...", "yellow")
        try:
            push_ips(clean_ips)
            push_domains(clean_domains)
            push_hashes(clean_hashes)
            self.add_status("🟢 Data pushed to firewall successfully!", "green")
        except Exception as e:
            self.add_status(f"🔴 API push failed: {str(e)}", "red")

    def show_sectioned_tables(self, ips, domains, hashes):
        popup = tk.Toplevel(self.root)
        popup.title("Cleaned Threats Summary")
        popup.geometry("720x500")

        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def create_section(frame, title, data):
            label = ttk.Label(frame, text=title, font=('Arial', 10, 'bold'))
            label.pack(anchor='w', padx=5, pady=(10, 0))
            tree = ttk.Treeview(frame, columns=("data",), show='headings', height=min(len(data), 10))
            tree.heading("data", text=title)
            tree.column("data", anchor='center', width=650)
            if data:
                for item in data:
                    tree.insert('', tk.END, values=(item,))
            else:
                tree.insert('', tk.END, values=("No data found",))
            tree.pack(fill=tk.X, padx=5, pady=5)

        create_section(scrollable_frame, "IP Addresses", ips)
        create_section(scrollable_frame, "Domains", domains)
        create_section(scrollable_frame, "Hashes", hashes)

    def add_status(self, message, color):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        self.status_log.config(state='normal')
        self.status_log.insert(tk.END, formatted_msg)
        self.status_log.tag_add(color, "end-2l", "end-1c")
        self.status_log.tag_config("yellow", foreground="yellow")
        self.status_log.tag_config("green", foreground="lightgreen")
        self.status_log.tag_config("red", foreground="red")
        self.status_log.see(tk.END)
        self.status_log.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ThreatFeedGUI(root)
    root.mainloop()
