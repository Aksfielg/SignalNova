import zipfile
import os

with zipfile.ZipFile('PS7_ExoplanetDetection_Submission.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk('ps7_exoplanet'):
        if 'data\\raw' in root or 'data/raw' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            # Use forward slashes for zip internal paths
            arcname = filepath.replace('\\', '/')
            z.write(filepath, arcname)

size_kb = os.path.getsize('PS7_ExoplanetDetection_Submission.zip') / 1024
print(f"ZIP Size: {size_kb:.2f} KB")

with zipfile.ZipFile('PS7_ExoplanetDetection_Submission.zip', 'r') as z:
    for f in z.namelist()[:40]:
        print(f)
