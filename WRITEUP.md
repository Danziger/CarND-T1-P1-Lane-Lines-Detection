CarND · T1 · P1 · Lane Lines Detection Project Writeup
======================================================

[//]: # (Image References)

[step1]: ./output/images/001%20-%20Color%20Spaces.png "Color Spaces"
[step2]: ./output/images/002%20-%20Filters.png "Filters"
[step3]: ./output/images/003%20-%20Region%20-%20of%20-%20Interest.png "Region of Interest"
[step4]: ./output/images/004%20-%20Gaussian%20Blur.png "Gaussian Blur"
[step5]: ./output/images/005%20-%20Canny%20Edge%20Detection.png "Canny Edge Detection"
[step6]: ./output/images/006%20-%20Hough%20Transform.png "Hough Transform"
[step7]: ./output/images/007%20-%20Line%20Classification.png "Line Classification"
[step8]: ./output/images/008%20-%20Final%20Result.png "Final Result"


Project Goals
-------------

The goals / steps of this project are the following:

* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


Project Reflection
------------------

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 7 steps:

#### Step 1 - Changing color space from RGB to HLS:

First, I convert the images from RGB to HLS, even thought grayscale is suggested, at the cost of a bigger amount of data
to process (3 channels instead of 1), as having a single channel for color (H = Hue), another one for lightness
(L = Luma) and another one for saturation (S = Saturation) makes it easier for us to create filters than in RGB, where
those 3 attributes are spread across all its 3 channels. We do this in the next step.

![Color Spaces][step1]

We can see how the lane lies stand out clearer in HLS than they do in HSV.


#### Step 2 - Color (yellow and white) filters:

We know lane lines in our examples are either white or yellow. Therefore, any other information (pixels of any other
color) is not relevant to us and we can filter it out. To do this we create two filters and merge them together, one for
white and another one for yellow, considering a range of shades for both that will be considered valid.

Once applied, we can see most non-relevant information, with some exceptions, has already been filtered out:

![Filters][step2]


#### Step 3 - Region of interest filter:

We know that the lines we are interested in are always inside a centered triangle pointing upwards from the bottom of
the image to approx. 60 - 70 % of it. We also know those two lines never touch them, so this triangle it's actually
a trapezium.

When I tested my project with the challenge videos of the Advanced Lane Lines Project, I found out I should also filter
a smaller triangle area that corresponds to the space between both lines (as there could be signs painted on the road)
and also leave a small margin at the bottom of the image, as the hood of the car may appear in that section.

Any information outside that area can be discarded, as whatever it is, it's not going to be a lane lines:

![Region of Interest][step3]


#### Step 4 - Gaussian blur:

In order to smooth out noise and small irregularities from the the image, we apply a subtle gaussian blur, that will
still keep the lane lines in place.

Here we can see different parameters for this algorithm:

![Gaussian Blur][step4]

I finally took K = 5.


#### Step 5 - Canny edge detection:

In order to detect edges on our image, particularly those around the lane lines, we apply canny edge detection
algorithm.

Here we can see different parameters for this algorithm:

![Canny Edge Detection][step5]

I finally took T = [50, 100].


#### Step 6 - Hough lines:

Now that we have all the edges clearly showing up on the image, we need to extract them as lines to be able to work with
these lines. To do that, we apply a Hough transform. 

This will give us a bunch of lines, some of which we are interested in (the ones that are the lateral borders of our
lane lines) and some others which we will discard (top or bottom borders or the lane lines or any other line produced by
road irregularities, other cars, shadows...).

Here we can see different parameters for this algorithm:

![Hough Transform][step6]

I finally took:
- rho = 2
- theta = PI / 180
- threshold = 30,
- minLineLength = 20
- maxLineLength = 80


#### Step 7 - Hough lines filtering and classification:

Using each line's slope and position we can distinguish those on the right side of the image from those on the left
one, and discard those which's slope is too big or too small:

![Line Classification][step7]

Notice how, in the second image (007 - Challenge Shadow.jpg), some lines have been discarded based on their slope (the
cyan ones).


#### Step 8 - Fitting a linear model:

Next, I fit a linear model to the points of right lines and another one to those of left lines. Each point will have a
weight based on the length of the line it belonged to, so the 2 points of a long line will have a bigger impact on the
final line's attributes that those of a short one.

It's important to mention that the resulting line is a weighted combination of the one fitted to those points and the
N previous ones (N = 8 in the current pipeline), with the weights being 1, 2, ..., N + 1, so that the more recent
information always has a bigger impact than the old one.

This will make the lines drawn on the videos change smoothly.


#### Step 9 - Drawing the lines on the image:

Lastly, I just draw the two resulting lines on top of the original image:

![Final Result][step8]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what we can see in `003 - Challenge.mp4` as the discontinuous lane line's portions
approach and disappear, causing the fitted line to wiggle slightly. Although we could improve that by having a bigger
queue to store more of the previous lines' attributes, or changing the weights so that the most recent values are
not so much more important than the previous ones, that would also mean the fitted line would have a harder time trying
to match the changes on the road, causing other problems like the ones we can see in `006 - Advanced Project Harder
Challenge.mp4`

Another shortcoming could be that any signs painted in the middle of the lane, like those in `005 - Advanced Project
Challenge.png`, will be also interpreted as lane lines. Although this has currently been partially fixed with a region
filter, that may not be the best approach and doesn't totally mitigate the problem, as we can clearly see if we compare 
`005 - Advanced Project Challenge.png` with any of the previous videos.

One of the biggest limitations of the current pipeline is using a linear model, as the sharpest the curves on the
image/video are, the worse the results will be, which we can clearly see in the last video `006 - Advanced Project
Harder Challenge.mp4`.

Lastly, another big restriction of this pipeline is that it has been designed to identify a single pair of lane lines
and only once the car has already been centered between them, otherwise they will probably be incorrectly filtered out 
by the region filter.


### 3. Suggest possible improvements to your pipeline

To fix the buffering issues, the weights could be changed dynamically, probably using the variance to give more or less
priority to the new values or to the old ones.

Another thing that is currently being done with fix values but could be improved by dynamically setting them is
filtering segments extracted using the Hough Transform based on their slope. Probably, the limit values used to discard
them should depend on previous values. This will probably improve the results in `006 - Advanced Project Harder
Challenge.mp4` as much as possible with a linear model.

The next improvement would be to fit a more complex model, let's say a polynomial one, to be able to precisely detect
the lane lines on curvy roads.

Lastly, we could remove or change the region filter and use a clustering algorithm like K-Means to be able to identify
multiple lanes and lane lines.
