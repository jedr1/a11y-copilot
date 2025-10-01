import os
import subprocess
import json
from pathlib import Path
import re

OUTPUT_DIR="audits"
INACCESSIBLE_SITES_FILE = Path("inaccessible_sites.json")

ACCESSIBLE_REQUIRED_SCORE = 0.7

def audit_site(url, site_id):
  result_path = os.path.join(OUTPUT_DIR, f"{site_id}.json")
  cmd = f"npx lighthouse {url} --quiet --chrome-flags='--headless' --only-categories=accessibility --output=json --output-path={result_path}"

  subprocess.run(cmd, shell=True, check=False)

  try:
    with open(result_path, "r") as f:
      report = json.load(f)
    score = report["categories"]["accessibility"]["score"]
    return {
      "is_inaccessible": score < ACCESSIBLE_REQUIRED_SCORE,
      "score": score
    }
  
  except Exception as e:
    print(f"Error parsing result for {url}: {e}")


def url_to_id(url):
  return re.sub(r"[^a-zA-Z0-9]", "_", url)

def save_inaccessible_site(url, is_inaccessible, accessibility_score, entropy_value, edge_density_value, is_cluttered):
  site_report = {
      "url": url,
      "is_inaccessible": bool(is_inaccessible),           # convert NumPy bool
      "accessibility_score": float(accessibility_score), # convert NumPy float
      "is_cluttered": bool(is_cluttered),
      "entropy_value": float(entropy_value),
      "edge_density_value": float(edge_density_value)
  }

  if INACCESSIBLE_SITES_FILE.exists():
     with open(INACCESSIBLE_SITES_FILE, "r") as f:
        data = json.load(f)
  else:
     data = []

  data.append(site_report)

  with open(INACCESSIBLE_SITES_FILE, "w") as f:
     json.dump(data, f, indent=2)
  
  print(f"Inaccessible site saved: {url} (is_inaccessible={is_inaccessible}, is_cluttered={is_cluttered})")