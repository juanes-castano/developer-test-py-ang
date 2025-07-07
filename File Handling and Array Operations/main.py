import os
import logging
from typing import Optional, List, Tuple
import csv
import statistics
import datetime

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import pydicom
    from pydicom.errors import InvalidDicomError
except ImportError:
    pydicom = None

try:
    from PIL import Image
    import numpy as np
except ImportError:
    Image = None
    np = None

class FileProcessor:
    def __init__(self, base_path: str, log_file: str):
        self.base_path = base_path
        self.logger = logging.getLogger("FileProcessor")
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        folder_path = os.path.join(self.base_path, folder_name)
        if not os.path.isdir(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            print(f"Error: Folder '{folder_name}' does not exist.")
            return
        items = os.listdir(folder_path)
        print(f"Total items in '{folder_name}': {len(items)}")
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                type_str = "Folder"
                size_str = "-"
            else:
                type_str = "File"
                size_str = f"{os.path.getsize(item_path) / (1024*1024):.2f} MB" if details else "-"
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d %H:%M:%S') if details else "-"
            print(f"{item} | {type_str} | Size: {size_str} | Modified: {mtime}")

    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)
        if not os.path.isfile(file_path):
            self.logger.error(f"CSV file not found: {file_path}")
            print(f"Error: File '{filename}' does not exist.")
            return
        try:
            if pd:
                df = pd.read_csv(file_path)
                print(f"Columns ({len(df.columns)}): {list(df.columns)}")
                print(f"Rows: {len(df)}")
                numeric_cols = df.select_dtypes(include='number').columns
                report_lines = []
                for col in numeric_cols:
                    mean = df[col].mean()
                    std = df[col].std()
                    print(f"{col}: mean={mean:.3f}, std={std:.3f}")
                    report_lines.append(f"{col}: mean={mean:.3f}, std={std:.3f}")
                if summary:
                    non_numeric = df.select_dtypes(exclude='number').columns
                    for col in non_numeric:
                        print(f"Summary for '{col}':")
                        value_counts = df[col].value_counts()
                        for val, count in value_counts.items():
                            print(f"  {val}: {count}")
                if report_path:
                    with open(report_path, "w") as f:
                        f.write("\n".join(report_lines))
            else:
                # Fallback to csv module
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    rows = list(reader)
                    columns = reader.fieldnames
                    print(f"Columns ({len(columns)}): {columns}")
                    print(f"Rows: {len(rows)}")
                    # Try to compute numeric stats
                    report_lines = []
                    for col in columns:
                        try:
                            values = [float(row[col]) for row in rows if row[col] != ""]
                            mean = statistics.mean(values)
                            std = statistics.stdev(values) if len(values) > 1 else 0.0
                            print(f"{col}: mean={mean:.3f}, std={std:.3f}")
                            report_lines.append(f"{col}: mean={mean:.3f}, std={std:.3f}")
                        except ValueError:
                            if summary:
                                freq = {}
                                for row in rows:
                                    val = row[col]
                                    freq[val] = freq.get(val, 0) + 1
                                print(f"Summary for '{col}':")
                                for val, count in freq.items():
                                    print(f"  {val}: {count}")
                    if report_path:
                        with open(report_path, "w") as f:
                            f.write("\n".join(report_lines))
        except Exception as e:
            self.logger.error(f"Error reading CSV: {e}")
            print(f"Error processing CSV: {e}")

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        if not pydicom:
            print("pydicom is not installed.")
            return
        file_path = os.path.join(self.base_path, filename)
        if not os.path.isfile(file_path):
            self.logger.error(f"DICOM file not found: {file_path}")
            print(f"Error: File '{filename}' does not exist.")
            return
        try:
            ds = pydicom.dcmread(file_path)
            print(f"Patient Name: {getattr(ds, 'PatientName', 'N/A')}")
            print(f"Study Date: {getattr(ds, 'StudyDate', 'N/A')}")
            print(f"Modality: {getattr(ds, 'Modality', 'N/A')}")
            if tags:
                for tag in tags:
                    try:
                        value = ds.get_item(tag)
                        print(f"Tag {tag}: {value.value if value else 'Not found'}")
                    except Exception as e:
                        print(f"Tag {tag}: Error ({e})")
            if extract_image:
                if Image is None or np is None:
                    print("PIL or numpy not installed, cannot extract image.")
                    return
                if hasattr(ds, 'pixel_array'):
                    arr = ds.pixel_array
                    # Intenta reducir el arreglo a 2D
                    arr = np.squeeze(arr)
                    if arr.ndim > 2:
                        # Si aún tiene más de 2 dimensiones, toma la primera "capa"
                        arr = arr[0]
                    # Normaliza a 0-255
                    arr = arr.astype(float)
                    arr = (arr - arr.min()) / (arr.max() - arr.min()) * 255.0
                    arr = arr.astype('uint8')
                    img = Image.fromarray(arr)
                    out_path = os.path.join(self.base_path, filename + ".png")
                    img.save(out_path)
                    print(f"Image extracted to {out_path}")
                else:
                    self.logger.error("No pixel data found in DICOM file.")
                    print("No pixel data found in DICOM file.")
        except InvalidDicomError:
                        self.logger.error(f"Invalid DICOM file: {file_path}")
                        print("Invalid DICOM file.")
        except Exception as e:
                        self.logger.error(f"Error reading DICOM: {e}")
                        print(f"Error processing DICOM: {e}")
if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(base_path, "fileprocessor.log")

    processor = FileProcessor(base_path, log_file)

    print("\n--- Contenido de la carpeta actual ---")
    processor.list_folder_contents(".", details=True)

    print("\n--- Análisis de sample-02-csv.csv ---")
    processor.read_csv("sample-02-csv.csv", report_path="csv_report.txt", summary=True)

    print("\n--- Lectura de sample-02-dicom.dcm ---")
    processor.read_dicom("sample-02-dicom.dcm", tags=[(0x0010, 0x0010), (0x0008, 0x0060)], extract_image=True)

    print("\n--- Lectura de sample-02-dicom-2.dcm ---")
    processor.read_dicom("sample-02-dicom-2.dcm", tags=[(0x0010, 0x0010), (0x0008, 0x0060)], extract_image=True)