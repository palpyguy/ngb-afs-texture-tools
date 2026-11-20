import glob
for f in sorted(glob.glob("extracted_ngb/*.bin")):
    with open(f, "rb") as fp:
        print(f, fp.seek(0, 2), fp.seek(0) or fp.read(16))
