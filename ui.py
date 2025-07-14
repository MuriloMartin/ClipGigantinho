import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

RTSP_URL = "rtsp://admin:elefante123123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    root.bind("<Escape>", lambda e: root.destroy())

    buffering_on = tk.BooleanVar(value=True)

    # === Grid layout ===
    root.grid_columnconfigure(0, weight=1, uniform="group1")
    root.grid_columnconfigure(1, weight=4, uniform="group1")
    root.grid_rowconfigure(0, weight=1)

    # === Right: Video ===
    video_frame = tk.Frame(root, bg='black')
    video_frame.grid(row=0, column=1, sticky='nsew')
    video_label = tk.Label(video_frame, bg='black')
    video_label.place(relx=0.5, rely=0.5, anchor='center')

    # === Left: Controls ===
    utils_frame = tk.Frame(root, bg='gray20')
    utils_frame.grid(row=0, column=0, sticky='nsew')
    utils_frame.grid_rowconfigure(0, weight=1)
    utils_frame.grid_rowconfigure(1, weight=2)
    utils_frame.grid_rowconfigure(2, weight=2)

    # === Toggle Buffering Switch ===
    toggle_frame = tk.Frame(utils_frame, bg='gray20')
    toggle_frame.grid(row=0, column=0, pady=20, padx=20, sticky='n')
    toggle_label = tk.Label(toggle_frame, text="Toggle buffer switch", fg="white", bg="gray20")
    toggle_label.pack(pady=(0, 5))
    toggle_btn = ttk.Checkbutton(toggle_frame, variable=buffering_on, onvalue=True, offvalue=False)
    toggle_btn.pack()

    # === Save 30s Button ===
    save_btn_frame = tk.Frame(utils_frame, bg='gray25', bd=2, relief='ridge')
    save_btn_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')
    save_btn = ttk.Button(save_btn_frame, text="SAVE 30s button")
    save_btn.place(relx=0.5, rely=0.5, anchor='center')

    # === Clips Save List Placeholder ===
    list_frame = tk.Frame(utils_frame, bg='gray30', bd=2, relief='ridge')
    list_frame.grid(row=2, column=0, padx=20, pady=10, sticky='nsew')
    list_label = tk.Label(list_frame, text="CLIPS SAVE LIST", fg="white", bg="gray30")
    list_label.place(relx=0.5, rely=0.5, anchor='center')

    # === OpenCV setup ===
    cap = cv2.VideoCapture(0)

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

        video_label.after(66, update_video)

    update_video()
    root.mainloop()
    cap.release()

if __name__ == "__main__":
    main()
