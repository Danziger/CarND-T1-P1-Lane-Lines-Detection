import cv2
import numpy as np


def rgb2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


def rgb2hls(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)


def hls2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_HLS2GRAY)


def bgr2gray(img):
    # Use when reading an image with cv2.imread()
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def yellowHlsFilter(img):
    # H in [0, 180], S in [0, 255], L in [0, 255]
    # See http://hslpicker.com

    lower = np.uint8([15, 25, 120])
    upper = np.uint8([35, 200, 255])

    return cv2.inRange(img, lower, upper)


def whiteHlsFilter(img):
    # H in [0, 180], S in [0, 255], L in [0, 255]
    # See http://hslpicker.com

    lower = np.uint8([0, 200, 0])
    upper = np.uint8([180, 255, 255])

    return cv2.inRange(img, lower, upper)


def yellowAndWhiteHlsFilter(img):
    return cv2.bitwise_or(yellowHlsFilter(img), whiteHlsFilter(img))


def yellowAndWhiteRgbFiltered(img):
    return cv2.bitwise_and(img, img, mask=yellowAndWhiteHlsFilter(rgb2hls(img)))


def regionOfInterestFilter(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    return cv2.bitwise_and(img, mask)


def gaussianBlur(img, kernel_size=3):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def houghLines(img, rho, theta, threshold, min_line_len, max_line_gap):
    return cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)


def drawLines(img, lines, color=(255, 0, 0), thickness=10, make_copy=True):
    # Copy the passed image
    img_copy = np.copy(img) if make_copy else img

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img_copy, (x1, y1), (x2, y2), color, thickness)

    return img_copy


def classifyLinesPoints(lines, width):
    centerLeft = width * 0.4
    centerRight = width * 0.6

    # Classify the points based on their slope:

    rightPointsX = []
    rightPointsY = []
    rightWeights = []
    rightLines = []
    leftPointsX = []
    leftPointsY = []
    leftWeights = []
    leftLines = []
    discardedLines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)

            # Ignore suspicious lines:

            slopeAbs = np.abs(slope)
            slopeMin = 1 / 3
            slopeMax = 3

            if slopeAbs < slopeMin or slopeAbs > slopeMax:
                discardedLines.append([[x1, y1, x2, y2]])

                continue

            # If line is valid, classify it in right or left based on its slope, and keep its length as well:

            length = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

            if slope > 0 and x1 > centerLeft and x2 > centerLeft:
                rightPointsX.extend([x1, x2])
                rightPointsY.extend([y1, y2])
                rightWeights.extend([length, length])
                rightLines.append([[x1, y1, x2, y2]])
            elif slope < 0 and x1 <= centerRight and x2 <= centerRight:
                leftPointsX.extend([x1, x2])
                leftPointsY.extend([y1, y2])
                leftWeights.extend([length, length])
                leftLines.append([[x1, y1, x2, y2]])
            else:
                discardedLines.append([[x1, y1, x2, y2]])

    return dict(
        right=dict(X=rightPointsX, Y=rightPointsY, weights=rightWeights, lines=rightLines),
        left=dict(X=leftPointsX, Y=leftPointsY, weights=leftWeights, lines=leftLines),
        discarded=discardedLines,
    )


def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)
