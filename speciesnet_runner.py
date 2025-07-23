# speciesnet_runner.py
import subprocess

def run_speciesnet_on_frames(frames_folder, json_output_path):
    command = [
        "python", "-m", "speciesnet.scripts.run_model",
        "--folders", frames_folder,
        "--predictions_json", json_output_path,
        "--country", "IND"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("SpeciesNet STDOUT:\n", result.stdout)
    print("SpeciesNet STDERR:\n", result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"SpeciesNet failed with code {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
