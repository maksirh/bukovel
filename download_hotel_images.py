#!/usr/bin/env python3
"""
Download hotel images from Pixover gallery and convert to PNG.
Gallery: Готель Затишний двір
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image
from io import BytesIO

GALLERY_ID = "69e9d50bbee521ea8547ac8b"
SCENE_ID = "69e9d50bbee521ea8547ac8d"
API_URL = f"https://osachuk.pixover.gallery/api/galleries/{GALLERY_ID}/scenes/{SCENE_ID}/files"

BASE_DIR = Path(__file__).parent / "hotel_images"

CATEGORIES = {
    "exterior": "Зовнішній вигляд, фасад, територія",
    "rooms": "Номери, спальні, ванні кімнати",
    "interior": "Інтер'єр, лобі, спільні приміщення",
    "amenities": "Ресторан, басейн, зона відпочинку",
}

HEADERS = {
    "Accept": "application/json",
    "Referer": "https://osachuk.pixover.gallery/3472-hotelzatyshnyidvir",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}

MAX_WORKERS = 6
RETRY_COUNT = 3


def create_folder_structure():
    BASE_DIR.mkdir(exist_ok=True)
    for cat, desc in CATEGORIES.items():
        cat_dir = BASE_DIR / cat
        cat_dir.mkdir(exist_ok=True)

    all_dir = BASE_DIR / "_all"
    all_dir.mkdir(exist_ok=True)

    readme_path = BASE_DIR / "README.md"
    if not readme_path.exists():
        lines = [
            "# Hotel Images — Готель Затишний двір\n",
            "Фотограф: Михайло Осачук\n\n",
            "## Структура папок\n\n",
            "| Папка | Призначення |\n",
            "|-------|-------------|\n",
        ]
        for cat, desc in CATEGORIES.items():
            lines.append(f"| `{cat}/` | {desc} |\n")
        lines.append("| `_all/` | Всі завантажені фото (для сортування) |\n\n")
        lines.append("## Як розсортувати\n\n")
        lines.append(
            "Всі фото знаходяться у `_all/` у порядку галереї (001.png, 002.png...).\n"
        )
        lines.append("Перегляньте і перемістіть у відповідні тематичні папки.\n\n")
        lines.append(f"**Всього фото:** 100\n")
        lines.append(f"**Якість:** large (оригінал, ~4000×2668 px)\n")
        readme_path.write_text("".join(lines), encoding="utf-8")

    print(f"✓ Структура папок створена: {BASE_DIR}")


def fetch_files_list():
    resp = requests.get(API_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    files = data.get("files", [])
    files.sort(key=lambda x: x.get("orderNum", 0))
    print(f"✓ Отримано список: {len(files)} файлів")
    return files


def download_and_convert(idx, file_info, dest_dir):
    order_num = idx + 1
    name_stem = Path(file_info["name"]).stem
    out_path = dest_dir / f"{order_num:03d}_{name_stem}.png"

    if out_path.exists():
        return order_num, out_path.name, "skip"

    large_url = file_info["urlList"].get("large") or file_info["url"]

    for attempt in range(RETRY_COUNT):
        try:
            r = requests.get(large_url, headers=HEADERS, timeout=60)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            img = img.convert("RGB")
            img.save(out_path, "PNG", optimize=False)
            return order_num, out_path.name, "ok"
        except Exception as e:
            if attempt == RETRY_COUNT - 1:
                return order_num, file_info["name"], f"error: {e}"
            time.sleep(2)


def main():
    print("=" * 55)
    print("  Завантаження фото — Готель Затишний двір")
    print("=" * 55)

    create_folder_structure()
    files = fetch_files_list()

    dest = BASE_DIR / "_all"
    total = len(files)
    done = 0
    errors = []

    print(f"\n↓ Завантажую {total} фото (large → PNG)...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_and_convert, i, f, dest): i
            for i, f in enumerate(files)
        }
        for future in as_completed(futures):
            order_num, name, status = future.result()
            done += 1
            if status == "ok":
                print(f"  [{done:3}/{total}] ✓ {name}")
            elif status == "skip":
                print(f"  [{done:3}/{total}] → {name} (вже існує)")
            else:
                print(f"  [{done:3}/{total}] ✗ {name} — {status}")
                errors.append((order_num, name, status))

    print("\n" + "=" * 55)
    print(f"  Готово: {total - len(errors)}/{total} успішно")
    if errors:
        print(f"  Помилок: {len(errors)}")
        for num, name, err in errors:
            print(f"    #{num:03d} {name}: {err}")
    print(f"  Папка: {BASE_DIR / '_all'}")
    print("=" * 55)


if __name__ == "__main__":
    main()
