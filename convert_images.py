import os

FOLDER = "images"
PREFIX = "minecraft_"
KNOWN_PREFIXES = ["mc_", "mc_minecraft_", "minecraft_minecraft_", "minecraft_"]

def strip_known_prefixes(filename):
    for known in KNOWN_PREFIXES:
        if filename.startswith(known):
            return filename[len(known):]
    return filename

def rename_files_clean_prefix():
    for fname in os.listdir(FOLDER):
        path = os.path.join(FOLDER, fname)
        if not os.path.isfile(path):
            continue

        clean_name = strip_known_prefixes(fname)
        new_name = PREFIX + clean_name

        if fname == new_name:
            print(f"✅ Already clean: {fname}")
            continue

        new_path = os.path.join(FOLDER, new_name)
        os.rename(path, new_path)
        print(f"🔁 Renamed: {fname} → {new_name}")

if __name__ == "__main__":
    rename_files_clean_prefix()

