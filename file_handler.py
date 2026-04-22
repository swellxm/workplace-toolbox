import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def generate_preview_list(files: list, rename_type: str, custom_text: str = "", old_text: str = "", new_text: str = "", start_num: int = 1, step: int = 1) -> List[Tuple[str, str]]:
    preview = []
    for i, file in enumerate(files):
        original_name = file.name
        name_without_ext = os.path.splitext(original_name)[0]
        ext = os.path.splitext(original_name)[1]

        if rename_type == "prefix":
            new_name = f"{custom_text}{original_name}"
        elif rename_type == "suffix":
            new_name = f"{name_without_ext}{custom_text}{ext}"
        elif rename_type == "sequence":
            seq_num = start_num + i * step
            new_name = f"{name_without_ext}_{seq_num:03d}{ext}"
        elif rename_type == "replace":
            new_name = original_name.replace(old_text, new_text) if old_text else original_name
        else:
            new_name = original_name

        preview.append((original_name, new_name))
    return preview

def organize_by_type(files: list) -> dict:
    categories = {
        "文档": [".doc", ".docx", ".pdf", ".txt", ".rtf"],
        "表格": [".xls", ".xlsx", ".csv", ".ods"],
        "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "视频": [".mp4", ".avi", ".mov", ".wmv", ".flv"],
        "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "其他": []
    }

    organized = {cat: [] for cat in categories}
    organized["其他"] = []

    for file in files:
        ext = get_file_extension(file.name)
        found = False
        for cat, extensions in categories.items():
            if ext in extensions:
                organized[cat].append(file.name)
                found = True
                break
        if not found:
            organized["其他"].append(file.name)

    return organized

def organize_by_date(files: list) -> dict:
    now = datetime.now()
    return {
        "今天": [],
        "本周": [],
        "本月": [],
        "更早": []
    }

def organize_by_size(files: list) -> dict:
    return {
        "< 1MB": [],
        "1-10MB": [],
        "10-100MB": [],
        "> 100MB": []
    }

def search_replace_in_text(text: str, search: str, replace: str) -> Tuple[str, int]:
    count = text.count(search)
    new_text = text.replace(search, replace)
    return new_text, count

def batch_rename_files(preview: List[Tuple[str, str]], base_path: str) -> List[Tuple[str, str]]:
    results = []
    for original, new_name in preview:
        if original != new_name:
            results.append((original, new_name, "success"))
        else:
            results.append((original, new_name, "skipped"))
    return results
