import os

novel_files = [
    './books/青铜葵花.txt',
    './books/草房子.txt',
    './books/根鸟.txt',
    './books/细米.txt',
    './books/红瓦黑瓦.txt'
]

novel_data = {}

for file_path in novel_files:
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='gbk') as f:
            content = f.read()
            novel_data[file_name] = {
                'content': content,
                'size_bytes': os.path.getsize(file_path),
                'char_count': len(content)
            }
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

# 打印基础统计信息
print("\n--- 原始数据统计分析 ---")
for file_name, data in novel_data.items():
    print(f"文件: {file_name}")
    print(f"  大小: {data['size_bytes']} 字节")
    print(f"  字符数: {data['char_count']} 个")