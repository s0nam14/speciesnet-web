# app.py
import streamlit as st
import os
import tempfile

from extract_frames import extract_all_frames
from speciesnet_runner import run_speciesnet_on_frames
from results_parser import parse_predictions_to_csv

st.title("Species Detection from Video using SpeciesNet")

uploaded_files = st.file_uploader(
    "Upload one or more .mp4 video files",
    type=["mp4"],
    accept_multiple_files=True
)

if st.button("Run Detection"):
    if not uploaded_files:
        st.warning("Please upload at least one video file.")
    else:
        with tempfile.TemporaryDirectory() as temp_input_dir, tempfile.TemporaryDirectory() as temp_output_dir:
            # Save videos to temp dir
            video_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_input_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                video_paths.append(file_path)

            st.info("Extracting frames...")
            extracted_frames = extract_all_frames(video_paths, temp_output_dir)

            if not extracted_frames:
                st.error("No frames extracted. Check your video files.")
            else:
                st.info("Running SpeciesNet model...")
                json_output = os.path.join(temp_output_dir, "predictions.json")
                try:
                    run_speciesnet_on_frames(temp_output_dir, json_output)
                    st.info("Parsing predictions...")
                    csv_output = os.path.join(temp_output_dir, "results.csv")
                    df = parse_predictions_to_csv(json_output, csv_output)
                    st.success("Detection complete!")
                    st.dataframe(df)

                    st.download_button(
                        label="Download CSV",
                        data=df.to_csv(index=False).encode(),
                        file_name="speciesnet_results.csv",
                        mime="text/csv"
                    )
                except RuntimeError as e:
                    st.error("SpeciesNet failed. See logs.")
                    st.text(str(e))
