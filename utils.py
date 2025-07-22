import cv2
import os

def extract_frames_from_video(video_path, video_id, frame_dir):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps) if fps > 0 else 1
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_out_dir = os.path.join(frame_dir, video_id)
    os.makedirs(frame_out_dir, exist_ok=True)

    for i in range(0, total, interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, frame = cap.read()
        if not success:
            break
        frame_path = os.path.join(frame_out_dir, f"{os.path.basename(video_path)}_{i:04d}.jpg")
        cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    cap.release()
