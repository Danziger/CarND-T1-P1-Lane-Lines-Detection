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

    def drawLineFromPoints(self, image, X, Y, weights, color):
        #  Apply Linear Regression to fit a line model to those points:

        # slope, intercept, R, P, stdErr = stats.linregress(np.array(points))

        matX = np.matrix(X)

        if matX.shape[1] is not 0:
            reg = LinearRegression()

            reg.fit(np.transpose(np.matrix(X)), np.transpose(np.matrix(Y)), weights)

            coef = float(reg.coef_)
            intercept = float(reg.intercept_)

            # print(coef, intercept)

            self.slopes.append(coef)
            self.intercepts.append(intercept)

            # print(self.slopes, self.intercepts)
            # print(self.weights[-len(self.slopes):10])

        slope = np.average(self.slopes, weights=self.weights[-len(self.slopes):self.size])
        intercept = np.average(self.intercepts, weights=self.weights[-len(self.intercepts):self.size])

        # print(slope, intercept)

        # Ignore suspicious lines and keep the last correct one:

        # global lastSlope
        # global lastIntercept

        # if lastSlope is not None and lastIntercept is not None:
        #     slope = 0.75 * slope + 0.25 * lastSlope
        #     intercept = 0.75 * intercept + 0.25 * lastIntercept

        if slope < 0.2 and slope > -0.2:
            # For debugging of suspicious lines:

            #  color = [255, 0, 255]

            for i in range(len(X)):
                cv2.circle(image, (X[i], Y[i]), 5, [50, 0, 255], 20)

            # if lastSlope is not None and lastIntercept is not None:
                # slope = lastSlope
                # intercept = lastIntercept
        else:
            # lastSlope = slope
            # lastIntercept = intercept
            pass

        #  Convert pairs (slope, intercept) in (x, y):

        HEIGHT = image.shape[0]

        y1 = int(0.60 * HEIGHT)
        y2 = int(1.00 * HEIGHT)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        # Draw the two lines in different colors:

        THICKNESS = 15

        cv2.line(image, (x1, y1), (x2, y2), color, THICKNESS)