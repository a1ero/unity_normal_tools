#!/usr/bin/env python3
"""
unity_normal_unswizzle.py

Конвертирует Unity DXT5nm карту нормалей (формат, в который Unity
перепаковывает текстуру, помеченную как "Normal map": X в альфе,
Y в зелёном, R и B забиты константой -> текстура выглядит красной
и "прозрачной") обратно в обычную RGB карту нормалей (где
доминирует синий канал).

Поддерживает вход: .dds (DXT5/BC3, а также несжатый RGBA),
.png, .tga и всё остальное, что читает Pillow.
Выход: .png (можно потом пересохранить в .dds/.tga чем угодно).

Использование:
    python3 unity_normal_unswizzle.py input.dds output.png
    python3 unity_normal_unswizzle.py input_folder/ output_folder/   # пакетно

Опции:
    --invert-y     инвертировать зелёный канал (OpenGL <-> DirectX
                    конвенция, если нормали "вывернуты")
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SUPPORTED_EXT = {".dds", ".png", ".tga", ".tif", ".tiff", ".bmp", ".jpg", ".jpeg"}


def unswizzle_unity_normal(img: Image.Image, invert_y: bool = False) -> Image.Image:
    """Принимает Unity DXT5nm (A=X, G=Y) и возвращает обычную RGB normal map."""
    img = img.convert("RGBA")
    arr = np.asarray(img).astype(np.float32) / 255.0

    x = arr[..., 3] * 2.0 - 1.0        # X был в альфе
    y = arr[..., 1] * 2.0 - 1.0        # Y был в зелёном

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
    parser.add_argument("input", type=Path, help="Файл или папка с исходными текстурами")
    parser.add_argument("output", type=Path, help="Файл или папка для результата (.png)")
    parser.add_argument("--invert-y", action="store_true", help="Инвертировать зелёный канал (Y)")
    args = parser.parse_args()

    if args.input.is_dir():
        args.output.mkdir(parents=True, exist_ok=True)
        files = [p for p in sorted(args.input.rglob("*")) if p.suffix.lower() in SUPPORTED_EXT]
        if not files:
            print(f"В папке {args.input} не найдено подходящих файлов ({', '.join(SUPPORTED_EXT)})", file=sys.stderr)
            sys.exit(1)
        for src in files:
            rel = src.relative_to(args.input).with_suffix(".png")
            dst = args.output / rel
            try:
                process_file(src, dst, args.invert_y)
            except Exception as e:
                print(f"ОШИБКА при обработке {src}: {e}", file=sys.stderr)
    else:
        process_file(args.input, args.output, args.invert_y)


if __name__ == "__main__":
    main()
