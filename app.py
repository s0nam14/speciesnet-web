import streamlit as st
import tempfile
import os
import json
import pandas as pd
import subprocess
from extract_frame import extract_frames_from_video

st.set_page_config(page_title="SpeciesNet Video Analyzer")
st.title("🎥🐾 SpeciesNet Video Analyzer")
st.markdown("Upload videos to detect species using the SpeciesNet model.")

uploaded_files = st.file_uploader("Upload one or more .mp4 videos", type=["mp4"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Run Species Detection"):
        with st.spinner("Processing videos and predicting species..."):

            with tempfile.TemporaryDirectory() as video_dir, tempfile.TemporaryDirectory() as frames_dir:
                for uploaded_file in uploaded_files:
                    video_path = os.path.join(video_dir, uploaded_file.name)
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.read())
                    extract_frames_from_video((video_path, frames_dir))

                output_json = os.path.join(frames_dir, "speciesnet_output.json")
                subprocess.run([
                    "python", "-m", "speciesnet.scripts.run_model",
                    "--folders", frames_dir,
                    "--predictions_json", output_json,
                    "--country", "IND"
                ], check=True)

                with open(output_json, 'r') as f:
                    predictions = json.load(f)["predictions"]

                video_to_species = {}
                for item in predictions:
                    img_file = os.path.basename(item["filepath"])
                    video_name = "_".join(img_file.split("_")[:-1]) + ".mp4"
                    species = item.get("prediction", "N/A")
                    video_to_species.setdefault(video_name, set()).add(species)

                data = [{"Video File": vid, "Detected Species": ", ".join(species)} for vid, species in video_to_species.items()]
                df = pd.DataFrame(data)
                st.success("Detection complete! 🎉")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv, file_name="speciesnet_results.csv", mime="text/csv")

                with open(output_json, 'rb') as f:
                    st.download_button("📄 Download Raw JSON", f, file_name="speciesnet_output.json", mime="application/json")
