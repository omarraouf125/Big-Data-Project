import urllib.request
import os

dataset_dir = "Dataset"
base_url = "https://datasets.imdbws.com/"

files = [
    "title.basics.tsv.gz",
    "title.ratings.tsv.gz",
    "title.principals.tsv.gz",
    "title.crew.tsv.gz",
    "title.akas.tsv.gz",
    "title.episode.tsv.gz",
    "name.basics.tsv.gz",
]

for f in files:
    dest = os.path.join(dataset_dir, f)
    if os.path.exists(dest):
        print(f"[SKIP] {f} already exists")
        continue
    url = base_url + f
    print(f"[DOWNLOAD] {f} ...")
    urllib.request.urlretrieve(url, dest)
    size_mb = os.path.getsize(dest) / (1024*1024)
    print(f"[DONE] {f} ({size_mb:.1f} MB)")

print("\nAll downloads complete!")
for f in files:
    dest = os.path.join(dataset_dir, f)
    if os.path.exists(dest):
        size_mb = os.path.getsize(dest) / (1024*1024)
        print(f"  {f}: {size_mb:.1f} MB")
