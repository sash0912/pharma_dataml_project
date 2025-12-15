import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
REPORT_DIR = "docs"

os.makedirs(REPORT_DIR, exist_ok=True)

report_lines = []
report_lines.append("# Data Profiling Report\n")

for file in os.listdir(RAW_DATA_DIR):
    if file.endswith(".csv"):
        file_path = os.path.join(RAW_DATA_DIR, file)
        report_lines.append(f"\n## Dataset: {file}\n")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            report_lines.append(f"❌ Error reading file: {e}\n")
            continue

        report_lines.append(f"- Number of rows: {df.shape[0]}")
        report_lines.append(f"- Number of columns: {df.shape[1]}\n")

        report_lines.append("### Columns & Data Types\n")
        for col, dtype in df.dtypes.items():
            report_lines.append(f"- {col}: {dtype}")

        report_lines.append("\n### Missing Values\n")
        missing = df.isnull().sum()
        for col, count in missing.items():
            report_lines.append(f"- {col}: {count}")

        report_lines.append("\n### Sample Rows\n")
        report_lines.append(df.head(5).to_markdown(index=False))

with open(os.path.join(REPORT_DIR, "data_profiling_report.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("Data profiling completed. Report saved to docs/data_profiling_report.md")
