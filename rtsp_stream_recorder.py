import argparse
from moviepy.editor import VideoFileClip
import cv2
import time
import logging

logging.basicConfig(filename='rtsp_stream_recorder.log', level=logging.DEBUG)


def record_rtsp_stream(stream_url, duration):
    try:
        cap = cv2.VideoCapture(stream_url)

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

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
        out.release()
        cap.release()
        logging.info("Recording finished successfully")
    except Exception as e:
        logging.error(f"Failed to record RTSP stream. Reason: {str(e)}")


def modification_video(file_path):
    clip = VideoFileClip(file_path)
    clip.write_videofile(file_path, codec='libx264', audio_codec='aac', preset='medium', bitrate='2000k')
    logging.info("Video modification successfully")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stream_url', help='RTSP stream URL')
    parser.add_argument('duration', type=int, help='Duration')
    args = parser.parse_args()
    stream_url = args.stream_url
    duration = args.duration
    record_rtsp_stream(stream_url, duration)
    file_path = 'output.avi'
    modification_video(file_path)
