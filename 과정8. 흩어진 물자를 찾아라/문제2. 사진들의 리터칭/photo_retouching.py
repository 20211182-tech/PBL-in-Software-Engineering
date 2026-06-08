from pathlib import Path

import cv2


BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / 'images'

MAIN_IMAGE = IMAGE_DIR / 'sample_retouching.jpg'
OBJECT_IMAGE = IMAGE_DIR / 'sample_objects.jpg'


def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_image(image_path):
    image = cv2.imread(str(image_path))
    if image is None:
        print(f'이미지를 읽을 수 없습니다: {image_path}')
    return image


def flip_and_rotate(image):
    show_image('original image', image)

    flip_up_down = cv2.flip(image, 0)
    show_image('flip up down', flip_up_down)

    flip_left_right = cv2.flip(image, 1)
    show_image('flip left right', flip_left_right)

    rotate_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    show_image('rotate 90', rotate_90)

    rotate_180 = cv2.rotate(image, cv2.ROTATE_180)
    show_image('rotate 180', rotate_180)

    up_sample = cv2.pyrUp(image)
    show_image('up sample x2', up_sample)


def resize_and_crop(image):
    resize_640 = cv2.resize(image, (640, 480))
    show_image('resize 640 x 480', resize_640)

    resize_1024 = cv2.resize(image, (1024, 768))
    show_image('resize 1024 x 768', resize_1024)

    resize_ratio = cv2.resize(image, None, fx=0.3, fy=0.7)
    show_image('resize fx 0.3 fy 0.7', resize_ratio)

    height, width = image.shape[:2]
    start_x = width // 4
    end_x = width * 3 // 4
    start_y = height // 4
    end_y = height * 3 // 4

    crop_image = image[start_y:end_y, start_x:end_x].copy()
    show_image('deep copy crop image', crop_image)


def color_and_negative(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image('gray image', gray_image)

    negative_image = 255 - image
    show_image('negative image', negative_image)


def binary_edge_blur(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    show_image('binary image', binary_image)

    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_image = cv2.convertScaleAbs(sobel_x + sobel_y)
    show_image('sobel edge', sobel_image)

    laplacian_image = cv2.Laplacian(gray_image, cv2.CV_64F)
    laplacian_image = cv2.convertScaleAbs(laplacian_image)
    show_image('laplacian edge', laplacian_image)

    canny_image = cv2.Canny(gray_image, 100, 200)
    show_image('canny edge', canny_image)

    blur_image = cv2.GaussianBlur(image, (15, 15), 0)
    show_image('blur image', blur_image)

    part_blur_image = image.copy()
    height, width = part_blur_image.shape[:2]
    start_x = width // 4
    end_x = width * 3 // 4
    start_y = height // 4
    end_y = height * 3 // 4
    part = part_blur_image[start_y:end_y, start_x:end_x]
    part = cv2.GaussianBlur(part, (31, 31), 0)
    part_blur_image[start_y:end_y, start_x:end_x] = part
    show_image('part blur image', part_blur_image)


def hsv_and_channels(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_image, s_image, v_image = cv2.split(hsv_image)

    show_image('h channel', h_image)
    show_image('s channel', s_image)
    show_image('v channel', v_image)

    b_image, g_image, r_image = cv2.split(image)
    show_image('b channel', b_image)
    show_image('g channel', g_image)
    show_image('r channel', r_image)


def draw_object_labels(image):
    result_image = image.copy()

    cv2.rectangle(result_image, (70, 110), (210, 270), (0, 0, 255), 3)
    cv2.putText(
        result_image,
        'item 1',
        (60, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )
    cv2.line(result_image, (135, 85), (140, 110), (0, 0, 255), 2)

    cv2.rectangle(result_image, (320, 120), (520, 300), (0, 0, 255), 3)
    cv2.putText(
        result_image,
        'item 2',
        (330, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )
    cv2.line(result_image, (400, 95), (420, 120), (0, 0, 255), 2)

    cv2.circle(result_image, (190, 390), 70, (0, 0, 255), 3)
    cv2.putText(
        result_image,
        'item 3',
        (110, 330),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )
    cv2.line(result_image, (180, 340), (190, 320), (0, 0, 255), 2)

    show_image('object labels', result_image)


def main():
    image = load_image(MAIN_IMAGE)
    object_image = load_image(OBJECT_IMAGE)

    if image is None or object_image is None:
        return

    flip_and_rotate(image)
    resize_and_crop(image)
    color_and_negative(image)
    binary_edge_blur(image)
    hsv_and_channels(image)
    draw_object_labels(object_image)


if __name__ == '__main__':
    main()
