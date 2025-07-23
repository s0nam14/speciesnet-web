import json
import csv
import os

def generate_csv(json_path, csv_path):
    with open(json_path) as f:
        data = json.load(f)

    preds = data.get("predictions", [])
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Video", "Species Prediction"])
        for p in preds:
            filepath = p.get("filepath", "")
            video = os.path.basename(filepath).split("_")[0] + ".mp4"
            prediction = p.get("classifications", {}).get("classes", ["Unknown"])[0]
            writer.writerow([video, prediction])
