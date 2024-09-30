## Output image
![Answer Image](answer.png)

## Methodology

1. **Loading the Image**:
   - The image (`red.png`) is loaded using OpenCV.

2. **Preprocessing and Finding Cone Centers**:
   - The image is converted from its BGR to an HSV color space to make color segmentation easier.
   - A specific HSV range is defined to detect the color of the traffic cones, and a binary mask is created to focus solely on the pixels within this range.
   - Contours are extracted from the binary mask, and the centroids of each contour are calculated to determine the positions of the traffic cones.

3. **Splitting Cones and Fitting Lines**:
   - The cone centroids are split into left and right groups based off of their x-coordinates relative to the image width for line-fitting.
   - A line is fitted to the left and right groups of cones using the least-squares, then the fitted lines are then drawn on the original image.

4. **Saving the Output**:
   - The final image, with the lines drawn, is saved as `answer.png`.

## What Did You Try and Why Do You Think It Did Not Work?

- **Initial Thresholding Attempts**:
  - Initially, a different HSV range was used to segment the cones, but it was not robust enough under different lighting conditions, leading to missing or incorrectly detected cones. Adjusting the HSV values to better match the cone colors in different lighting conditions improved the accuracy of detection.
  
- **Contour Filtering**:
  - At first, no filtering was applied to the detected contours, resulting in false positives due to noise in the image. Adding a condition to calculate the centroid only when the contour area (`M["m00"]`) was non-zero solved this issue.

## Libraries Used

- OpenCV, NumPy

