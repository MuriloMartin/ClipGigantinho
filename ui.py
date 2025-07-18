import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
from main import get_files_list, save_clip_from_buffer, start_buffering, RTSP_URL, clear_buffer




def main(ffmpeg_proc):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black')

    def refresh_list():
        files = get_files_list()
        listbox.delete(0, tk.END)
        for f in files:
            listbox.insert(tk.END, f)

    def on_key_press(event):
        print(f"Key pressed: {event.keysym}")
        if event.keysym in ("space", "Return"): 
            save_clip_from_buffer()
            refresh_list()
        elif event.keysym == "Escape":
            root.destroy()
            clear_buffer()
            ffmpeg_proc.terminate()
            ffmpeg_proc.wait()

    root.bind("<Key>", on_key_press)

    # === Grid layout ===
    root.grid_columnconfigure(0, weight=1, uniform="group1")
    root.grid_columnconfigure(1, weight=4, uniform="group1")
    root.grid_rowconfigure(0, weight=1)

    # === Right: Video ===
    video_frame = tk.Frame(root, bg='black')
    video_frame.grid(row=0, column=1, sticky='nsew')
    video_label = tk.Label(video_frame, bg='black')
    video_label.place(relx=0.5, rely=0.5, anchor='center')

    # === Left: Controls (utils_frame) ===
    utils_frame = tk.Frame(root, bg='gray20')
    utils_frame.grid(row=0, column=0, sticky='nsew')

    utils_frame.grid_rowconfigure(0, weight=1)
    utils_frame.grid_columnconfigure(0, weight=1)

    listbox = tk.Listbox(utils_frame, bg='gray30', fg='white', bd=2, relief='ridge',
                         font=('Arial', 14))
    listbox.grid(row=0, column=0, sticky='nsew')

    scrollbar = tk.Scrollbar(utils_frame, orient='vertical', command=listbox.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    listbox.config(yscrollcommand=scrollbar.set)

    refresh_list()

    # === OpenCV setup ===
    cap = cv2.VideoCapture(
        RTSP_URL,
        cv2.CAP_FFMPEG
    )
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (960, 540))  # adjust to fit your layout
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

        video_label.after(10, update_video)  # ~30 FPS

    update_video()

    def on_close():
        cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    ffmpeg_proc = start_buffering()
    main(ffmpeg_proc)
