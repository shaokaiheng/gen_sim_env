import os

def generate_enhanced_filelist(output_filename="filelist.f"):
    # 配置后缀
    src_extensions = ('.v', '.sv')
    hdr_extensions = ('.svh')
    
    current_dir = os.getcwd()
    file_paths = []
    inc_dirs = set() # 使用集合避免重复添加同一个目录

    # 1. 递归遍历目录
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            
            # 处理源文件
            if file.endswith(src_extensions):
                file_paths.append(abs_path)
            
            # 处理头文件：记录其所属目录
            elif file.endswith(hdr_extensions):
                inc_dirs.add(root)
                # 如果你也想把 .svh 文件本身列出来，取消下面这行的注释：
                # file_paths.append(abs_path)

    # 2. 写入文件
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("// ############################################\n")
            f.write("// # Generated Filelist\n")
            f.write("// ############################################\n\n")
            
            # 写入 Include 目录
            if inc_dirs:
                f.write("// Include Directories\n")
                for d in sorted(inc_dirs):
                    f.write(f"+incdir+{d}\n")
                f.write("\n")
            
            # 写入源文件路径
            f.write("// Source Files\n")
            for p in file_paths:
                f.write(f"{p}\n")
                
        print(f"Done! Filelist generated at: {os.path.abspath(output_filename)}")
        print(f"Found {len(file_paths)} source files and {len(inc_dirs)} include directories.")
        
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    generate_enhanced_filelist()
