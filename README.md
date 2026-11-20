# Ninja Gaiden Black (Xbox) — AFS & XPR Texture Modding Toolkit

A collection of Python scripts for extracting, inspecting, modifying, and safely repacking textures from Original Xbox **Ninja Gaiden Black** `.afs` archives.

## Features
* **AFS Unpacking (`unpack.py`):** Extracts files from Team Ninja `.afs` archives and generates a `manifest.json` tracking exact file offsets and sizes.
* **XPR Container Slicing (`xpr_tool.py`):** Scans extracted KMD/model files for embedded Xbox `XPR0` texture headers and extracts them into standalone `.xpr` files (and reinjects modified ones).
* **Safe In-Place Repacking (`repack.py`):** Patches modified files back into the original `.afs` archive using `manifest.json` offsets to preserve archive alignment and prevent game crashes.
* **Archive Inspection (`check.py`):** Quickly inspects file headers and structure inside `.afs` and extracted containers.

## Prerequisites
* **Python 3.8+** (uses standard library modules; no extra pip packages required unless noted)
* **GreedXplorer** (for converting `.xpr` textures to `.dds` and re-importing edited `.dds` files back into `.xpr`)
* A **`.dds` capable image editor** (such as GIMP, Paint.NET, or Photoshop with the NVIDIA/Intel DDS plugin) I use PhotoCraft
* Legally dumped **Ninja Gaiden Black (Original Xbox)** `.afs` files (e.g., `databin.afs`)

## Modding Workflow

### 1. Unpack the `.afs` Archive
Place your target `.afs` file in your working directory and run:
```bash
python unpack.py databin.afs
```
This extracts the contents into an output folder and creates a `manifest.json` file. **Keep `manifest.json` safe—it is required for repacking.**

### 2. Extract `.xpr` Textures
Run the XPR extraction tool against the unpacked files to slice out the `XPR0` texture containers:
```bash
python xpr_tool.py extract
```

### 3. Convert & Edit Textures
1. Open the extracted `.xpr` file in **GreedXplorer**.
2. Export the target texture as a **`.dds`** file.
3. Edit the `.dds` texture in your image editor.
   * *Tip:* Keep the original dimensions and DXT compression format (DXT1, DXT3, DXT5, or ARGB) unchanged so the file size matches when reinjecting.
4. Import the modified `.dds` back into the `.xpr` container using GreedXplorer and save it.

### 4. Reinject `.xpr` & Repack `.afs`
1. Patch the modified `.xpr` back into its parent KMD/container file:
   ```bash
   python xpr_tool.py inject
   ```
2. Repack the modified files into a copy of your original `.afs` archive:
   ```bash
   python repack.py databin.afs
   ```

## Disclaimer
This repository contains **only original Python tooling**. No copyrighted game files, `.afs` archives, `.xpr` containers, or textures from *Ninja Gaiden Black* are included or distributed here.
