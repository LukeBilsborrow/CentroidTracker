import cvlib
import sys
import math
import os
from PIL import Image

import numpy as np

import CentroidTracker
import ImageUtils


def crop_frames(frames, detections):
    tracker = CentroidTracker.CentroidTracker()
    cropped_frames = []
    for i in range(len(frames)):
        frame = frames[i]
        detection_data = detections[i]
        objects = tracker.update(detection_data)
        if len(objects) == 0:
            continue
        try:
            cropped_frame = frame.crop(objects[0][1])
            cropped_frames.append(cropped_frame)
        except:
            continue

    return cropped_frames

def get_ordered_frames_from_dir(dir):
    frames = []
    total_files = len([name for name in os.listdir(dir)])
    for i in range(1, total_files+1):
        frame_title = f"out-{i:04d}.png"
        frame = Image.open(os.path.join("C:/Users/lukex/Desktop/frames", frame_title))
        frames.append(frame)

    return frames

def get_frames_detections(frames):
    detections = []
    for i in frames:
        faces, confidences = cvlib.detect_face(np.asarray(i), threshold=0.2)
        detections.append(faces)

    return detections

frames = get_ordered_frames_from_dir("C:/Users/lukex/Desktop/frames")
detections = get_frames_detections(frames)
cropped_frames = crop_frames(frames, detections)
max_width = math.ceil(max([x.size[0] for x in cropped_frames])/2)*2
max_height = math.ceil(max([x.size[1] for x in cropped_frames])/2)*2

cropped_frames = [ImageUtils.pad_image_to_size(x, (max_width, max_height)) for x in cropped_frames]
for i in range(1, len(cropped_frames)+1):
    frame_title = f"out-{i:04d}.png"
    cropped_frames[i-1].save(os.path.join("C:/Users/lukex/Desktop/frames2", frame_title))



sys.exit()