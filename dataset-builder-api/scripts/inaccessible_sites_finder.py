import time
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import a11y_audit_utils, playwright_utils, computer_vision_utils

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


csv_path = os.path.expanduser("~/Downloads/majestic_million.csv")

chunksize = 3000
URLS = []

for chunk in pd.read_csv(csv_path, usecols=['Domain'], chunksize=chunksize):
    URLS.extend(chunk['Domain'].tolist())
    if len(URLS) >= 3000:
        URLS = URLS[:3000]
        break

start_time = time.time()
MAX_RUN_TIME = 6 * 60 * 60 # 6 hours in seconds

for url in URLS:
  if (time.time() - start_time) > MAX_RUN_TIME:
      print("Max runtime reached, stopping.")
      break
  
  if not url.startswith(("http://", "https://")):
    url = "https://" + url
    
  site_id = a11y_audit_utils.url_to_id(url)
  audit_result = a11y_audit_utils.audit_site(url, site_id)
  is_inaccessible = audit_result["is_inaccessible"]
  accessibility_score = audit_result["score"]

  screenshot_file_path = os.path.join(SCREENSHOTS_DIR, f"{site_id}.png")
  webpage_screenshot_filepath = playwright_utils.take_webpage_screenshot(url, screenshot_file_path)
  entropy_value = computer_vision_utils.compute_entropy(webpage_screenshot_filepath)
  edge_density_value = computer_vision_utils.compute_edge_density(webpage_screenshot_filepath)
  is_cluttered = entropy_value > 2.5 or edge_density_value > 0.02

  if is_inaccessible or is_cluttered:
    a11y_audit_utils.save_inaccessible_site(
      url=url,
      is_inaccessible=is_inaccessible,
      accessibility_score=accessibility_score,
      is_cluttered=is_cluttered,
      entropy_value=entropy_value,
      edge_density_value=edge_density_value
    )