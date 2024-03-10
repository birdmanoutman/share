import os

import pylnk3 as lnk  # pylnk3库，但请根据实际导入的库名称调整


def parse_lnk(lnk_path):
    """解析.lnk文件获取目标路径"""
    try:
        with open(lnk_path, 'rb') as f:
            lnk_data = lnk.parse(f)
            # 假设我们正确获取到了目标路径
            target_path = lnk_data.path  # 根据实际属性调整
            # 打印出目标路径，确保其正确性
            print(f"Target path: {target_path}")
            return target_path
    except Exception as e:
        print(f"Error parsing {lnk_path}: {e}")
        return None


def create_symbolic_link(source, link_name):
    """创建符号链接"""
    # 确保源路径是绝对路径
    source_abs = os.path.abspath(source)
    print(f"Creating symbolic link: {link_name} -> {source_abs}")
    try:
        os.symlink(source_abs, link_name)
        print(f"Created symbolic link: {link_name} -> {source_abs}")
    except OSError as e:
        print(f"Error creating symbolic link: {e}")


def convert_lnk_to_symlink_in_directory(directory):
    """转换目录及子目录中的所有.lnk文件为符号链接"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.lnk'):
                lnk_path = os.path.join(root, file)
                target = parse_lnk(lnk_path)  # 解析.lnk文件获取目标
                if target:
                    symlink_path = os.path.splitext(lnk_path)[0]  # 移除.lnk扩展名
                    create_symbolic_link(target, symlink_path)  # 创建符号链接
                    os.remove(lnk_path)  # 可选：删除原.lnk文件
                    print(f"Converted {lnk_path} to symlink.")
                else:
                    print(f"Failed to convert {lnk_path}.")


if __name__ == "__main__":
    directory_path = input("Enter the directory path to convert .lnk files: ").strip()
    convert_lnk_to_symlink_in_directory(directory_path)
