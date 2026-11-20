import os
import json
import shutil

ORIGINAL_AFS = "your_file.afs"  # Change this to match your original .afs filename
OUTPUT_AFS = "repacked_ngb.afs"

def repack_afs(manifest_path="extracted_ngb/manifest.json", out_dir="extracted_ngb"):
    shutil.copy2(ORIGINAL_AFS, OUTPUT_AFS)

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    with open(OUTPUT_AFS, "r+b") as afs:
        for entry in manifest:
            file_path = os.path.join(out_dir, entry["filename"])
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {entry['filename']} not found in the extracted directory")

            with open(file_path, "rb") as f:
                data = f.read()

            if len(data) != entry["size"]:
                raise ValueError(f"Size mismatch for {entry['filename']}: expected {entry['size']}, got {len(data)}")

            # Align to 2048-byte sectors
            padding = (2048 - len(data) % 2048) % 2048
            data += b"\x00" * padding

            afs.seek(entry["offset"])
            afs.write(data)
            print(f"Wrote {entry['filename']} at offset {entry['offset']}")

    print(f"Done! Saved game-ready archive to {OUTPUT_AFS}")

if __name__ == "__main__":
    repack_afs()
