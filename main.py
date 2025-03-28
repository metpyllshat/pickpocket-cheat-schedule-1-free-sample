import mss
import mss.tools
import numpy as np
from numba import njit, prange
import time
import keyboard

# Define the region of interest (x, y, width, height)
region = (528, 484, 310, 9)

# Pre-calculate the bounding box for mss
sct_box = {'left': region[0], 'top': region[1], 'width': region[2], 'height': region[3]}

# Optimized color range checks using Numba
@njit(fastmath=True)
def is_green(pixel):
    return 0 <= pixel[0] <= 100 and 100 <= pixel[1] <= 255 and 0 <= pixel[2] <= 100

@njit(fastmath=True)
def is_white(pixel):
    return 200 <= pixel[0] <= 255 and 200 <= pixel[1] <= 255 and 200 <= pixel[2] <= 255



@njit(parallel=True)
def process_image(img_np):
    height, width = img_np.shape[:2]
    white_under_green = False

    for y in prange(height):
        for x in range(width):
            if is_green(img_np[y, x]):
                for y2 in range(y + 1, height):  # Start searching for white below green
                    for x2 in range(max(0, x - 5), min(width, x + 6)): # Limit search range
                        if is_white(img_np[y2, x2]):
                            white_under_green = True
                            break
                    if white_under_green:
                        break
            if white_under_green:
                break
        if white_under_green:
            break

    return white_under_green


def main():
    with mss.mss() as sct:
        while True:
            pressed=False
            # Capture the screen region quickly
            sct_img = sct.grab(sct_box)
            img_np = np.array(sct_img, dtype=np.uint8)[:, :, :3]  # Keep only RGB, discard alpha
            
            if process_image(img_np) and not(pressed):
                keyboard.send('space')
                print('SPACE')
                pressed=True
                time.sleep(5)
                pressed=False

            # Reduce CPU usage when not detecting
            #time.sleep(0.01)  # You can add a small delay if needed, but keep it very short

if __name__ == '__main__':
    main()