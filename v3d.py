#!/usr/bin/env python3

# args: 
#   1: input file name
#   2: output file name, defaults to time_{input-file-name}.mp4
#   3: max frames to transform, 0 means avg of width and height (default), -1 means unlimited
#   4: shape, default -> thw, allowed: wth, thw

from sys import argv
from os import system
import cv2
import numpy as np

# Load video
if len(argv) > 1:
    video_path = argv[1]
else:
    print("you must specify input file name as a 1st argument.")
    exit(1)

if len(argv) > 2:
    output_path = argv[2]
else:
    output_path = 'time_' + video_path
    if not output_path.lower().endswith('.mp4'):
        output_path += '.mp4'

print(f"reading {video_path}, will write to {output_path}.")

# Read the video
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if frame_count == 0 or frame_width == 0 or frame_height == 0 or fps == 0:
    print(f"cannot decode {video_path}.")
    exit(2)
print(f"{video_path}: {frame_width}x{frame_height}, {fps} FPS, {frame_count} frames.")

# Handle max frames
max_frames = 0
if len(argv) > 3:
    max_frames = int(argv[3])
    print(f"processing no more than {max_frames} frames (0=average of width/height, -1=unlimited).")

if max_frames == 0:
    max_frames = ((frame_width + frame_height) / 4) * 2
    print(f"processing no more than {max_frames} frames")

# shapes
shape = 'thw'
if len(argv) > 4:
    shape = argv[4].lower()
print(f"new shape {shape}, allowed: thw, wth")

# Read frames into a NumPy array
frames = []
n = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
    n += 1
    if max_frames > 0 and n >= max_frames:
        break
cap.release()
print(f"read {len(frames)} frames.")

# Shape: (T, H, W, C)
frames = np.array(frames)
print(f"created NP array ({n} items).")

if shape == 'wth':
    # Swap height and time dimensions (T, H, W, C) → (W, T, H, C)
    transformed = np.transpose(frames, (2, 0, 1, 3))
elif shape == 'thw':
    # Swap time and width dimensions (T, H, W, C) → (W, H, T, C)
    transformed = np.transpose(frames, (2, 1, 0, 3))
else:
    print(f"unknown new shape {shape} just applying MJPEG re-encoding.")
    transformed = np.transpose(frames, (0, 1, 2, 3))
    print(f"applied transpose.")

# Get new video size
new_frame_count, new_height, new_width, _ = transformed.shape
print(f"{output_path} will be: {new_width}x{new_height}, {fps} FPS, {new_frame_count} frames.")

# Save the transformed video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

print(f"writing {output_path} {new_frame_count} frames.")
for i in range(new_frame_count):
    if i > 0 and i % 100 == 0:
        print(f"{i} frame.")
    out.write(transformed[i])

out.release()
print(f"transformed video saved as {output_path}.")
# print(f"consider now h265.sh {output_path}")
cmd = f"ffmpeg -loglevel error -hide_banner -nostats -y -threads 16 -re -i '{output_path}' -c:v libx265 -x265-params log-level=error -crf 29 -preset slow -an 'tmp_{output_path}' && mv 'tmp_{output_path}' '{output_path}' && ls -l '{output_path}'"
print(cmd)
system(cmd)
