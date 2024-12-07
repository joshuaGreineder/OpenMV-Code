import sensor, image, time, pyb
from pyb import DAC

# Configure the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

# Initialize the DAC
dac = DAC(2) # DAC on pin X6

# Define a function to process the image and detect lane lines
def detect_lane_lines(img):
    # Convert the image to grayscale
    gray = img.to_grayscale()

    # Apply a Canny edge detection
    edges = gray.find_edges(image.EDGE_CANNY, threshold=(50, 80))

    # Find line segments in the image
    lines = edges.find_lines(threshold=100)

    left_line = None
    right_line = None

    for line in lines:
        if line.theta() < 45 or line.theta() > 135:
            if left_line is None or line.magnitude() > left_line.magnitude():
                left_line = line
        elif line.theta() > 45 and line.theta() < 135:
            if right_line is None or line.magnitude() > right_line.magnitude():
                right_line = line

    return left_line, right_line

# Main loop to process the images and control the DAC
while True:
    img = sensor.snapshot()
    left_line, right_line = detect_lane_lines(img)

    if left_line:
        img.draw_line(left_line.line(), color=(255, 0, 0))
        dac.write(int(left_line.theta() * 4095 / 180))

    if right_line:
        img.draw_line(right_line.line(), color=(0, 255, 0))
        dac.write(int(right_line.theta() * 4095 / 180))
