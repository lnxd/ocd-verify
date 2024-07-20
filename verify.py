#!/usr/bin/env python3

import os
import hashlib
import sys

def get_all_file_paths(directory: str) -> list:
    file_paths = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files]
    print(f"- Loaded {len(file_paths)} files from {directory}.")
    return file_paths

def calculate_md5(file_path: str, output=True) -> str:
    try:
        with open(file_path, "rb") as file:
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        checksum = hash_md5.hexdigest()
        if output:
            print(f"- MD5 calculated for {file_path}: {checksum}")
        return checksum
    except Exception as e:
        if output:
            print(f"- Error calculating MD5 for {file_path}: {e}")
        return None

def main(directory1: str, directory2: str):
    files1 = set(get_all_file_paths(directory1))
    files2 = set(get_all_file_paths(directory2))

    rel_files1 = {os.path.relpath(path, directory1): path for path in files1}
    rel_files2 = {os.path.relpath(path, directory2): path for path in files2}

    unique_files1 = set(rel_files1) - set(rel_files2)
    unique_files2 = set(rel_files2) - set(rel_files1)
    common_files = set(rel_files1) & set(rel_files2)

    report_comparisons(common_files, rel_files1, rel_files2)
    report_unique_files(unique_files1, rel_files1, "Directory 1")
    report_unique_files(unique_files2, rel_files2, "Directory 2")

def report_comparisons(common_files, files1_dict, files2_dict):
    if common_files:
        print(f"- Found {len(common_files)} common files. Checking MD5 sums...")
        errors, mismatches = [], []
        for file_name in common_files:
            file1_path, file2_path = files1_dict[file_name], files2_dict[file_name]
            md5sum1, md5sum2 = calculate_md5(file1_path), calculate_md5(file2_path)

            if md5sum1 and md5sum2 and md5sum1 != md5sum2:
                print(f"- MD5 mismatch: {file_name}")
                mismatches.append(file_name)
            elif md5sum1 == md5sum2:
                print(f"- MD5 match for {file_name}.")
            else:
                print(f"- Skipping MD5 comparison for {file_name} due to error.")
                errors.append(file_name)
        print_results(errors, mismatches)
    else:
        print("- No common files to compare.")

def report_unique_files(unique_files, files_dict, directory_name):
    if unique_files:
        print(f"- Unique in {directory_name}:")
        for file_name in unique_files:
            file_path = files_dict[file_name]
            md5sum = calculate_md5(file_path, False)
            print(f"  - {file_name}: {md5sum}")
    else:
        print(f"- No unique files in {directory_name}.")

def print_results(errors, mismatches):
    print("\n--- Summary ---")
    for category, items in [("Failed checks", errors), ("Files with MD5 mismatches", mismatches)]:
        if items:
            print(f"- {category}:")
            for item in items:
                print(f"  - {item}")
        else:
            print(f"- No {category.lower()}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 verify.py <directory1> <directory2>")
        sys.exit(1)
    
    dir1, dir2 = sys.argv[1], sys.argv[2]
    if not all(map(os.path.isdir, [dir1, dir2])):
        print("Error: One or both specified paths are not valid directories.")
        sys.exit(1)
    
    main(dir1, dir2)
