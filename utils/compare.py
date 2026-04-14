import cv2
import os
import numpy as np

# Compare two images
def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    img1 = cv2.resize(img1, (200, 200))
    img2 = cv2.resize(img2, (200, 200))

    diff = cv2.absdiff(img1, img2)
    mse = np.mean(diff ** 2)

    return mse


# Detect logo
def detect_logo(upload_path):
    best_score = float("inf")
    best_match = None

    for logo in os.listdir("logos"):
        logo_path = os.path.join("logos", logo)

        score = compare_images(upload_path, logo_path)

        if score < best_score:
            best_score = score
            best_match = logo

    if best_score < 1000:
        return "Original Logo", best_match, best_score
    else:
        return "Fake Logo", best_match, best_score