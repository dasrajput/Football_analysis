import cv2


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames

def save_video(output_video_frames,output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()

def process_video_in_batches(video_frames, batch_size=10):
    num_frames = len(video_frames)
    for start in range(0, num_frames, batch_size):
        end = min(start + batch_size, num_frames)
        batch_frames = video_frames[start:end]
        process_batch(batch_frames)

def process_batch(batch_frames):
    # Example processing: Convert each frame to grayscale
    for i in range(len(batch_frames)):
        batch_frames[i] = cv2.cvtColor(batch_frames[i], cv2.COLOR_BGR2GRAY)
    return batch_frames
