import os
import re
import sys

def clean_file(filepath):
    """清理单个文件中的多余换行符和空白行，保留代码逻辑结构"""
    try:
        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 记录原始行数
        original_lines = content.splitlines()
        original_line_count = len(original_lines)
        
        # 保留注释、字符串字面值等特殊内容的占位符
        preserved_parts = {}
        placeholder_counter = 0
        
        # 保存多行注释（/* */ 形式）
        comment_start = 0
        while comment_start < len(content):
            start_pos = content.find('/*', comment_start)
            if start_pos == -1:
                break
            end_pos = content.find('*/', start_pos + 2)
            if end_pos == -1:
                break
            end_pos += 2
            comment_text = content[start_pos:end_pos]
            placeholder = f"__MULTILINE_COMMENT_{placeholder_counter}__"
            preserved_parts[placeholder] = comment_text
            content = content[:start_pos] + placeholder + content[end_pos:]
            comment_start = start_pos + len(placeholder)
            placeholder_counter += 1
        
        # 保存单行注释（// 形式）
        lines = content.split('\n')
        for i, line in enumerate(lines):
            pos = line.find('//')
            if pos != -1:
                comment_text = line[pos:]
                placeholder = f"__SINGLELINE_COMMENT_{placeholder_counter}__"
                preserved_parts[placeholder] = comment_text
                lines[i] = line[:pos] + placeholder
                placeholder_counter += 1
        content = '\n'.join(lines)
        
        # 保存字符串字面值（双引号内容）
        string_matches = list(re.finditer(r'"([^"\\]|\\.)*"', content))
        for match in reversed(string_matches):  # 从后往前替换，避免位置偏移
            string_text = match.group(0)
            placeholder = f"__STRING_LITERAL_{placeholder_counter}__"
            preserved_parts[placeholder] = string_text
            start, end = match.span()
            content = content[:start] + placeholder + content[end:]
            placeholder_counter += 1
        
        # 将所有只包含空白字符的行替换为单个换行符
        # 使用正则表达式匹配只包含空白字符的行（包括空行）
        content = re.sub(r'^\s*$', '', content, flags=re.MULTILINE)
        
        # 移除由上一步产生的连续空行（即多个连续的换行符）
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 清理可能产生的开头和结尾的多余换行符
        content = content.strip('\n')
        
        # 恢复保存的内容
        for placeholder, original_text in preserved_parts.items():
            content = content.replace(placeholder, original_text)
        
        # 记录处理后的行数
        new_lines = content.splitlines()
        new_line_count = len(new_lines)
        
        # 将清理后的内容写回文件
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"已处理文件: {filepath} (行数: {original_line_count} -> {new_line_count})")
        return True
    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {str(e)}")
        return False

def process_directory(directory_path):
    """遍历目录并处理所有.v和.sv文件"""
    if not os.path.isdir(directory_path):
        print(f"错误: 路径 '{directory_path}' 不是一个有效的目录")
        return
    
    # 查找所有 .v 和 .sv 文件
    files_to_process = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.v', '.sv')):
                filepath = os.path.join(root, file)
                files_to_process.append(filepath)
    
    if not files_to_process:
        print(f"在目录 '{directory_path}' 中未找到 .v 或 .sv 文件")
        return
    
    print(f"找到 {len(files_to_process)} 个文件需要处理:")
    for file in files_to_process:
        print(f"  - {file}")
    
    # 逐个处理文件
    processed_count = 0
    for filepath in files_to_process:
        if clean_file(filepath):
            processed_count += 1
    
    print(f"\n处理完成! 成功处理了 {processed_count}/{len(files_to_process)} 个文件")

def main():
    if len(sys.argv) != 2:
        print("用法: python remove_extra_newlines.py <目录路径>")
        print("此脚本用于清理Verilog/SystemVerilog文件中的多余换行符和空白行")
        sys.exit(1)
    
    directory_path = sys.argv[1].strip()
    
    # 处理路径中的引号
    directory_path = directory_path.strip('"\'')
    
    process_directory(directory_path)

if __name__ == "__main__":
    main()

