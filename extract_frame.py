import cv2
import os

def extract_frames_from_video(video_info):
    video_path, output_folder = video_info
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        cap.release()
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_count = 0

    for frame_num in range(0, total_frames, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        success, frame = cap.read()
        if not success:
            break
        frame_count += 1
        frame_filename = f"{video_name}_{frame_count:04d}.jpg"
        frame_output_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(frame_output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    cap.release()
    return True

