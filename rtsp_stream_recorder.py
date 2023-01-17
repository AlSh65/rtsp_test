import argparse

import cv2
import time
import logging

logging.basicConfig(filename='rtsp_stream_recorder.log', level=logging.DEBUG)


def record_rtsp_stream(stream_url, duration):
    try:
        # Open the RTSP stream
        cap = cv2.VideoCapture(stream_url)

        # Get the video frame width and height
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Define the codec and create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

        # Start recording
        start_time = time.time()
        end_time = start_time + duration
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                logging.error("Failed to capture video frame")
                break
            out.write(frame)
            if time.time() >= end_time:
                break

        # Release the video writer and capture objects
        out.release()
        cap.release()
        logging.info("Recording finished successfully")
    except Exception as e:
        logging.error("Failed to record RTSP stream. Reason: {}".format(str(e)))


def compress_video(file_path, codec='XVID', fps=20):
    cap = cv2.VideoCapture(file_path)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    ret, frame = cap.read()
    video_shape = (frame.shape[1], frame.shape[0])
    out = cv2.VideoWriter('compressed_' + file_path, fourcc, fps, video_shape)
    while ret:
        out.write(frame)
        ret, frame = cap.read()
    out.release()
    cap.release()
    logging.info("Video Compressed successfully")


def re_encode_video(file_path, codec='XVID', fps=20):
    cap = cv2.VideoCapture(file_path)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    ret, frame = cap.read()
    video_shape = (frame.shape[1], frame.shape[0])
    out = cv2.VideoWriter('re-encoded_' + file_path, fourcc, fps, video_shape)
    while ret:
        out.write(frame)
        ret, frame = cap.read()
    out.release()
    cap.release()
    logging.info("Video re-encoded successfully")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stream_url', help='RTSP stream URL')
    parser.add_argument('duration', type=int, help='Duration of recording in seconds')
    args = parser.parse_args()
    stream_url = args.stream_url
    duration = args.duration
    record_rtsp_stream(stream_url, duration)
    file_path = 'output.avi'
    compress_video(file_path)
    re_encode_video(file_path)