import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
from pydub import AudioSegment
import subprocess

# Global toggle for Video-to-Audio conversions
VTAToggle = False

# Prevent PIL from throwing DecompressionBombError for very large images
Image.MAX_IMAGE_PIXELS = None

class FileConverterApp:
    def __init__(self, root):
        """
        Initialize the main application window and menu.
        Sets up the GUI layout, frames, and initial state.
        """
        self.root = root
        self.root.title("File Converter App")
        self.root.geometry("400x500")

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu with converter options
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Image Converter", command=self.show_image_converter)
        self.file_menu.add_command(label="Audio Converter", command=self.show_audio_converter)
        self.file_menu.add_command(label="Video Converter", command=self.show_video_converter)
        self.file_menu.add_command(label="Video to Audio Converter", command=self.show_audio_to_video_converter)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Frame that holds all converter widgets dynamically
        self.converter_frame = ttk.Frame(root)
        self.converter_frame.pack()

        # GUI components placeholders
        self.input_listbox = None
        self.output_listbox = None
        self.selected_files_listbox = None
        self.select_file_button = None
        self.select_directory_button = None
        self.convert_button = None

        # State variables
        self.selected_input_files = []
        self.selected_output_format = None

    def clear_frame(self):
        """Clear all widgets from the converter frame."""
        for widget in self.converter_frame.winfo_children():
            widget.destroy()

    # ----------------- Converter type screens -----------------
    def show_video_converter(self):
        """Show UI for video conversion."""
        self.clear_frame()
        input_formats = ['mp4', 'mkv', 'mov', 'avi', 'flv', 'webm', 'wmv']
        output_formats = ['mp4', 'mkv', 'mov', 'avi', 'flv', 'webm', 'wmv']
        self.create_converter_ui(input_formats, output_formats)

    def show_image_converter(self):
        """Show UI for image conversion."""
        self.clear_frame()
        input_formats = ['jpg', 'jpeg', 'png', 'gif', 'tga', 'ico', 'webp', 'dds', 'bmp', 'heif', 'svg']
        output_formats = ['jpg', 'jpeg', 'png', 'gif', 'tga', 'ico', 'webp', 'dds', 'bmp', 'heif', 'svg']
        self.create_converter_ui(input_formats, output_formats)

    def show_audio_converter(self):
        """Show UI for audio conversion."""
        self.clear_frame()
        input_formats = ['mp3', 'wav', 'ogg', 'flac', 'acc', 'm4a', 'wma']
        output_formats = ['mp3', 'wav', 'ogg', 'flac', 'acc', 'm4a', 'wma']
        self.create_converter_ui(input_formats, output_formats)

    def show_audio_to_video_converter(self):
        """
        Show UI for extracting audio from video files.
        Sets the global VTAToggle to True to indicate special conversion.
        """
        global VTAToggle
        self.clear_frame()
        input_formats = ['mp4', 'mkv', 'mov', 'avi', 'flv', 'webm', 'wmv']
        output_formats = ['mp3', 'wav', 'ogg', 'flac', 'acc', 'm4a', 'wma']
        self.create_converter_ui(input_formats, output_formats)
        VTAToggle = True

    # ----------------- Converter UI -----------------
    def create_converter_ui(self, input_formats, output_formats):
        """
        Dynamically create the GUI for input/output selection,
        file selection, and conversion buttons.
        """
        if input_formats is None:
            input_formats = []
        if output_formats is None:
            output_formats = []

        # Frames for layout
        input_output_frame = ttk.Frame(self.converter_frame)
        input_output_frame.pack(side=tk.TOP, padx=5, pady=5)
        button1_frame = ttk.Frame(self.converter_frame)
        button1_frame.pack(side=tk.TOP, padx=5, pady=5)
        file_frame = ttk.Frame(self.converter_frame)
        file_frame.pack(side=tk.TOP, padx=5, pady=5)
        button2_frame = ttk.Frame(self.converter_frame)
        button2_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Labels for input/output formats
        input_label = tk.Label(input_output_frame, text="Select Input File Types")
        input_label.grid(row=0, column=0, padx=(0, 5))
        output_label = tk.Label(input_output_frame, text="Select Output File Types")
        output_label.grid(row=0, column=1, padx=(0, 5))

        # Listboxes for selecting input/output formats
        self.input_listbox = tk.Listbox(input_output_frame, selectmode=tk.MULTIPLE, exportselection=False)
        for item in input_formats:
            self.input_listbox.insert(tk.END, item)
        self.input_listbox.grid(row=1, column=0, padx=(0, 5))

        self.output_listbox = tk.Listbox(input_output_frame, selectmode=tk.SINGLE, exportselection=False)
        for item in output_formats:
            self.output_listbox.insert(tk.END, item)
        self.output_listbox.grid(row=1, column=1)

        # File selection buttons
        self.select_file_button = ttk.Button(button1_frame, text="Select a file", command=self.select_input_files)
        self.select_file_button.grid(row=2, column=0, pady=(5, 0))
        self.select_directory_button = ttk.Button(button1_frame, text="Select a directory", command=self.select_input_directory)
        self.select_directory_button.grid(row=2, column=1, pady=(5, 0))

        # Files to convert listbox
        files_to_convert_label = tk.Label(file_frame, text="Files to Convert")
        files_to_convert_label.pack(pady=(5, 0), padx=(0, 5))
        self.selected_files_listbox = tk.Listbox(file_frame)
        self.selected_files_listbox.pack(pady=(5, 0), padx=(0, 5))

        # Convert and clear buttons
        self.convert_button = ttk.Button(button2_frame, text="Convert", command=self.convert_images)
        self.convert_button.grid(row=5, column=0, pady=(1, 0))
        self.clear_files_button = ttk.Button(button2_frame, text="Clear Files", command=self.clear_selected_files)
        self.clear_files_button.grid(row=5, column=1, pady=(1, 0))

    # ----------------- File selection -----------------
    def clear_selected_files(self):
        """Clear all files from the selected files listbox."""
        try:
            self.selected_files_listbox.delete(0, tk.END)
        except Exception as e:
            print(f"Error clearing selected files: {e}")

    def select_input_files(self):
        """
        Open a file dialog to select multiple input files
        matching the selected input formats.
        """
        try:
            selected_input = self.input_listbox.curselection()
            if selected_input:
                self.selected_input_files = [self.input_listbox.get(idx) for idx in selected_input]
                file_dialog_types = [("Allowed Input Types", " ".join([f"*.{ext}" for ext in self.selected_input_files]))]
                file_paths = filedialog.askopenfilenames(
                    title="Select Input Files",
                    filetypes=file_dialog_types
                )
                self.selected_files_listbox.delete(0, tk.END)
                for file_path in file_paths:
                    self.selected_files_listbox.insert(tk.END, file_path)
        except Exception as e:
            print(f"Error selecting input files: {e}")

    def select_input_directory(self):
        """
        Open a directory selection dialog.
        Adds all files in the directory matching the selected input formats.
        """
        try:
            selected_directory = filedialog.askdirectory(title="Select Input Directory")
            if selected_directory:
                file_list = [f for f in os.listdir(selected_directory) if f.endswith(tuple(self.selected_input_files))]
                self.selected_files_listbox.delete(0, tk.END)
                for file_name in file_list:
                    file_path = os.path.join(selected_directory, file_name)
                    self.selected_files_listbox.insert(tk.END, file_path)
        except Exception as e:
            print(f"Error selecting input directory: {e}")

    # ----------------- Conversion -----------------
    def convert_images(self):
        """
        Main conversion function. Determines file type and calls
        the appropriate conversion method.
        """
        global VTAToggle
        try:
            output_format = self.output_listbox.get(self.output_listbox.curselection()[0])
            output_directory = filedialog.askdirectory(title="Select Output Directory")
            if output_format and output_directory:
                for file_path in self.selected_files_listbox.get(0, tk.END):
                    try:
                        if self.selected_input_files[0] in ['jpg','jpeg','png','gif','tga','ico','webp','dds','bmp','heif','svg']:
                            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                            if output_format == 'jpg':
                                self.convert_to_jpg(file_path, output_file_path)
                            else:
                                if os.path.exists(output_file_path):
                                    confirmed = self.confirm_overwrite(output_file_path)
                                    if not confirmed:
                                        continue
                                img = Image.open(file_path)
                                img.save(output_file_path, format=output_format)
                                img.close()
                        elif self.selected_input_files[0] in ['mp3','wav','ogg','flac','acc','m4a','wma']:
                            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                            self.convert_audio(file_path, output_file_path, output_directory, output_format)
                        elif self.selected_input_files[0] in ['mp4','mkv','mov','avi','flv','webm','wmv']:
                            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                            if VTAToggle:
                                self.convert_to_audio(file_path, output_directory, output_format)
                            else:
                                self.convert_to_video(file_path, output_directory, output_format)
                        else:
                            print(f"Unsupported input format: {self.selected_input_files[0]}")
                            self.show_popup("Unsupported Format", f"The selected input format '{self.selected_input_files[0]}' is not supported.")
                    except Exception as e:
                        print(f"Error converting {file_path}: {e}")
                self.show_popup("Conversion Completed", f"Files have been saved to {output_directory}")
        except Exception as e:
            print(f"Error during conversion process: {e}")

    # ----------------- Specific conversions -----------------
    def convert_to_jpg(self, input_path, output_path):
        """Convert any image to JPG while handling overwrite prompts."""
        try:
            if os.path.exists(output_path):
                if not self.confirm_overwrite(output_path):
                    return
            img = Image.open(input_path)
            rgb_img = img.convert("RGB")
            rgb_img.save(output_path, format="JPEG")
            img.close()
        except Exception as e:
            print(f"Error converting {input_path} to JPG: {e}")

    def convert_audio(self, input_path, output_path, output_directory, output_format):
        """Convert audio files using FFmpeg with error handling."""
        try:
            # Build the FFmpeg command depending on input/output formats
            input_ext = os.path.splitext(input_path)[1].lower().replace(".", "")
            output_ext = output_format.lower()
            if input_ext == "mp3" and output_ext == "wav":
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "pcm_s16le", output_path]
            elif input_ext in ["wav","flac"] and output_ext == "mp3":
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "libmp3lame", "-b:a", "320k", output_path]
            elif input_ext == "flac" and output_ext == "wav":
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "pcm_s16le", output_path]
            elif input_ext == "wav" and output_ext == "flac":
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "flac", output_path]
            elif input_ext == "mp3" and output_ext == "mp3":
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "copy", output_path]
            else:
                command = ["ffmpeg", "-y", "-i", input_path, "-c:a", "libmp3lame" if output_ext=="mp3" else "copy", output_path]
            subprocess.run(command)
        except Exception as e:
            print(f"Error converting audio {input_path} to {output_format}: {e}")

    def convert_to_video(self, input_path, output_directory, output_format):
        """Convert video files using FFmpeg with hardware acceleration."""
        try:
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}")
            if os.path.exists(output_file_path) and not self.confirm_overwrite(output_file_path):
                return
            subprocess.run(['ffmpeg','-y','-hwaccel','cuda','-i',input_path,
                            '-c:v','hevc_nvenc','-preset','p7','-rc','vbr_hq','-cq','19','-b:v','0',
                            '-c:a','aac','-b:a','320k',output_file_path])
        except Exception as e:
            print(f"Error converting video {input_path}: {e}")

    def convert_to_audio(self, input_path, output_directory, output_format):
        """Extract audio from video using FFmpeg."""
        global VTAToggle
        try:
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}")
            if os.path.exists(output_file_path) and not self.confirm_overwrite(output_file_path):
                return
            subprocess.run(['ffmpeg','-y','-i',input_path,'-vn','-acodec','libvorbis','-ac','2','-ab','320k','-ar','48000',output_file_path])
        except Exception as e:
            print(f"Error extracting audio from {input_path}: {e}")
        VTAToggle = False

    # ----------------- Utility -----------------
    def show_popup(self, title, message):
        """Display a message box to the user."""
        try:
            messagebox.showinfo(title, message)
        except Exception as e:
            print(f"Error showing popup: {e}")

    def confirm_overwrite(self, file_path):
        """Ask the user whether to overwrite an existing file."""
        try:
            return messagebox.askyesno("File Already Exists", f"A file named '{os.path.basename(file_path)}' already exists.\nDo you want to overwrite it?")
        except Exception as e:
            print(f"Error showing overwrite confirmation: {e}")
            return False

if __name__ == "__main__":
    # Initialize Tkinter app
    try:
        root = tk.Tk()
        app = FileConverterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error starting the application: {e}")