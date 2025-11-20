import os
import jieba
from collections import Counter

novel_files = [
    './books/青铜葵花.txt',
    './books/草房子.txt',
    './books/根鸟.txt',
    './books/细米.txt',
    './books/红瓦黑瓦.txt'
]

novel_data_segmented = {}
all_words = []

for file_path in novel_files:
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='gbk') as f:
            content = f.read()

            # Jieba word segmentation
            words = list(jieba.cut(content))
            novel_data_segmented[file_name] = {
                'segmented_words': words,
                'word_count': len(words)
            }
            all_words.extend(words)

    except Exception as e:
        print(f"Error reading {file_name}: {e}")

# Word segmentation statistics
print("\n--- 分词统计分析 ---")
for file_name, data in novel_data_segmented.items():
    print(f"文件: {file_name}")
    print(f"  分词数量: {data['word_count']} 个")

# Filter out single characters and spaces, and convert to lowercase for better statistics
filtered_words = [word.lower() for word in all_words if len(word.strip()) > 1]
word_freq = Counter(filtered_words)

print(f"总词汇量 (去重后): {len(word_freq)}")
print(f"总词数 (分词后): {len(filtered_words)}")
print("词频最高的20个词:")
for word, freq in word_freq.most_common(20):
    print(f"  {word}: {freq}")

# Calculate average word length
if filtered_words:
    avg_word_length = sum(len(word) for word in filtered_words) / len(filtered_words)
    print(f"平均词长: {avg_word_length:.2f}")
else:
    print("没有有效词语进行平均词长计算。")