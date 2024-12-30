import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import cv2
import os

def create_short_videos(video_path, output_folder, duration, caption=None, update_ui=None):
    try:
        # Open the video file
        video = cv2.VideoCapture(video_path)
        
        # Get the video properties
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        total_duration = total_frames // fps

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Calculate the number of short clips
        num_clips = total_duration // duration

        if update_ui:
            update_ui(f"Total video duration: {total_duration} seconds")
            update_ui(f"Number of {duration}-second clips to be created: {num_clips}")

        for i in range(num_clips):
            start_time = i * duration
            end_time = start_time + duration

            start_frame = start_time * fps
            end_frame = end_time * fps

            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            out_path = os.path.join(output_folder, f"short_clip_{i + 1}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            out = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))

            frame_count = 0
            while frame_count < (end_frame - start_frame):
                ret, frame = video.read()
                if not ret:
                    break

                if caption:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_color = (255, 255, 255)
                    thickness = 2
                    text_size = cv2.getTextSize(caption, font, font_scale, thickness)[0]
                    text_x = (frame.shape[1] - text_size[0]) // 2
                    text_y = frame.shape[0] - 10
                    cv2.putText(frame, caption, (text_x, text_y), font, font_scale, font_color, thickness)

                out.write(frame)
                frame_count += 1

            out.release()
            if update_ui:
                update_ui(f"Saved: {out_path}")

        if update_ui:
            update_ui("All short videos have been created!")

    except Exception as e:
        if update_ui:
            update_ui(f"Error: {e}")

    finally:
        video.release()

def browse_video():
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    video_path_var.set(file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder_path)

def start_processing():
    video_path = video_path_var.get()
    output_folder = output_folder_var.get()
    duration = duration_var.get()
    caption = caption_var.get()

    if not video_path or not output_folder or not duration:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        duration = int(duration)
        show_output_window(video_path, output_folder, duration, caption)
    except ValueError:
        messagebox.showerror("Error", "Duration must be a valid integer.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_output_window(video_path, output_folder, duration, caption):
    output_window = Toplevel(root)
    output_window.title("Processing Output")
    output_window.geometry("400x300")

    output_text = tk.Text(output_window, wrap=tk.WORD)
    output_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def update_ui(message):
        output_text.insert(tk.END, message + "\n")
        output_text.see(tk.END)

    output_text.insert(tk.END, "Processing started...\n")
    root.after(100, create_short_videos, video_path, output_folder, duration, caption, update_ui)

# Create the main window
root = tk.Tk()
root.title("Video Shortener")
root.geometry("400x300")

# Variables
video_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
duration_var = tk.StringVar()
caption_var = tk.StringVar()

# UI Elements
tk.Label(root, text="Video Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=video_path_var, width=30).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_video).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=output_folder_var, width=30).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Clip Duration (s):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=duration_var, width=10).grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Caption (Optional):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=caption_var, width=30).grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Start", command=start_processing).grid(row=4, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
