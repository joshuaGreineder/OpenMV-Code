import sensor, image
# Initialize the camera and LCD
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

while True:
    # Capture an image
    img = sensor.snapshot()

    # Rotate the image by 90 degrees clockwise
    img = img.transpose(image.Transpose.ROTATE_90)
    img = img.flip(False, True)  # Use True to rotate counterclockwise
