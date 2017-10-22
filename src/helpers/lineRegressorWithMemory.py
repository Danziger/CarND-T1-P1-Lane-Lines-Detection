from collections import deque
from sklearn.linear_model import LinearRegression

import cv2
import numpy as np


class LineStream:

    def __init__(self, size=8):
        self.size = size
        self.reset()

    def reset(self):
        size = self.size

        self.slopes = deque(maxlen=size)
        self.intercepts = deque(maxlen=size)
        self.weights = list(range(1, size+1, 1))

    def drawLineFromPoints(self, image, X, Y, weights, thickness=10, color=(255, 0, 0)):
        matX = np.matrix(X)

        HEIGHT = image.shape[0]
        WIDTH = image.shape[1]

        if matX.shape[1] is not 0:
            # Apply Linear Regression to fit a line model to the points:

            reg = LinearRegression()
            reg.fit(np.transpose(np.matrix(X)), np.transpose(np.matrix(Y)), weights)

            slope = float(reg.coef_)
            intercept = float(reg.intercept_)

            self.slopes.append(slope)
            self.intercepts.append(intercept)
        else:
            # Something is wrong, so draw a border around the image:

            cv2.rectangle(image, (0, 0), (WIDTH, HEIGHT), color, thickness * 2)

            # If we don't have any data yet, don't do anything, otherwise use previous data:

            if len(self.slopes) is 0:
                return

        # Calculate new line attributes based on fitted line and previous values:

        currentItems = len(self.slopes)

        slope = np.average(self.slopes, weights=self.weights[-currentItems:self.size])
        intercept = np.average(self.intercepts, weights=self.weights[-currentItems:self.size])

        if abs(slope) < 0.2: # TODO: Use realative values
            # Suspicious slope (too big). Just use previous one:

            cv2.rectangle(image, (0, 0), (WIDTH, HEIGHT), color[::-1], thickness * 2)

            # slope = self.slopes[-2]
            # intercept = self.intercepts[-2]

            # self.slopes[-1] = slope
            # self.intercepts[-1] = intercept

            # Draw individual points:

            for i in range(len(X)):
                cv2.circle(image, (X[i], Y[i]), thickness, color[::-1], -thickness)

        # Convert pairs (slope, intercept) in (x, y):

        y1 = int(0.60 * HEIGHT)
        y2 = int(1.00 * HEIGHT)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        # Draw the two lines in different colors:

        cv2.line(image, (x1, y1), (x2, y2), color, thickness)
