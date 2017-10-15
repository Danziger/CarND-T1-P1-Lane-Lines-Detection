#**Finding Lane Lines on the Road** 

##Writeup Template

###You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.


**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 7 steps:

####Step 1 - Changing color space from RGB to HLS:

First, I convert the images from RGB to HLS, even thought grayscale is suggested, as this offers two additional benefits
at the cost of a bigger amount of data to process (3 channels instead of 1).

The first one is that lines stand out more clearly regardless of shades and reflections, as their color is further away
from the road's one (any shade of gray) in this color space.

Secondly, having a single channel for color (H = Hue), another one for lightness (L = Luma) and another one for
saturation (S = Saturation) makes it easier for us to create filters than in RGB, where those 3 attributes are spread
across all its 3 channels. We do this in the next step.


####Step 2 - Color (yellow and white) filters:

We know lane lines in our examples are either white or yellow. Therefore, any other information (pixels of any other
color) are not relevant to us and we can filter them out. To do this we create two filters and merge them together, one
for white and another one for yellow, considering a range of shades for both that will be considered valid.

Once applied, we can see most non-relevant information, with some exceptions, has already been filtered out.

####Step 3 - Region of interest filter:

We know that the lines we are interested in are always inside a centered triangle pointing upwards from the bottom of
the image to approx. 60 - 70 % of it. We also know those two lines never touch them, so this triangle it's actually
a trapezium.

We can discard any information outside that area, as whatever we find in there, it's not going to be our lane lines.

####Step 4 - Gaussian blur:

In order to smooth out noise and small irregularities from the the image, we apply a subtle gaussian blur, that will
still keep the lane lines in place.

####Step 5 - Canny edge detection:

In order to detect edges on our image, particularly those around the lane lines, we apply canny edge detection
algorithm.

####Step 6 - Hough lines:

Now that we have all the edges clearly showing up on the image, we need to extract them as lines to be able to work with
these lines. To do that, we apply a Hough transform. 

This will give us a bunch of lines, some of which we are interested in (the ones that are the lateral borders of our
lane lines) and some others which we will discard (top or bottom borders or the lane lines or any other line produced by
road irregularities, other cars, shadows...).

####Step 7 - Hough lines filtering and classification:

Using each line's slope and position we can distinguish those on the right side of the image from those on the left
one, and discard those which's slope is too big or too small. 

####Step 8 - Fitting a linear model:

Next, I fit a linear model to the points of right lines and another one to those of left lines. Each point will have a
weight based on the length of the line it belonged to, so the 2 points of a long line will have a bigger impact on the
final line's attributes that those of a short one.

It's important to mention that the resulting line is a weighted combination of the one fitted to those points and the
N previous ones (N = 8 in the current pipeline), with the weights being 1, 2, ..., N + 1, so that the more recent
information always has a bigger impact than the old one.

####Step 9 - Drawing the lines on the image:

Lastly, I just draw the two resulting lines on top of the original image.




In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]





###2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


###3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...