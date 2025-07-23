import streamlit as st
import os
import tempfile
import shutil

from extract_frames import extract_all_frames
from speciesnet_runner import run_speciesnet_on_frames
from results_parser import parse_predictions_to_csv

st.title("SpeciesNet Video Species Detector")

uploaded_files = st.file_uploader(
    "Upload multiple .mp4 video files",
    accept_multiple_files=True,
    type=["mp4"]
)

if st.button("Run Detection"):
    if not uploaded_files:
        st.warning("Please upload at least one video file.")
    else:
        with tempfile.TemporaryDirectory() as tmp_input_dir, tempfile.TemporaryDirectory() as tmp_output_dir:
            # Save uploaded videos to temp input folder
            video_paths = []
            for uploaded_file in uploaded_files:
                path = os.path.join(tmp_input_dir, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                video_paths.append(path)
            
            st.info("Extracting frames from videos...")
            video_frames = extract_all_frames(video_paths, tmp_output_dir)
            
            st.info("Running SpeciesNet model on extracted frames...")
            json_output_path = os.path.join(tmp_output_dir, "speciesnet_predictions.json")
            run_speciesnet_on_frames(tmp_output_dir, json_output_path)
            
            st.info("Parsing results...")
            df = parse_predictions_to_csv(json_output_path, os.path.join(tmp_output_dir, "results.csv"))
            
            st.success("Detection completed!")
            st.dataframe(df)
            
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV results",
                data=csv_data,
                file_name="speciesnet_results.csv",
                mime="text/csv"
            )
