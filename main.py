import cv2
import time
import threading

CLIP_SIZE = 20
FPS = 30
# Set up the video capture
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('rtsp://admin:elefante123123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0')

frames_buffer = []



# Function to save video clip
def save_clip(buffer, output_dir='clips', fps=FPS, frame_size=(640, 480)):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = f"{output_dir}/clip_{timestamp}.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    for frame in buffer:
        out.write(frame)
    out.release()
    print(f"Saved clip to {output_path}")



def snip_buffer_start(buffer):
    snip_frame =(int) (FPS * CLIP_SIZE)
    return buffer[snip_frame:]
   
def crop_frames_buffer(buffer):
    crop_frame = (int) (FPS * CLIP_SIZE)
    return buffer[-crop_frame:]
   


# Initialize a variable to track the last update time
last_update_time = time.time()
last_log_time = time.time()
first_track = True
while True:
    ret, frame = cap.read() 
    if not ret:
        print("Failed to grab frame. Exiting...")
        break
    
    
    frames_buffer.append(frame)

    if len(frames_buffer) > FPS * CLIP_SIZE:
        frames_buffer.pop(0)
    

    
    print('Len buffer = {} | FPS = {}'.format(len(frames_buffer), FPS), end='\r',flush=True)

    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key
        print("Exiting...")
        break
    elif key == 32:  # Space key
        print("Saving last 30 seconds as a clip...")
        buffer = crop_frames_buffer(frames_buffer)
        # Run save_clip in a separate thread
        save_thread = threading.Thread(target=save_clip, args=(buffer, 'clips', 30, (frame.shape[1], frame.shape[0])))
        save_thread.start()

# Clean up
cap.release()
cv2.destroyAllWindows() 
