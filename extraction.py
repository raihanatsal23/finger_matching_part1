import cv2
import numpy as np
import csv
import os
from skimage.morphology import skeletonize, remove_small_objects
from skimage.morphology import convex_hull_image, erosion, square, thin
from skimage import measure
import math
import matplotlib.pyplot as plt

class MinutiaeFeature:
    def __init__(self, locX, locY, Orientation, Type):
        self.locX = locX
        self.locY = locY
        self.Orientation = Orientation
        self.Type = Type

    def __repr__(self):
        return f' locX:{self.locX} locY:{self.locY}  Orientation:{self.Orientation}'

class FingerprintFeatureExtractor:
    def __init__(self):
        self._mask = []
        self._skel = []
        self.minutiaeTerm = []
        self.minutiaeBif = []

    def __skeletonize(self, img):
        img = np.uint8(img > 128)
        skeleton = thin(img)  # Using thin instead of skeletonize for finer structure
        self._skel = np.uint8(skeleton) * 255
        self._mask = img * 255

    def __computeAngle(self, block, minutiaeType):
        angle = []
        (blkRows, blkCols) = np.shape(block)
        CenterX, CenterY = (blkRows - 1) / 2, (blkCols - 1) / 2
        if minutiaeType.lower() == 'termination':
            sumVal = 0
            for i in range(blkRows):
                for j in range(blkCols):
                    if (i == 0 or i == blkRows - 1 or j == 0 or j == blkCols - 1) and block[i][j] != 0:
                        angle.append(-math.degrees(math.atan2(i - CenterY, j - CenterX)))
                        sumVal += 1
                        if sumVal > 1:
                            angle.append(float('nan'))
            return angle
        elif minutiaeType.lower() == 'bifurcation':
            angle = []
            sumVal = 0
            for i in range(blkRows):
                for j in range(blkCols):
                    if (i == 0 or i == blkRows - 1 or j == 0 or j == blkCols - 1) and block[i][j] != 0:
                        angle.append(-math.degrees(math.atan2(i - CenterY, j - CenterX)))
                        sumVal += 1
            if sumVal != 3:
                angle.append(float('nan'))
            return angle

    def __getTerminationBifurcation(self):
        self._skel = self._skel == 255
        (rows, cols) = self._skel.shape
        self.minutiaeTerm = np.zeros(self._skel.shape)
        self.minutiaeBif = np.zeros(self._skel.shape)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if self._skel[i][j] == 1:
                    block = self._skel[i - 1:i + 2, j - 1:j + 2]
                    block_val = np.sum(block)
                    if block_val == 2:
                        self.minutiaeTerm[i, j] = 1
                    elif block_val == 4:
                        self.minutiaeBif[i, j] = 1

        self._mask = convex_hull_image(self._mask > 0)
        self._mask = erosion(self._mask, square(5))
        self.minutiaeTerm = np.uint8(self._mask) * self.minutiaeTerm

    def extractMinutiaeFeatures(self, img):
        self.__skeletonize(img)
        self.__getTerminationBifurcation()

        TermLabel = measure.label(self.minutiaeTerm, connectivity=2)
        BifLabel = measure.label(self.minutiaeBif, connectivity=2)

        FeaturesTerm = self.__extractFeatures(TermLabel, 'Termination')
        FeaturesBif = self.__extractFeatures(BifLabel, 'Bifurcation')

        return FeaturesTerm, FeaturesBif

    def __extractFeatures(self, label_image, minutiaeType):
        features = []
        for region in measure.regionprops(label_image):
            (row, col) = np.int16(np.round(region.centroid))
            block = self._skel[row - 1:row + 2, col - 1:col + 2]
            angle = self.__computeAngle(block, minutiaeType)
            if (minutiaeType == 'Termination' and len(angle) == 1) or (minutiaeType == 'Bifurcation' and len(angle) == 3):
                features.append(MinutiaeFeature(row, col, angle, minutiaeType))
        return features

def process_image(filepath, output_sub_dir, csv_writer):
    # Step 1: Load image
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    # Step 2: Noise reduction
    denoised_img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)

    # Step 3: CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_contrast = clahe.apply(denoised_img)

    # Step 4: Adaptive thresholding
    binary = cv2.adaptiveThreshold(
        enhanced_contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 15, 8
    )

    # Step 5: Morphological operations for cleaning
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    # Step 6: Skeletonization
    skeleton = thin(binary > 0).astype(np.uint8) * 255

    # Save the preprocessed image without minutiae points
    preprocess_output_path = f"{output_sub_dir}/{os.path.basename(filepath).split('.')[0]}_preprocess.png"
    cv2.imwrite(preprocess_output_path, skeleton)

    # Step 7: Minutiae Extraction
    feature_extractor = FingerprintFeatureExtractor()
    ridge_endings, bifurcations = feature_extractor.extractMinutiaeFeatures(skeleton)

    # Step 8: Save minutiae to CSV
    for minutiae in ridge_endings:
        csv_writer.writerow([os.path.basename(filepath), 'ridge_ending', minutiae.locX, minutiae.locY, minutiae.Orientation[0]])
    for minutiae in bifurcations:
        csv_writer.writerow([os.path.basename(filepath), 'bifurcation', minutiae.locX, minutiae.locY, minutiae.Orientation[0]])

    # Step 9: Visualize Minutiae
    visualize_minutiae(skeleton, ridge_endings, bifurcations, f"{output_sub_dir}/{os.path.basename(filepath).split('.')[0]}_minutiae.png")

def visualize_minutiae(skeleton, ridge_endings, bifurcations, output_path):
    minutiae_image = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
    for minutiae in ridge_endings:
        cv2.circle(minutiae_image, (minutiae.locY, minutiae.locX), 3, (0, 0, 255), -1)  # Red for ridge endings
    for minutiae in bifurcations:
        cv2.circle(minutiae_image, (minutiae.locY, minutiae.locX), 3, (255, 0, 0), -1)  # Blue for bifurcations
    cv2.imwrite(output_path, minutiae_image)

def main():
    input_dir = "./input/"
    output_dir = "./output/"
    csv_file = "./output/minutiae_data.csv"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open CSV file and write header
    with open(csv_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Image", "Minutiae Type", "X", "Y", "Orientation"])

        # Loop through each subdirectory in the input directory
        for sub_dir in os.listdir(input_dir):
            sub_dir_path = os.path.join(input_dir, sub_dir)

            # Check if the item is a directory
            if os.path.isdir(sub_dir_path):
                output_sub_dir = os.path.join(output_dir, sub_dir)
                os.makedirs(output_sub_dir, exist_ok=True)

                for filename in os.listdir(sub_dir_path):
                    if filename.endswith(".tif"):
                        filepath = os.path.join(sub_dir_path, filename)
                        process_image(filepath, output_sub_dir, csv_writer)

if __name__ == "__main__":
    main()


