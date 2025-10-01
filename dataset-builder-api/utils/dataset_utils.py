import os
from app import DATASET_FOLDER
import uuid

def save_screenshot_to_dataset(label, file):
    label_folder = os.path.join(DATASET_FOLDER, label)
    os.makedirs(label_folder, exist_ok=True)

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(label_folder, filename)

    file.save(filepath)