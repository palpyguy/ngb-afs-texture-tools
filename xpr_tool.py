import sys, struct, glob, os

def extract_xpr():
    for bin_path in sorted(glob.glob("extracted_ngb/*.bin")):
        with open(bin_path, "rb") as f:
            data = f.read()
        idx = data.find(b"XPR0")
        if idx == -1:
            continue
        xpr_size = struct.unpack_from("<I", data, idx + 4)[0]
        xpr_path = bin_path.replace(".bin", ".xpr")
        with open(xpr_path, "wb") as out:
            out.write(data[idx : idx + xpr_size])
        print(f"Extracted {xpr_path} ({xpr_size} bytes)")

def inject_xpr():
    for xpr_path in sorted(glob.glob("extracted_ngb/*.xpr")):
        bin_path = xpr_path.replace(".xpr", ".bin")
        with open(bin_path, "rb") as f:
            bin_data = bytearray(f.read())
        with open(xpr_path, "rb") as f:
            xpr_data = f.read()
        idx = bin_data.find(b"XPR0")
        orig_size = struct.unpack_from("<I", bin_data, idx + 4)[0]
        if len(xpr_data) != orig_size:
            raise ValueError(f"Size mismatch for {xpr_path}: expected {orig_size}, got {len(xpr_data)}")
        bin_data[idx : idx + orig_size] = xpr_data
        with open(bin_path, "wb") as out:
            out.write(bin_data)
        print(f"Injected {xpr_path} back into {bin_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "inject":
        inject_xpr()
    else:
        extract_xpr()
