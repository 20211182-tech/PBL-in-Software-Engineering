import argparse
from datetime import datetime
from pathlib import Path

import cv2


WAIT_TIME_MS = 33
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

KEY_ESC = 27
KEY_CTRL_Z = 26
KEY_CTRL_X = 24
KEY_CTRL_C = 3

CODECS = ('mp4v', 'XVID')

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / 'images'
VIDEO_DIR = BASE_DIR / 'videos'
CAPTURE_DIR = BASE_DIR / 'captures'
RECORDING_DIR = BASE_DIR / 'recordings'


def ensure_directory(directory):
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_now_text():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


def build_output_path(directory, extension, now_text=None):
    timestamp = now_text or get_now_text()
    clean_extension = extension.lstrip('.')
    return directory / f'{timestamp}.{clean_extension}'


def is_exit_key(key):
    return key == KEY_ESC


def is_capture_key(key):
    return key == KEY_CTRL_Z


def is_record_start_key(key):
    return key == KEY_CTRL_X


def is_record_stop_key(key):
    return key == KEY_CTRL_C


def get_recording_extension(codec_name):
    if codec_name == 'mp4v':
        return 'mp4'
    return 'avi'


def get_video_fps(capture):
    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        return 30
    return fps


def get_video_size(capture):
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height


def create_video_writer(output_path, codec_name, fps, frame_size):
    fourcc = cv2.VideoWriter_fourcc(*codec_name)
    return cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)


def show_image(image_path):
    image = cv2.imread(str(image_path))
    if image is None:
        print(f'이미지를 열 수 없습니다: {image_path}')
        return False

    cv2.imshow('Image Viewer', image)
    cv2.waitKey(WAIT_TIME_MS)
    cv2.destroyAllWindows()
    return True


def play_video(video_path):
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        print(f'동영상을 열 수 없습니다: {video_path}')
        return False

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        cv2.imshow('Video Player', frame)
        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF
        if is_exit_key(key):
            break

    capture.release()
    cv2.destroyAllWindows()
    return True


def show_camera():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    if not capture.isOpened():
        print('첫 번째 카메라를 열 수 없습니다.')
        return False

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        cv2.imshow('Camera Viewer', frame)
        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF
        if is_exit_key(key):
            break

    capture.release()
    cv2.destroyAllWindows()
    return True


def capture_frame(frame):
    ensure_directory(CAPTURE_DIR)
    output_path = build_output_path(CAPTURE_DIR, 'png')
    cv2.imwrite(str(output_path), frame)
    print(f'이미지 캡처 완료: {output_path}')


def start_recording(codec_name, fps, frame_size):
    ensure_directory(RECORDING_DIR)
    extension = get_recording_extension(codec_name)
    output_path = build_output_path(RECORDING_DIR, extension)
    writer = create_video_writer(output_path, codec_name, fps, frame_size)
    print(f'녹화 시작: {output_path}')
    return writer


def stop_recording(writer):
    writer.release()
    print('녹화 중지')


def play_video_with_shortcuts(video_path, codec_name='mp4v'):
    if codec_name not in CODECS:
        print(f'지원하지 않는 코덱입니다: {codec_name}')
        return False

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        print(f'동영상을 열 수 없습니다: {video_path}')
        return False

    fps = get_video_fps(capture)
    frame_size = get_video_size(capture)
    writer = None

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        cv2.imshow('Shortcut Video Player', frame)

        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF

        if is_exit_key(key):
            break
        if is_capture_key(key):
            capture_frame(frame)
        if is_record_start_key(key) and writer is None:
            writer = start_recording(codec_name, fps, frame_size)
        if is_record_stop_key(key) and writer is not None:
            stop_recording(writer)
            writer = None

    if writer is not None:
        writer.release()

    capture.release()
    cv2.destroyAllWindows()
    return True


def find_first_file(directory, suffixes):
    if not directory.exists():
        return None

    for file_path in sorted(directory.iterdir()):
        if file_path.suffix.lower() in suffixes:
            return file_path

    return None


def run_demo():
    image_path = find_first_file(IMAGE_DIR, {'.jpg', '.jpeg', '.png', '.bmp'})
    video_path = find_first_file(VIDEO_DIR, {'.mp4'})

    if image_path is None:
        print(f'이미지 파일을 넣어 주세요: {IMAGE_DIR}')
    else:
        show_image(image_path)

    if video_path is None:
        print(f'mp4 파일을 넣어 주세요: {VIDEO_DIR}')
    else:
        play_video(video_path)
        play_video_with_shortcuts(video_path)


def parse_arguments():
    parser = argparse.ArgumentParser(description='OpenCV 이미지/영상 제어')
    parser.add_argument('--image', type=Path, help='출력할 이미지 파일 경로')
    parser.add_argument('--video', type=Path, help='재생할 mp4 파일 경로')
    parser.add_argument('--camera', action='store_true', help='첫 번째 카메라 출력')
    parser.add_argument(
        '--shortcuts',
        action='store_true',
        help='ESC, Ctrl+Z, Ctrl+X, Ctrl+C 단축키 사용',
    )
    parser.add_argument(
        '--codec',
        choices=CODECS,
        default='mp4v',
        help='녹화 코덱 선택',
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.image is not None:
        show_image(args.image)

    if args.video is not None:
        if args.shortcuts:
            play_video_with_shortcuts(args.video, args.codec)
        else:
            play_video(args.video)

    if args.camera:
        show_camera()

    if args.image is None and args.video is None and not args.camera:
        run_demo()


if __name__ == '__main__':
    main()
