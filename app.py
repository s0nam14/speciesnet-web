import streamlit as st
import tempfile
import zipfile
import os
from extract_frames import extract_all_frames
from speciesnet_runner import run_speciesnet
from results_parser import generate_csv

st.set_page_config(page_title="SpeciesNet Video Classifier", layout="centered")
st.title("🦁 SpeciesNet Video Classifier")
st.write("Upload a ZIP file containing `.mp4` videos. The app will extract frames, run SpeciesNet, and give you a downloadable CSV.")

uploaded = st.file_uploader("Upload ZIP of .mp4 files", type=["zip"])

if uploaded:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "videos.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded.read())

        # Extract zip
        input_folder = os.path.join(tmpdir, "videos")
        os.makedirs(input_folder, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(input_folder)

        st.success("✅ Videos extracted.")

        # Extract frames
        frames_folder = os.path.join(tmpdir, "frames")
        st.info("Extracting frames...")
        extract_all_frames(input_folder, frames_folder)
        st.success("✅ Frames extracted.")

        # Run model
        json_output = os.path.join(tmpdir, "predictions.json")
        st.info("Running SpeciesNet model...")
        run_speciesnet(frames_folder, json_output)
        st.success("✅ Model completed.")

        # Parse results
        csv_output = os.path.join(tmpdir, "results.csv")
        generate_csv(json_output, csv_output)

        with open(csv_output, "rb") as f:
            st.download_button("📥 Download CSV Results", f, "speciesnet_results.csv", mime="text/csv")
