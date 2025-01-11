import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinterdnd2 as tkdnd
import main  # Assuming main.py is in the same directory
import sys
import threading
import os  # For `resource_path` and `os.path.normpath`
import platform #For playing video

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # This will not be used in one-folder mode but keep it for consistency
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class FootballAnalysisGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("Football Analysis Tool")
        master.geometry("600x400")

        # Create and configure main frame
        main_frame = ttk.Frame(master, padding="20", style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame with select button and drop zone
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        # Create the Select Video button
        self.input_button = ttk.Button(input_frame, text="Select Input Video", command=self.select_input)
        self.input_button.pack(side=tk.LEFT, padx=(0, 10))

        # Create the drag and drop zone
        self.drop_zone = tk.Label(input_frame, text="Drag and Drop Video Here", width=30, height=5,
                                  relief="solid", borderwidth=1, background="#f0f0f0", anchor="center")
        self.drop_zone.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Enable drag and drop for the drop zone
        self.drop_zone.drop_target_register(tkdnd.DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.drop_file)

        # Input path label
        self.input_path = tk.StringVar()
        self.input_label = ttk.Label(input_frame, textvariable=self.input_path, wraplength=400)
        self.input_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Process and Play buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.process_button = ttk.Button(button_frame, text="Generate Output Video", command=self.start_processing, state=tk.DISABLED)
        self.process_button.grid(row=0, column=0, padx=10)

        self.play_button = ttk.Button(button_frame, text="Play Generated Video", command=self.play_video, state=tk.DISABLED)
        self.play_button.grid(row=0, column=1, padx=10)

        # Progress bar and status label
        self.progress = ttk.Progressbar(main_frame, length=500, mode='indeterminate')
        self.progress.pack(pady=10)

        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(pady=10)

        # Log window with scrollbar
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.log_window = tk.Text(log_frame, height=10, width=70, state='disabled', font=('Consolas', 10), bg='#f0f0f0', fg='#333333')
        self.log_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_window.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_window['yscrollcommand'] = scrollbar.set

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        style.configure('TLabel', font=('Arial', 11))
        style.configure("TProgressbar", thickness=25)
        style.configure('Main.TFrame', background='#e6e6e6')

    def start_processing(self):
        """Start video processing in a separate thread."""
        self.process_thread = threading.Thread(target=self.process_video)
        self.process_thread.start()

    def drop_file(self, event):
        file_path = event.data.strip('{}')  # Remove curly braces if present
        if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.input_path.set(f"Selected video: {file_path}")
            self.process_button['state'] = tk.NORMAL
            self.update_log(f"Video file dropped: {file_path}")
        else:
            messagebox.showerror("Error", "Please drop a valid video file.")
            self.update_log("Invalid file dropped")

    def select_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.input_path.set(f"Selected video: {file_path}")
            self.process_button['state'] = tk.NORMAL

    def process_video(self):
        input_path = self.input_path.get().split(": ")[1]
        video_name = input_path.split('/')[-1].split('.')[0]
        output_path = f'Output_Videos/{video_name}_output.avi'
        output_path = resource_path(output_path) #Use resource path here
        self.progress.start()
        self.update_log("Processing video...")
        try:
            result = main.process_video(input_path, output_path)
            if result is not None:
                for message in result:
                    self.update_log(message)
            else:
                self.update_log("Processing completed, but no messages were returned.")
            self.update_log("Video processed successfully!")
            self.show_success_message(output_path)
        except Exception as e:
            self.update_log(f"Error occurred during processing: {str(e)}")
            self.show_error_message(str(e))
            print(f"Error: {str(e)}", file=sys.stderr)
        finally:
            self.progress.stop()
            self.update_play_button(output_path)

    def show_success_message(self, output_path):
        self.output_path = output_path
        self.master.after(0, lambda: messagebox.showinfo("Success", f"Output video generated successfully at {output_path}"))
        self.master.after(0, lambda: self.play_button.config(state=tk.NORMAL))

    def show_error_message(self, message):
        """Show an error message."""
        self.master.after(0, lambda: messagebox.showerror("Error", message))

    def update_play_button(self, output_path):
        """Update play button state after processing."""
        self.master.after(0, lambda: self.play_button.config(state=tk.NORMAL))

    def play_video(self):
        output_path = resource_path(self.output_path) #Use resource path here
        if os.path.exists(output_path):
            if platform.system() == 'Windows':
                os.startfile(output_path)
            elif platform.system() == 'Darwin':  # macOS
                import subprocess
                subprocess.call(('open', output_path))
            else:  # Linux and other Unix-like
                import subprocess
                subprocess.call(('xdg-open', output_path))

            self.update_log("Played generated output video!")
        else:
            self.show_error_message(f"Output video not found at {output_path}")

    def update_log(self, message):
        self.log_window.config(state='normal')
        self.log_window.insert(tk.END, message + '\n')
        self.log_window.see(tk.END)
        self.log_window.config(state='disabled')
        self.master.update_idletasks()

# Initialize the main window
root = tkdnd.TkinterDnD.Tk()
root.title("Football Analysis Tool")
root.geometry("600x400")

# Initialize the GUI
gui = FootballAnalysisGUI(root)
root.mainloop()