#!/usr/bin/env python3
"""
unity_normal_unswizzle.py

Converts the Unity DXT5nm normal map (the format in which Unity 
repacks a texture marked as “Normal map”: X in alpha, Y in green, 
R and B filled with a constant -> the texture appears red 
and “transparent”) back into a regular RGB normal map 
(where the blue channel dominates).

Supports input: .dds (DXT5/BC3, as well as uncompressed RGBA),
.png, .tga and anything else that Pillow reads.
Output: .png (you can then re‑save it to .dds/.tga using anything).

Usage:
 python3 unity_normal_unswizzle.py input.dds output.png
 python3 unity_normal_unswizzle.py input_folder/ output_folder/ # batch processing

Options:
     --invert-y invert the green channel (OpenGL <-> DirectX
     convention if normals are “inverted”)
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SUPPORTED_EXT = {".dds", ".png", ".tga", ".tif", ".tiff", ".bmp", ".jpg", ".jpeg"}


def unswizzle_unity_normal(img: Image.Image, invert_y: bool = False) -> Image.Image:
    """Accepts Unity DXT5nm (A=X, G=Y) and returns a standard RGB normal map."""
    img = img.convert("RGBA")
    arr = np.asarray(img).astype(np.float32) / 255.0

    x = arr[..., 3] * 2.0 - 1.0        # X was in the alpha.
    y = arr[..., 1] * 2.0 - 1.0        # Y was in green.

    if invert_y:
        y = -y

    z_sq = 1.0 - x * x - y * y
    z = np.sqrt(np.clip(z_sq, 0.0, 1.0))

    out = np.empty(arr.shape[:2] + (3,), dtype=np.float32)
    out[..., 0] = x * 0.5 + 0.5
    out[..., 1] = y * 0.5 + 0.5
    out[..., 2] = z * 0.5 + 0.5

    out_u8 = np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)
    return Image.fromarray(out_u8, mode="RGB")


def process_file(src: Path, dst: Path, invert_y: bool) -> None:
    img = Image.open(src)
    result = unswizzle_unity_normal(img, invert_y=invert_y)
    dst.parent.mkdir(parents=True, exist_ok=True)
    result.save(dst)
    print(f"OK: {src} -> {dst}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="A file or folder containing the source textures")
    parser.add_argument("output", type=Path, help="File or folder for the result (.png)")
    parser.add_argument("--invert-y", action="store_true", help="Invert the green channel (Y)")
    args = parser.parse_args()

    if args.input.is_dir():
        args.output.mkdir(parents=True, exist_ok=True)
        files = [p for p in sorted(args.input.rglob("*")) if p.suffix.lower() in SUPPORTED_EXT]
        if not files:
            print(f"No suitable files were found in the {args.input} folder ({', '.join(SUPPORTED_EXT)})", file=sys.stderr)
            sys.exit(1)
        for src in files:
            rel = src.relative_to(args.input).with_suffix(".png")
            dst = args.output / rel
            try:
                process_file(src, dst, args.invert_y)
            except Exception as e:
                print(f"ERROR during processing {src}: {e}", file=sys.stderr)
    else:
        process_file(args.input, args.output, args.invert_y)


if __name__ == "__main__":
    main()
