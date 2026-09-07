# Unity Normal Map DXT5nm Converter

Небольшой скрипт для восстановления обычной RGB-карты нормалей из текстур, которые Unity перепаковывает в формат **DXT5nm** при импорте с типом "Normal map".

## Проблема

Когда текстура в Unity помечена как **Normal map**, движок перепаковывает её в DXT5 со смещёнными каналами:

| Канал | Что реально хранит |
|-------|---------------------|
| R     | не используется (константа) |
| G     | Y-компонента нормали |
| B     | не используется (константа) |
| A     | X-компонента нормали |

Из-за этого при просмотре такой текстуры вне Unity она выглядит красной и "прозрачной" — красный/синий залиты константой, а реальные данные лежат в зелёном и альфа-каналах.

## Что делает скрипт

Разворачивает DXT5nm обратно в честный RGB normal map:

1. `X = A * 2 - 1`
2. `Y = G * 2 - 1`
3. `Z = sqrt(max(0, 1 - X² - Y²))` — досчитывается, так как нормаль единичной длины и в файле не хранится
4. Упаковывает `X, Y, Z` обратно в `R, G, B` обычной нормали (доминирует синий канал, как и должно быть)

## Требования

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)
- [numpy](https://pypi.org/project/numpy/)

```bash
pip install pillow numpy
```

## Использование

Один файл:

```bash
python3 unity_normal_unswizzle.py input.dds output.png
```

Папка целиком (рекурсивно, с сохранением структуры подпапок):

```bash
python3 unity_normal_unswizzle.py input_folder/ output_folder/
```

Если после конвертации нормали выглядят "вывернутыми" (свет как будто падает не с той стороны) — типичная путаница DirectX/OpenGL конвенции для зелёного канала:

```bash
python3 unity_normal_unswizzle.py input.dds output.png --invert-y
```

### Windows: drag & drop

В комплекте есть bat-файлы для тех, кто не хочет работать через консоль:

- `install_dependencies.bat` — запустить один раз, поставит Pillow и numpy
- `convert_normal.bat` — перетащить на него картинку (или несколько) — рядом появится `ИмяФайла_normal.png`
- `convert_normal_inverty.bat` — то же самое, но с `--invert-y`

Все `.bat`-файлы и `unity_normal_unswizzle.py` должны лежать в одной папке — `.bat` ищет скрипт рядом с собой.

Требуется Python, установленный с [python.org](https://www.python.org/downloads/) (не из Microsoft Store), с отмеченной галочкой **"Add python.exe to PATH"** при установке.

## Поддерживаемые форматы

На входе — всё, что читает Pillow: `.dds` (DXT5/BC3, а также несжатый RGBA), `.png`, `.tga`, `.tif`, `.bmp`. На выходе — `.png`, который при необходимости можно пересохранить в любой другой формат.

## Файлы

```
unity_normal_unswizzle.py     — основной скрипт
convert_normal.bat            — drag & drop конвертация (Windows)
convert_normal_inverty.bat    — то же, с инверсией Y
install_dependencies.bat      — установка зависимостей (Windows)
```
