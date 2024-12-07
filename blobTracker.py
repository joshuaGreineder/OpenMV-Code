"""
Program is used for tracking/recognizing objects to count every unique object.
"""

import sensor
import image
import time
import math


sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

# Define the min/max LAB values we're looking for
obj_threshold = (24, 60, 32, 54, 0, 42)
dist_threshold = 10
prev_pos = []
curr_pos = []
count = 0
clock = time.clock() # Create clock object

while(True):
    clock.tick() # Advances the clock
    img = sensor.snapshot() # Takes a snapshot and saves it in memory
    img.draw_line(0,100,320,100, color= (255,255,255))
    img.draw_line(0,140,320,140, color= (255,255,255))

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([obj_threshold], area_threshold=2500, merge=True)

    # Draw blobs
    for blob in blobs:
        if (blob.cy() < 140) or blob.cy() > 100):
            # Draw a rectangle where the blob was found
            img.draw_rectangle(blob.rect(), color=(0,255,0))
            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
            curr_pos.append((blob.cx(), blob.cy()))
        else:
            # Draw a rectangle where the blob was found
            img.draw_rectangle(blob.rect(), color=(255,0,0))
            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=(255,0,0))

    for pos in curr_pos:
        new_obj = !within_range(pos)
        if new_obj:
            count = count + 1
    prev_pos = curr_pos

    print("FPS %f" % clock.fps())


def within_range(obj) -> bool:
    for pos in prev_pos:
        # Calculate the distance between the new object and the objects in prev_pos
        distance = calculate_distance(obj, pos)
        if distance < dist_threshold:  # Set a threshold for the distance
            return True  # Object is within range of a previously detected object
    return False  # Object is not within range of any previously detected object


def calculate_distance(obj1, obj2):
    distance = math.sqrt((obj2[0] - obj1[0])**2 + (obj2[1] - obj1[1])**2)
    return distance
