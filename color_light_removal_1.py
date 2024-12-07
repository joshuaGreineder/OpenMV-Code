import sensor, image, time

# Initialize camera
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

# Parameters for lane detection
roi = (0, 120, 320, 60)  # Region of interest
canny_threshold = (50, 80)  # Canny edge detection threshold
hough_rho = 1
hough_theta = 1
hough_threshold = 60
hough_min_line_length = 20
hough_max_line_gap = 15

while True:
    clock.tick()

    # Capture a frame
    img = sensor.snapshot()

    # Apply ROI
    img_roi = img.copy(roi=roi)

    # Perform Canny edge detection
    edges = img_roi.find_edges(image.EDGE_CANNY, threshold=canny_threshold)

    # Perform Hough line detection
    lines = edges.find_lines(rho=hough_rho, theta=hough_theta,
                              threshold=hough_threshold,
                              line_threshold=hough_min_line_length,
                              max_theta_diff=15,
                              roi=(0, 0, img_roi.width(), img_roi.height()))

    # Find the most dominant lane line
    dominant_line = None
    max_length = 0
    for line in lines:
        length = (line.x2() - line.x1()) ** 2 + (line.y2() - line.y1()) ** 2
        if length > max_length:
            max_length = length
            dominant_line = line

    # Draw the detected lane line
    if dominant_line:
        img.draw_line(dominant_line.line(), color=127)

    # Display the image with lane lines
    img.show()

    print(clock.fps())
