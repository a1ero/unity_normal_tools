# Unity Normal Map DXT5nm Converter

A small script for recovering a standard RGB normal map from textures that Unity repacks into **DXT5nm** format when imported with the "Normal map" texture type.

## The problem

When a texture in Unity is marked as **Normal map**, the engine repacks it into DXT5 with shuffled channels:

| Channel | What it actually stores |
|---------|--------------------------|
| R       | unused (constant) |
| G       | Y component of the normal |
| B       | unused (constant) |
| A       | X component of the normal |

Because of this, when viewed outside Unity such a texture looks red and "transparent" — the red/blue channels are filled with a constant, while the real data lives in the green and alpha channels.

## What the script does

Unpacks DXT5nm back into a proper RGB normal map:

1. `X = A * 2 - 1`
2. `Y = G * 2 - 1`
3. `Z = sqrt(max(0, 1 - X² - Y²))` — reconstructed, since the normal has unit length and Z isn't stored in the file
4. Packs `X, Y, Z` back into `R, G, B` of a standard normal map (blue dominates, as it should)

## Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)
- [numpy](https://pypi.org/project/numpy/)

```bash
pip install pillow numpy
```

## Usage

Single file:

```bash
python3 unity_normal_unswizzle.py input.dds output.png
```

Entire folder (recursive, preserving subfolder structure):

```bash
python3 unity_normal_unswizzle.py input_folder/ output_folder/
```

If normals look "inverted" after conversion (lighting appears to come from the wrong side) — a typical DirectX/OpenGL convention mismatch for the green channel:

```bash
python3 unity_normal_unswizzle.py input.dds output.png --invert-y
```

### Windows: drag & drop

The package includes batch files for those who'd rather not use the console:

- `install_dependencies.bat` — run once to install Pillow and numpy
- `convert_normal.bat` — drag an image (or several) onto it — `FileName_normal.png` appears next to it
- `convert_normal_inverty.bat` — same, but with `--invert-y`

All `.bat` files and `unity_normal_unswizzle.py` must be in the same folder — the `.bat` files look for the script next to themselves.

Requires Python installed from [python.org](https://www.python.org/downloads/) (not the Microsoft Store), with the **"Add python.exe to PATH"** checkbox checked during installation.

## Supported formats

Input: anything Pillow can read — `.dds` (DXT5/BC3, as well as uncompressed RGBA), `.png`, `.tga`, `.tif`, `.bmp`. Output: `.png`, which can be re-saved to any other format if needed.

## Files

```
unity_normal_unswizzle.py     — main script
convert_normal.bat            — drag & drop conversion (Windows)
convert_normal_inverty.bat    — same, with Y inversion
install_dependencies.bat      — installs dependencies (Windows)
```
