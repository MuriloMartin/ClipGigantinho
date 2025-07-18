import os
import subprocess
import time
import glob
import threading
from pathlib import Path

# === CONFIGURATION ===
RTSP_URL = 'rtsp://admin:elefante123123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0' 
BUFFER_DIR = 'clips_buffer'
CLIP_SAVE_DIR = 'clips'
CLIP_DURATION = 30  
MAX_BUFFER_SECONDS = 35  

# === Setup ===
Path(BUFFER_DIR).mkdir(exist_ok=True)
Path(CLIP_SAVE_DIR).mkdir(exist_ok=True)

def start_ffmpeg_segmenter():
    print("[FFMPEG] Starting segmenter...")
    cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', RTSP_URL,
        '-c:v', 'libx264',
        '-preset', 'veryfast',          # faster encoding
        '-tune', 'zerolatency',         # helps with RTSP
        '-g', '30',                     
        '-keyint_min', '30',
        '-sc_threshold', '0',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'segment',
        '-segment_time', '1',
        '-reset_timestamps', '1',
        '-strftime', '1',
        f'{BUFFER_DIR}/%Y%m%d_%H%M%S.mp4'
    ]

    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)



def get_last_n_clips(n):
    files = sorted(glob.glob(f"{BUFFER_DIR}/*.mp4"))
    return files[-n:]

def save_clip_from_buffer():
    clips = get_last_n_clips(CLIP_DURATION)
    if len(clips) < CLIP_DURATION:
        print("[SAVE] Not enough data yet.")
        return

    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_file = f"{CLIP_SAVE_DIR}/clip_{timestamp}.mp4"
    input_txt = f"inputs_{timestamp}.txt"

    with open(input_txt, 'w') as f:
        for clip in clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', input_txt,
        '-c', 'copy',
        output_file
    ]

    subprocess.run(cmd)
    os.remove(input_txt)
    print(f"[SAVE] Saved clip to: {output_file}")

def cleanup_old_clips():
    files = sorted(glob.glob(f"{BUFFER_DIR}/*.mp4"))
    if len(files) <= MAX_BUFFER_SECONDS:
        return
    to_delete = files[:-MAX_BUFFER_SECONDS]
    for f in to_delete:
        try:
            os.remove(f)
        except Exception as e:
            print(f"[CLEANUP] Failed to remove {f}: {e}")

def background_cleaner():
    while True:
        cleanup_old_clips()
        time.sleep(5)

def clear_buffer():
    files = glob.glob(f"{BUFFER_DIR}/*.mp4")
    for f in files:
        os.remove(f)

def get_files_list():
    try:
        return [f for f in os.listdir(CLIP_SAVE_DIR) if f.endswith('.mp4')]
    except FileNotFoundError:
        return []

def start_buffering():
    clear_buffer()
    ffmpeg_proc = start_ffmpeg_segmenter()
    cleaner_thread = threading.Thread(target=background_cleaner, daemon=True)
    cleaner_thread.start()
    return ffmpeg_proc

