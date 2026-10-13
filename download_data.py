from pathlib import Path
from spacex_pipeline import collect_launch_table

out = Path(__file__).resolve().parents[1] / "data"
out.mkdir(exist_ok=True)
df = collect_launch_table()
path = out / "spacex_launches_raw.csv"
df.to_csv(path, index=False)
print(f"Saved {len(df)} launch rows to {path}")
