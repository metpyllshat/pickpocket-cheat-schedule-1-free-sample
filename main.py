import numpy as np
import pyautogui as pag
import cv2
import keyboard

region = (575, 447, 216, 14)

while True:
    screenshot = pag.screenshot(region=region)
    img_np = np.array(screenshot)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format

    # Define color ranges (you might need to adjust these)
    lower_green = np.array([0, 100, 0])  # Example:  Darker green
    upper_green = np.array([100, 255, 100])  # Example: Brighter green
    lower_white = np.array([200, 200, 200])  # Example:  Very light gray to white
    upper_white = np.array([255, 255, 255])  # Example: Pure white

    # Create masks
    mask_green = cv2.inRange(img_cv, lower_green, upper_green)
    mask_white = cv2.inRange(img_cv, lower_white, upper_white)

    # Find contours for green and white regions
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_under_green = False

    # Iterate through green contours and check for white pixels directly below
    for contour_green in contours_green:
        # Get the bounding rectangle for the green contour
        x_g, y_g, w_g, h_g = cv2.boundingRect(contour_green)

        # Iterate through white contours
        for contour_white in contours_white:
            x_w, y_w, w_w, h_w = cv2.boundingRect(contour_white)

            # Check if the x-coordinate of the white contour is within the x-range of the green contour
            # and if the y-coordinate of the white contour is below the green contour
            if (x_g <= x_w <= x_g + w_g) and (y_w > y_g + h_g):
                # Further check if the centers of the white areas are aligned with the green areas
                center_x_green = x_g + w_g // 2
                center_x_white = x_w + w_w // 2

                # Allow for a small tolerance in x-alignment (e.g., +/- 5 pixels)
                tolerance = 5
                if abs(center_x_green - center_x_white) <= tolerance:
                    white_under_green = True
                    break  # Exit the inner loop (white contours) once a match is found

        if white_under_green:
            break  # Exit the outer loop (green contours) if a match is found


    if white_under_green:
        keyboard.press('space')
        print('SPACE')
    if keyboard.is_pressed('insert'):
        print('image saved')
        screenshot.save('123.jpeg')


    # Optional: Display the image with contours (for debugging)
    # cv2.drawContours(img_cv, contours_green, -1, (0, 0, 255), 2)  # Draw green contours in red
    # cv2.drawContours(img_cv, contours_white, -1, (255, 0, 0), 2)  # Draw white contours in blue
    # cv2.imshow("Debug", img_cv)
    # if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
    #     cv2.destroyAllWindows()
    #     break