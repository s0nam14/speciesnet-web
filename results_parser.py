import json
import pandas as pd

def parse_predictions_to_csv(json_file, csv_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    rows = []
    for pred in data.get("predictions", []):
        filepath = pred.get("filepath", "")
        classes = pred.get("classifications", {}).get("classes", [])
        # You can customize extraction as needed; here we take top class only
        top_class = classes[0] if classes else "Unknown"
        video_name = filepath.split('_')[0]  # assuming filename format videoName_XXXX.jpg
        rows.append({
            "video": video_name,
            "predicted_class": top_class
        })

    df = pd.DataFrame(rows)
    df.to_csv(csv_file, index=False)
    return df
