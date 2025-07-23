import subprocess

def run_speciesnet(frames_dir: str, output_json: str):
    cmd = [
        "python", "-m", "speciesnet.scripts.run_model",
        "--folders", frames_dir,
        "--predictions_json", output_json,
        "--country", "IND"
    ]
    subprocess.run(cmd, check=True)
