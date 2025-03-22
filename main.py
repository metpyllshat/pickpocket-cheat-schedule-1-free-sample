import numpy as np
import pyautogui as pag
import cv2
import keyboard

region = (576, 454, 214, 6)

while True:
    screenshot = pag.screenshot(region=region)
    img_np = np.array(screenshot)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    lower_green = np.array([0, 100, 0])
    upper_green = np.array([100, 255, 100]) 
    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255]) 

    mask_green = cv2.inRange(img_cv, lower_green, upper_green)
    mask_white = cv2.inRange(img_cv, lower_white, upper_white)

    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_under_green = False

    for contour_green in contours_green:
        x_g, y_g, w_g, h_g = cv2.boundingRect(contour_green)

        for contour_white in contours_white:
            x_w, y_w, w_w, h_w = cv2.boundingRect(contour_white)

            if (x_g <= x_w <= x_g + w_g) and (y_w > y_g + h_g):
                center_x_green = x_g + w_g // 2
                center_x_white = x_w + w_w // 2

                tolerance = 5
                if abs(center_x_green - center_x_white) <= tolerance:
                    white_under_green = True
                    break 

        if white_under_green:
            break


    if white_under_green:
        keyboard.press('space')
        print('SPACE')