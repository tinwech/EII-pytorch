import numpy as np
import cv2 as cv
import argparse

drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
color_guided = False  # if True, draw guided color

ix, iy = -1, -1
r = 10  # circle radius
COLOR = (0, 0, 255)
WHITE = (255, 255, 255)
image = None
color = None
mask = None
guide = None


def draw(event, x, y, flags, param):
    global ix, iy, drawing, mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                if color_guided:
                    cv.rectangle(image, (ix, iy), (x, y), COLOR, -1)
                    cv.rectangle(guide, (ix, iy), (x, y), COLOR, -1)
                else:
                    cv.rectangle(image, (ix, iy), (x, y), WHITE, -1)
                    cv.rectangle(color, (ix, iy), (x, y), WHITE, -1)
                    cv.rectangle(mask, (ix, iy), (x, y), WHITE, -1)
            else:
                if color_guided:
                    cv.circle(image, (x, y), r, COLOR, -1)
                    cv.circle(guide, (x, y), r, COLOR, -1)
                else:
                    cv.circle(image, (x, y), r, WHITE, -1)
                    cv.circle(color, (x, y), r, WHITE, -1)
                    cv.circle(mask, (x, y), r, WHITE, -1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False


def main(img_path, output_path):
    global image, color, mask, guide, mode, color_guided
    image = cv.imread(img_path)
    color = cv.imread(img_path)
    gray = color[:, :, 0] * 0.11 + color[:, :, 1] * 0.59 + color[:, :, 2] * 0.3
    mask = np.zeros(color.shape, np.uint8)
    guide = np.zeros(color.shape, np.uint8)
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw)
    while (1):
        cv.imshow('image', image)
        k = cv.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == ord('c'):
            color_guided = not color_guided
        elif k == ord('q') or k == 27:
            cv.imwrite(f"color/{output_path}", color)
            cv.imwrite(f"gray/{output_path}", gray)
            cv.imwrite(f"mask/{output_path}", mask)
            cv.imwrite(f"guide/{output_path}", guide)
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default="images/img.png")
    parser.add_argument('--output', type=str, default="img.png")
    args = parser.parse_args()
    main(args.image, args.output)
