import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

class InfiCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Infi Code Editor")
        self.root.geometry("1000x750")
        
        # UI Modern Styling Hex Codes
        self.bg_color = "#1e1e1e"
        self.sidebar_color = "#252526"
        self.text_color = "#d4d4d4"
        self.btn_color = "#0e639c"
        self.terminal_bg = "#121212"
        self.terminal_fg = "#00ff00"
        self.line_num_bg = "#1e1e1e"
        self.line_num_fg = "#858585"

        self.current_filepath = None

        self.root.configure(bg=self.bg_color)
        
        # --- Top Menu Action Control Panel ---
        self.control_bar = tk.Frame(self.root, bg=self.sidebar_color, height=45)
        self.control_bar.pack(fill=tk.X, side=tk.TOP)
        
        self.btn_open = tk.Button(self.control_bar, text="📂 Open File", command=self.open_file, bg=self.sidebar_color, fg=self.text_color, borderwidth=0, padx=12, pady=6, activebackground="#3c3c3c", activeforeground="white")
        self.btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save = tk.Button(self.control_bar, text="💾 Save File", command=self.save_file, bg=self.sidebar_color, fg=self.text_color, borderwidth=0, padx=12, pady=6, activebackground="#3c3c3c", activeforeground="white")
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_run = tk.Button(self.control_bar, text="▶ Run Code", command=self.run_code, bg=self.btn_color, fg="white", borderwidth=0, padx=18, pady=6, font=("Segoe UI", 10, "bold"), activebackground="#1177bb")
        self.btn_run.pack(side=tk.LEFT, padx=25, pady=5)

        # --- Code Input Frame (Line Numbers + Text Box) ---
        self.editor_container = tk.Frame(self.root, bg=self.bg_color)
        self.editor_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Line Number Gutter Display Canvas
        self.line_numbers = tk.Canvas(self.editor_container, width=45, bg=self.line_num_bg, bd=0, highlightthickness=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Y Scrollbar setup
        self.scrollbar_y = tk.Scrollbar(self.editor_container)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Editor Code Box Input Element
        self.code_input = tk.Text(self.editor_container, wrap=tk.NONE, bg=self.bg_color, fg=self.text_color, insertbackground="white", font=("Consolas", 12), yscrollcommand=self.scrollbar_y.set, borderwidth=0, highlightthickness=0)
        self.code_input.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5)
        
        self.scrollbar_y.config(command=self.on_scrollbar_scroll)
        self.code_input.config(yscrollcommand=self.scrollbar_y.set)

        # Event listeners to update the gutter line count display dynamically
        self.code_input.bind("<KeyRelease>", self.update_line_numbers)
        self.code_input.bind("<MouseWheel>", self.update_line_numbers)
        self.code_input.bind("<Button-1>", self.update_line_numbers)

        # --- Bottom Workspace Process Outputs Console Logs Window ---
        self.terminal_label = tk.Label(self.root, text=" Build Messages & Runtime Logs:", anchor="w", bg=self.sidebar_color, fg=self.text_color, font=("Segoe UI", 9), pady=4)
        self.terminal_label.pack(fill=tk.X)

        self.terminal_output = tk.Text(self.root, height=14, bg=self.terminal_bg, fg=self.terminal_fg, font=("Consolas", 11), state=tk.DISABLED, borderwidth=0, highlightthickness=0, padx=10, pady=8)
        self.terminal_output.pack(fill=tk.X, side=tk.BOTTOM)

        # Initial layout render call setup
        self.update_line_numbers()

    def on_scrollbar_scroll(self, *args):
        """Ensures that line numbers stay perfectly in sync during scrollbar actions."""
        self.code_input.yview(*args)
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        """Calculates internal row elements and updates the gutter column coordinate text blocks."""
        self.line_numbers.delete("all")
        i = self.code_input.index("@0,0")
        while True:
            dline = self.code_input.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(35, y, anchor="ne", text=linenum, fill=self.line_num_fg, font=("Consolas", 11))
            i = self.code_input.index(f"{i}+1line")

    def log_message(self, message):
        """Clears and appends text back straight inside UI terminal display log viewer panel."""
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.delete("1.0", tk.END)
        self.terminal_output.insert(tk.END, message)
        self.terminal_output.config(state=tk.DISABLED)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Infi Script Language Automation", "*.infi"), ("All Files", "*.*")])
        if path:
            self.current_filepath = path
            with open(path, "r") as f:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, f.read())
            self.root.title(f"Infi Code Editor - {os.path.basename(path)}")
            self.update_line_numbers()

    def save_file(self):
        if not self.current_filepath:
            path = filedialog.asksaveasfilename(defaultextension=".infi", filetypes=[("Infi Script Language Automation", "*.infi")])
            if not path:
                return
            self.current_filepath = path
            
        with open(self.current_filepath, "w") as f:
            f.write(self.code_input.get("1.0", tk.END).strip())
        self.root.title(f"Infi Code Editor - {os.path.basename(self.current_filepath)}")

    def run_code(self):
        """Compiles open source file utilizing the local relative paths inside the project structure."""
        # Checkpoint auto save execution safeguard
        if not self.current_filepath:
            self.save_file()
            if not self.current_filepath:
                return
        else:
            with open(self.current_filepath, "w") as f:
                f.write(self.code_input.get("1.0", tk.END).strip())

        self.log_message("[System Message] Saving environment buffers...\nExecuting local build process chains...\n")

        # Resolve dynamic base directories to support both raw execution and frozen PyInstaller deployment
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
            working_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            working_dir = base_dir
        
        # Path tracking mapped exactly to your folder names: 'gcc' and 'compiler'
        gcc_bin_dir = os.path.abspath(os.path.join(base_dir, "..", "gcc", "bin"))
        compiler_script = os.path.join(base_dir, "compiler", "infi.py")

        # Inject local portable GCC right into system environment parameters array
        env = os.environ.copy()
        env["PATH"] = gcc_bin_dir + os.pathsep + env.get("PATH", "")

        try:
            # Process backend compilation task stream captures 
            process = subprocess.run(
                ["python", compiler_script, self.current_filepath],
                capture_output=True,
                text=True,
                env=env,
                cwd=working_dir # Keeps temporary generated files outside the virtual extraction core directory
            )
            
            output_log = process.stdout
            if process.stderr:
                output_log += "\n" + process.stderr
                
            self.log_message(output_log)

        except Exception as e:
            self.log_message(f"[IDE Engine Error] Failed to handle runtime sub-process pipeline:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InfiCodeEditor(root)
    root.mainloop()