
import json
import os
import subprocess
from pathlib import Path

def test_silt_detect_json_examples_config() -> None:
    # silence TF noise in test output
    env = os.environ.copy()
    env["TF_CPP_MIN_LOG_LEVEL"] = "2"
    env["TF_ENABLE_ONEDNN_OPTS"] = "0"

    repo_root = Path(__file__).resolve().parents[1]
    cfg = repo_root / "examples" / "silt_config.yaml"
    assert cfg.exists()
    
    # run installed console script via current interpreter
    proc = subprocess.run(
        ["pyhydrointel", "silt-detect", "-c", str(cfg), "--json"],
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    assert proc.stdout.strip(), f"Empty stdout.\nSTDERR:\n{proc.stderr}"
    data = json.loads(proc.stdout)

    # keys present
    assert set(data) == {"image_path", "silt_ratio", "silt_height_m"}

    # exact expected result from the run
    assert data["silt_ratio"] == 0.15
    assert data["silt_height_m"] == 0.03

    # output image created and matches expected name
    img_path = Path(data["image_path"])
    assert img_path.exists()
    assert img_path.name == "dry_csz0.20_slope0.0072.png"