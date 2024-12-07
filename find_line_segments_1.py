
import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)  # Grayscale is faster
sensor.set_framesize(sensor.QQVGA)
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
    img = sensor.snapshot().histeq(adaptive=True, clip_limit=1).lens_corr(strength=1.2).laplacian(1, sharpen=True)

    radius = 1
    target_color = 255  # Target grayscale value
    color_tolerance = 80

    lines = img.find_line_segments(merge_distance=30, max_theta_diff=70)
    if lines:
        for l in lines:
            if l and has_color_in_radius(img, int(l.x1()), int(l.y1()), radius, target_color, color_tolerance):
                img.draw_line(l.line(), color=255)

    print("FPS %f" % clock.fps())
