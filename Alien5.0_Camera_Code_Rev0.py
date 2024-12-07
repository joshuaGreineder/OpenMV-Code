# ALIEN 5.0 CAMERA CODE
# Created by Joshua Greineder
# Contributers:
# Description:
# This Python script captures images from a camera sensor,
# enhances them, converts them to grayscale, and detects
# line segments meeting specific color and length criteria.
# It then draws these eligible line segments in red on the
# original color image.
# Date Created 8/12/2023
# Last Modified 10/13/2023

import sensor, image, time, math

# Initialize the camera sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Set the pixel format to RGB565 for color
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)  # Skip some initial frames to allow the sensor to stabilize
clock = time.clock()

# Function to check if a target color is present in a given radius of a point
def has_color_in_radius(img, x, y, radius, target_color, tolerance):
    for i in range(x - radius, x + radius + 1):
        for j in range(y - radius, y + radius + 1):
            if 0 <= i < img.width() and 0 <= j < img.height():
                color = img.get_pixel(i, j)
                if abs(color - target_color) <= tolerance:
                    return True
    return False

while True:
    clock.tick()
    # Capture the image in color, perform histogram equalization, lens correction, and sharpening
    img = sensor.snapshot().histeq(adaptive=True, clip_limit=1).lens_corr(strength=1.2).laplacian(1, sharpen=True)

    # Convert the color image to grayscale for processing
    img_gray = img.copy().to_grayscale()

    radius = 1
    target_color = 255  # Target color value (white)
    color_tolerance = 20

    # Find line segments in the grayscale image
    lines = img_gray.find_line_segments(merge_distance=5, max_theta_diff=3)
    if lines:
        for l in lines:
            if l and has_color_in_radius(img_gray, int(l.x1()), int(l.y1()), radius, target_color, color_tolerance) and has_color_in_radius(img_gray, int(l.x2()), int(l.y2()), radius, target_color, color_tolerance):
                # Calculate the length of the line segment
                line_length = math.sqrt((l.x2() - l.x1()) ** 2 + (l.y2() - l.y1()) ** 2)

                # Set a minimum length threshold (adjust as needed)
                min_length_threshold = 20

                if line_length >= min_length_threshold:
                    img.draw_line(l.line(), color=(255, 0, 0))  # Draw in color on the color image

    # Display the color image with lines drawn
    # img.compress(quality=100)  # You can uncomment this line if needed to compress the image
    print("FPS %f" % clock.fps())
