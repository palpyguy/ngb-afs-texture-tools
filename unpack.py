import os
import struct
import json

def extract_afs(afs_path, out_dir="extracted_ngb"):
    os.makedirs(out_dir, exist_ok=True)
    
    with open(afs_path, "rb") as f:
        data = f.read()

    if data[:4] != b"AFS\x00":
        raise ValueError("Not a valid AFS file")

    # Read file count
    file_count = struct.unpack_from("<I", data, 4)[0]
    print(f"Found {file_count} entries in AFS.")

    # Read offset/size table
    offsets_sizes = []
    for i in range(file_count):
        offset, size = struct.unpack_from("<II", data, 8 + i * 8)
        offsets_sizes.append((offset, size))

    # Extract files
    manifest = []
    for i, (offset, size) in enumerate(offsets_sizes):
        if offset == 0 or size == 0:
            continue

        chunk = data[offset : offset + size]
        base_name = f"{i:04d}_entry.bin"

        file_path = os.path.join(out_dir, base_name)
        with open(file_path, "wb") as out_f:
            out_f.write(chunk)

        manifest.append({
            "index": i,
            "filename": base_name,
            "offset": offset,
            "size": size
        })

    # Save manifest
    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

if __name__ == "__main__":
    extract_afs("your_file.afs")
