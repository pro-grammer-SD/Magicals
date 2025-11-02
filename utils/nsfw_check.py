import cv2
import tempfile
import numpy as np
from opennsfw2 import predict_image

def sample_frames(video_path, n=10):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        cap.release()
        return []
    step = max(1, total // n)
    frames = []
    for i in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, frame = cap.read()
        if not ok:
            continue
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cv2.imwrite(tmp.name, frame)
        frames.append(tmp.name)
    cap.release()
    return frames

def check_video_nsfw(video_path, threshold=0.7):
    frames = sample_frames(video_path, n=10)
    if not frames:
        return False, {}
    scores = []
    info = {}
    for f in frames:
        r = predict_image(f)
        scores.append(r)
        info[f] = r
    mean_score = float(np.mean(scores))
    for f in frames:
        try:
            import os
            os.remove(f)
        except:
            pass
    return mean_score >= threshold, {"mean": mean_score, "frames_checked": len(scores)}
