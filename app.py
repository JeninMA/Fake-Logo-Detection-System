import streamlit as st
import cv2
import numpy as np
import os
import tempfile

# -------------------------------
# Function: Compare Images (MSE)
# -------------------------------
def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    # ✅ Safety check (prevents crash)
    if img1 is None:
        st.error(f"Error loading uploaded image: {img1_path}")
        return float("inf")

    if img2 is None:
        st.warning(f"Skipping invalid logo file: {img2_path}")
        return float("inf")

    # Resize images
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    # Calculate MSE
    diff = cv2.absdiff(img1, img2)
    mse = np.mean(diff ** 2)

    return mse


# -------------------------------
# Function: Detect Logo
# -------------------------------
def detect_logo(upload_path):
    best_score = float("inf")
    best_match = None

    for logo in os.listdir("logos"):
        logo_path = os.path.join("logos", logo)

        score = compare_images(upload_path, logo_path)

        if score < best_score:
            best_score = score
            best_match = logo

    # Decision threshold
    if best_score < 5:
        return "Original Logo", best_match, best_score
    else:
        return "Fake Logo", best_match, best_score


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Fake Logo Detection", layout="centered")

st.title("🛡️ Fake Logo Detection System")
st.write("Upload a logo image to check whether it is **Original or Fake**.")

uploaded_file = st.file_uploader("Upload Logo Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Show uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # ✅ Proper temp file saving
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    if st.button("Check Logo"):
        result, match, score = detect_logo(temp_path)

        # Show result
        st.subheader("Result:")
        st.success(result)

        # Extra details
        st.write(f"**Matched with:** {match}")
        st.write(f"**Similarity Score (lower = better):** {score:.2f}")