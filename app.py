import streamlit as st
import os, uuid, shutil, json, subprocess
import pandas as pd
from utils import extract_frames_from_video

# Paths
UPLOAD_DIR = "uploaded_videos"
FRAME_DIR = "extracted_frames"
PRED_JSON = "output/predictions.json"
PRED_CSV = "output/predictions.csv"

# Setup
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("🦁 Animal Species Detector (SpeciesNet)")
st.write("Upload camera trap videos (.mp4) and detect species using SpeciesNet.")

# File uploader
uploaded_files = st.file_uploader("Upload .mp4 videos", type=["mp4"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Run Detection"):
        # Clean old data
        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
        shutil.rmtree(FRAME_DIR, ignore_errors=True)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(FRAME_DIR, exist_ok=True)

        st.info("📽️ Extracting frames...")
        for uploaded_file in uploaded_files:
            video_id = str(uuid.uuid4())
            video_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())
            extract_frames_from_video(video_path, video_id, FRAME_DIR)

        st.success("✅ Frames extracted!")

        # Run SpeciesNet
        st.info("🐾 Running SpeciesNet...")
        command = f"python -m speciesnet.scripts.run_model --folders {FRAME_DIR} --predictions_json {PRED_JSON} --country IND"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Debug info
        st.text("SpeciesNet Output:")
        st.code(result.stdout + result.stderr)

        # Check output
        if not os.path.exists(PRED_JSON):
            st.error("❌ No predictions.json file found. SpeciesNet may have failed.")
        else:
            with open(PRED_JSON, 'r') as f:
                data = json.load(f)
            results = []
            for item in data["predictions"]:
                species = item.get("prediction", "Unknown")
                video_name = os.path.basename(item["filepath"]).split('_')[0]
                results.append((video_name, species))
            df = pd.DataFrame(results, columns=["Video", "Species"]).drop_duplicates()
            df.to_csv(PRED_CSV, index=False)

            st.success("✅ SpeciesNet completed!")
            st.dataframe(df)
            st.download_button("📥 Download CSV", df.to_csv(index=False), "species_predictions.csv", "text/csv")
