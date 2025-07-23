from speciesnet.scripts.run_model import run_inference_on_folders

def run_speciesnet_on_frames(frames_folder, json_output_path):
    # This runs the model inference using SpeciesNet's internal Python API
    # "folders" is a list of folders or a single folder containing images
    # It will save JSON predictions at json_output_path
    run_inference_on_folders(
        folders=[frames_folder],
        predictions_json=json_output_path,
        country="IND"
    )
