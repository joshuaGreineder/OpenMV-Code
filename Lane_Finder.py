import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Set the pixel format to RGB565 for color
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

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
    # Capture the image in color
    img = sensor.snapshot().histeq(adaptive=True, clip_limit=1).lens_corr(strength=1.2).laplacian(1, sharpen=True)

    # Convert the color image to grayscale for processing
    img_gray = img.copy().to_grayscale()

    radius = 4
    target_color = 255
    color_tolerance = 30

    lines = img_gray.find_line_segments(merge_distance=20, max_theta_diff=5)
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
    #img.compress(quality=100)  # Compress the image to fit the IDE's window
    print("FPS %f" % clock.fps())
