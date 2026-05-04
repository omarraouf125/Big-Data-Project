"""
Setup script for Apache Spark + Hadoop (Windows) for Big-Data-Project.

What this does:
  1. pip-installs pyspark 3.5.1 and findspark
  2. Creates A:\spark  → junction to the bundled Spark inside pyspark's package
  3. Creates A:\hadoop\bin and downloads winutils.exe + hadoop.dll (Hadoop 3.3.6)
     so PySpark can write temp files on Windows without errors.

Run once:  python setup_spark.py
"""

import os
import sys
import subprocess
import urllib.request
import shutil


# ── 1. Install Python packages ──────────────────────────────────────────────
print("=" * 60)
print("Step 1: Installing pyspark and findspark …")
print("=" * 60)
subprocess.check_call([sys.executable, "-m", "pip", "install",
                       "pyspark==3.5.1", "findspark", "--quiet"])
print("pyspark and findspark installed.\n")


# ── 2. Locate the Spark home bundled inside pyspark ─────────────────────────
import pyspark  # noqa: E402  (just installed above)

PYSPARK_SPARK_HOME = os.path.join(os.path.dirname(pyspark.__file__))
print(f"PySpark package directory: {PYSPARK_SPARK_HOME}")

SPARK_TARGET = r"A:\spark"

# ── 3. Create A:\spark as a directory junction (no copy needed) ───────────────
print("\n" + "=" * 60)
print(f"Step 2: Creating junction  {SPARK_TARGET}  →  {PYSPARK_SPARK_HOME}")
print("=" * 60)

if os.path.exists(SPARK_TARGET) or os.path.islink(SPARK_TARGET):
    print(f"  '{SPARK_TARGET}' already exists – skipping.")
else:
    # mklink /J creates a directory junction (no admin needed on most setups)
    result = subprocess.run(
        ["cmd", "/c", f'mklink /J "{SPARK_TARGET}" "{PYSPARK_SPARK_HOME}"'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  Junction created: {result.stdout.strip()}")
    else:
        # Fallback: copy the directory (slow but always works)
        print(f"  Junction failed ({result.stderr.strip()}); falling back to full copy …")
        shutil.copytree(PYSPARK_SPARK_HOME, SPARK_TARGET)
        print(f"  Copied Spark to {SPARK_TARGET}")

print(f"  A:\\spark exists: {os.path.isdir(SPARK_TARGET)}\n")


# ── 4. Download winutils + hadoop.dll to A:\hadoop\bin ───────────────────────
HADOOP_BIN = r"A:\hadoop\bin"
os.makedirs(HADOOP_BIN, exist_ok=True)

# Pre-built binaries from https://github.com/cdarlint/winutils (Hadoop 3.3.6)
BASE_URL = (
    "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.6/bin/"
)
FILES = ["winutils.exe", "hadoop.dll"]

print("=" * 60)
print(f"Step 3: Downloading Hadoop Windows binaries to {HADOOP_BIN}")
print("=" * 60)

for fname in FILES:
    dest = os.path.join(HADOOP_BIN, fname)
    if os.path.exists(dest):
        print(f"  {fname} already present – skipping.")
        continue
    url = BASE_URL + fname
    print(f"  Downloading {fname} …", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, \
             open(dest, "wb") as out:
            shutil.copyfileobj(resp, out)
        size_kb = os.path.getsize(dest) // 1024
        print(f"done ({size_kb} KB)")
    except Exception as exc:
        print(f"FAILED: {exc}")
        print(f"  Please download {fname} manually from:\n    {url}")
        print(f"  and place it in {HADOOP_BIN}")

print()


# ── 5. Verify ────────────────────────────────────────────────────────────────
print("=" * 60)
print("Verification")
print("=" * 60)
hadoop_root = r"A:\hadoop"
print(f"  A:\\spark   exists : {os.path.isdir(SPARK_TARGET)}")
print(f"  A:\\hadoop  exists : {os.path.isdir(hadoop_root)}")
for fname in FILES:
    dest = os.path.join(HADOOP_BIN, fname)
    print(f"  {HADOOP_BIN}\\{fname} : {'OK' if os.path.exists(dest) else 'MISSING'}")

# Quick Spark smoke-test
print()
print("Running Spark smoke-test …")
try:
    os.environ["HADOOP_HOME"] = r"A:\hadoop"
    os.environ["SPARK_HOME"] = SPARK_TARGET
    os.environ["PATH"] = HADOOP_BIN + ";" + os.environ.get("PATH", "")
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    import findspark
    findspark.init()

    from pyspark.sql import SparkSession
    spark = (
        SparkSession.builder
        .appName("smoke_test")
        .master("local[1]")
        .config("spark.driver.memory", "1g")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.createDataFrame([(1, "hello"), (2, "world")], ["id", "val"])
    count = df.count()
    spark.stop()
    print(f"  Smoke-test PASSED (counted {count} rows, Spark {spark.version})")
except Exception as exc:
    print(f"  Smoke-test FAILED: {exc}")
    print("  Check the error above; the notebook may still work.")

print()
print("Setup complete.  You can now run 01_preprocessing.ipynb.")
