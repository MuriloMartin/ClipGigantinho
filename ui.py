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
    
    # Configure grid layout
    root.grid_columnconfigure(0, weight=1, uniform="group1")
    root.grid_columnconfigure(1, weight=4, uniform="group1")
    root.grid_rowconfigure(0, weight=1)

    # === Video Frame ===
    video_frame = tk.Frame(root, bg='black')
    video_frame.grid(row=0, column=1, sticky='nsew')
    video_label = tk.Label(video_frame, bg='black')
    video_label.place(relx=0.5, rely=0.5, anchor='center')

    # === UI controls ===
    utils_frame = tk.Frame(root, bg='gray20')
    utils_frame.grid(row=0, column=0, sticky='nsew')

    # === BUTTONS FRAME ===
    buttons_frame = tk.Frame(utils_frame, bg="pink")
    buttons_frame.pack(side="top", pady=50) 

    # === List FRAME ===
    list_frame = tk.Frame(utils_frame, bg="blue")
    list_frame.pack(side="bottom", pady=50)  

    # Toggle Buffering Button
    toggle_btn = ttk.Button(buttons_frame, text="Toggle Buffering")
    toggle_btn.pack(pady=10, ipadx=10, ipady=5)

    # Save Clip Button
    save_btn = ttk.Button(buttons_frame, text="Save last 30s")
    save_btn.pack(pady=10, ipadx=10, ipady=5)

    # === OpenCV setup ===
    cap = cv2.VideoCapture(0)

    def update_video():
        ret, frame = cap.read()
        if ret:
            # Convert frame to RGB and then to ImageTk
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            
            root.update_idletasks()  # Forces geometry calculation

            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk  # Keep reference
            video_label.config(image=imgtk)

        video_label.after(66, update_video)  # Refresh every ~30 ms

    update_video()
    root.mainloop()

    cap.release()

if __name__ == "__main__":
    main()
