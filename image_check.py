import sensor
import image
import pyb
import os

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Set the pixel format (can be grayscale or RGB565)
sensor.set_framesize(sensor.QVGA)    # Set the frame size (320x240 in this case)
sensor.skip_frames(time=2000)        # Allow the sensor to warm up

# Number of images to capture
num_images = 5

# Capture and save a series of images
for i in range(num_images):
    # Capture an image
    img = sensor.snapshot()

    # Create a unique file name for each image using a counter
    temp_file = "image_{}.jpg".format(i)

    # Save the image with the unique file name
    img.save(temp_file)

    # Print a message to indicate success
    print("Image {} saved to {}".format(i, temp_file))

    # Delay for a moment between captures (you can adjust this as needed)
    pyb.delay(1000)
