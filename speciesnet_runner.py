import subprocess

def run_speciesnet(frames_dir: str, output_json: str):
    cmd = [
        "python", "-m", "speciesnet.scripts.run_model",
        "--folders", frames_dir,
        "--predictions_json", output_json,
        "--country", "IND"
    ]
    print("Running command:", " ".join(cmd))  # DEBUG
    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)  # DEBUG
    print("STDERR:", result.stderr)  # DEBUG

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=result.args,
            output=result.stdout,
            stderr=result.stderr
        )
