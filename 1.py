import os
import shutil

DIR_PUB = "./publications"
DIR_ALUM = "./students-alumni"
BACKUP_PREFIX = ".backup_"

def get_subdirs(path):
    dirs = []
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            dirs.append(name)
    return dirs


def main():
    pub_dirs = get_subdirs(DIR_PUB)
    alum_raw = get_subdirs(DIR_ALUM)

    # map:真实名字 -> .backup_xxx文件夹名
    alum_map = {}
    for d in alum_raw:
        if d.startswith(BACKUP_PREFIX):
            real_name = d[len(BACKUP_PREFIX):]
            alum_map[real_name] = d

    match_items = []
    for pub_name in pub_dirs:
        if pub_name in alum_map:
            match_items.append(pub_name)

    print(f"共匹配到 {len(match_items)} 个目录，将替换目录内部文件，外层文件夹保留原名\n")

    for name in sorted(match_items):
        src_dir = os.path.join(DIR_ALUM, alum_map[name])
        dst_dir = os.path.join(DIR_PUB, name)

        print(f"👉处理 {name}")
        print(f" 源目录 {src_dir}")
        print(f" 目标目录 {dst_dir}")

        # 遍历备份目录内全部文件，覆盖拷贝到publications对应子目录
        for entry in os.listdir(src_dir):
            src_entry = os.path.join(src_dir, entry)
            dst_entry = os.path.join(dst_dir, entry)

            if os.path.isfile(src_entry):
                # 覆盖文件（index.html等）
                shutil.copy2(src_entry, dst_entry)
                print(f"    覆盖文件: {entry}")
            elif os.path.isdir(src_entry):
                # 如果里面还有子文件夹，递归拷贝
                if os.path.exists(dst_entry):
                    shutil.rmtree(dst_entry)
                shutil.copytree(src_entry, dst_entry)
                print(f"    拷贝子目录: {entry}")
        print()

    print("✅完成！仅替换内部文件，publications外层文件夹名称全部保留原样；独有目录未改动。")

if __name__ == "__main__":
    main()