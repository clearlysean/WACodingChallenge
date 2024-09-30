import cv2
import numpy as np

def process_colorspace(img):
    # Convert the image from BGR colorspace to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define an HSV color range for the traffic cones
    lower_color = np.array([0, 200, 140])
    upper_color = np.array([160, 255, 230])

    # Create a binary mask to black out pixels not within the specified HSV range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    return mask

def find_cone_centers(mask):
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and find all the cones
    cones = []
    for c in contours:
        # Get the moment of the contour
        M = cv2.moments(c)

        # Compute the center of the contour
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cones.append((cx, cy))

    # Convert the list of cones to a numpy array
    return np.array(cones)

def split_cones(cones, img_width):
    # Split the cones list into 2 lists containing the cones on the left and right
    left_cones = [cone for cone in cones if cone[0] < img_width / 2]
    right_cones = [cone for cone in cones if cone[0] >= img_width / 2]
    return left_cones, right_cones

def fit_and_draw_lines(img, left_cones, right_cones):
    # Fit a line to the list of left cones
    if len(left_cones) > 0:
        left_cones = np.array(left_cones)
        vx, vy, x, y = cv2.fitLine(left_cones, cv2.DIST_L2, 0, 0.01, 0.01)
        rows, cols = img.shape[:2]
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        cv2.line(img, (cols - 1, righty), (0, lefty), (0, 0, 255), 2)

    # Fit a line to the list of right cones
    if len(right_cones) > 0:
        right_cones = np.array(right_cones)
        vx, vy, x, y = cv2.fitLine(right_cones, cv2.DIST_L2, 0, 0.01, 0.01)
        rows, cols = img.shape[:2]
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        cv2.line(img, (cols - 1, righty), (0, lefty), (0, 0, 255), 2)

def main():
    # Lod the image
    img = cv2.imread("red.png")

    # Process the image colorspace to create a mask
    mask = process_colorspace(img)

    # Find the cone centers
    cones = find_cone_centers(mask)

    # Split the cones into left and right
    left_cones, right_cones = split_cones(cones, img.shape[1])

    # Fit lines and draw them on the image
    fit_and_draw_lines(img, left_cones, right_cones)

    # Write the image
    cv2.imwrite("answer.png", img)

if __name__ == "__main__":
    main()

