import sensor
import image
import pyb
import ustruct

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

# Open a serial connection (adjust the UART number and baud rate as needed)
uart = pyb.UART(3, 115200)

# Number of images to capture
num_images = 100

for i in range(num_images):
    # Capture an image
    img = sensor.snapshot()

    # Convert the image to JPEG format and get its size
    img = img.compress(quality=90)
    img_size = img.size()

    # Send the image size as a 4-byte integer
    uart.write(ustruct.pack("<L", img_size))

    # Send the image data
    uart.write(img)

    # Delay for a moment between captures (you can adjust this as needed)
    pyb.delay(1000)

# Close the UART connection
uart.deinit()
