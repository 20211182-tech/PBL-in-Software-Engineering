import argparse
from datetime import datetime
from pathlib import Path


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


def load_cv2():
    try:
        import cv2  # pylint: disable=import-outside-toplevel
    except ImportError:
        print('OpenCV is not installed. Install it with: pip install opencv-python')
        return None

    return cv2


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


def create_video_writer(cv2, output_path, codec_name, fps, frame_size):
    fourcc = cv2.VideoWriter_fourcc(*codec_name)
    return cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)


def show_image(image_path):
    cv2 = load_cv2()
    if cv2 is None:
        return False

    image = cv2.imread(str(image_path))
    if image is None:
        print(f'Could not read image: {image_path}')
        return False

    cv2.imshow('Image Viewer', image)
    cv2.waitKey(WAIT_TIME_MS)
    cv2.destroyAllWindows()
    return True


def play_video(video_path):
    cv2 = load_cv2()
    if cv2 is None:
        return False

    video = cv2.VideoCapture(str(video_path))
    if not video.isOpened():
        print(f'Could not open video: {video_path}')
        return False

    while True:
        ok, frame = video.read()
        if not ok:
            break

        cv2.imshow('Video Player', frame)
        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF
        if is_exit_key(key):
            break

    video.release()
    cv2.destroyAllWindows()
    return True


def show_camera():
    cv2 = load_cv2()
    if cv2 is None:
        return False

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    if not camera.isOpened():
        print('Could not open the first camera.')
        return False

    while True:
        ok, frame = camera.read()
        if not ok:
            break

        cv2.imshow('Camera Viewer', frame)
        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF
        if is_exit_key(key):
            break

    camera.release()
    cv2.destroyAllWindows()
    return True


def play_video_with_shortcuts(video_path, codec_name='mp4v'):
    cv2 = load_cv2()
    if cv2 is None:
        return False

    if codec_name not in CODECS:
        print(f'Unsupported codec: {codec_name}')
        return False

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        print(f'Could not open video: {video_path}')
        return False

    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    writer = None

    ensure_directory(CAPTURE_DIR)
    ensure_directory(RECORDING_DIR)

    while True:
        ok, frame = capture.read()
        if not ok:
            break

        cv2.imshow('Shortcut Video Player', frame)

        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(WAIT_TIME_MS) & 0xFF

        if is_exit_key(key):
            break

        if is_capture_key(key):
            output_path = build_output_path(CAPTURE_DIR, 'png')
            cv2.imwrite(str(output_path), frame)
            print(f'Captured image: {output_path}')

        if is_record_start_key(key) and writer is None:
            extension = 'mp4' if codec_name == 'mp4v' else 'avi'
            output_path = build_output_path(RECORDING_DIR, extension)
            writer = create_video_writer(
                cv2=cv2,
                output_path=output_path,
                codec_name=codec_name,
                fps=fps,
                frame_size=frame_size,
            )
            print(f'Started recording: {output_path}')

        if is_record_stop_key(key) and writer is not None:
            writer.release()
            writer = None
            print('Stopped recording.')

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

    if image_path is not None:
        show_image(image_path)
    else:
        print(f'Put image files in: {IMAGE_DIR}')

    if video_path is not None:
        play_video(video_path)
        play_video_with_shortcuts(video_path)
    else:
        print(f'Put mp4 files in: {VIDEO_DIR}')


def parse_arguments():
    parser = argparse.ArgumentParser(description='OpenCV image and video viewer')
    parser.add_argument('--image', type=Path, help='Image file path')
    parser.add_argument('--video', type=Path, help='MP4 video file path')
    parser.add_argument('--camera', action='store_true', help='Open camera 0')
    parser.add_argument(
        '--shortcuts',
        action='store_true',
        help='Play video with ESC, Ctrl+Z, Ctrl+X, Ctrl+C shortcuts',
    )
    parser.add_argument(
        '--codec',
        choices=CODECS,
        default='mp4v',
        help='Recording codec',
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.image is not None:
        show_image(args.image)

    if args.video is not None and args.shortcuts:
        play_video_with_shortcuts(args.video, codec_name=args.codec)
    elif args.video is not None:
        play_video(args.video)

    if args.camera:
        show_camera()

    if args.image is None and args.video is None and not args.camera:
        run_demo()


if __name__ == '__main__':
    main()
