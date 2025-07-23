import cv2
import os

def extract_frames_from_video(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Skipping unreadable file: {video_path}")
        return 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print(f"Skipping 0 FPS file: {video_path}")
        return 0
    interval = int(fps)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    count = 0

    for frame_num in range(0, total, interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        success, frame = cap.read()
        if not success:
            break
        count += 1
        frame_file = f"{video_name}_{count:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    cap.release()
    return count

def extract_all_frames(input_folder, output_folder):
    video_exts = ('.mp4', '.avi', '.mov', '.mkv')
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.lower().endswith(video_exts):
            video_path = os.path.join(input_folder, file)
            extract_frames_from_video(video_path, output_folder)
