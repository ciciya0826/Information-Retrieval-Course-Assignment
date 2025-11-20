import os
import jieba
from sparse_retrieval_system import SparseRetrievalSystem


def main():
    retrieval_system = SparseRetrievalSystem()

    novel_files = [
        './books/青铜葵花.txt',
        './books/草房子.txt',
        './books/根鸟.txt',
        './books/细米.txt',
        './books/红瓦黑瓦.txt'
    ]

    print("正在构建索引...")
    for file_path in novel_files:
        file_name = os.path.basename(file_path).replace(".txt", "")
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
                retrieval_system.add_document(file_name, content)
                print(f"已添加文档: {file_name}")
        except Exception as e:
            print(f"读取文件 {file_name} 时出错: {e}")

    # 打印系统统计信息
    stats = retrieval_system.get_statistics()
    print("\n--- 检索系统统计信息 ---")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 示例测试查询
    test_queries = [
        "青铜葵花",
        "桑桑",
        "根鸟",
        "学校",
        "孩子们"
    ]

    print("\n--- 示例测试查询结果 ---")
    for query in test_queries:
        print(f"\n查询: '{query}'")

        tf_idf_results = retrieval_system.search(query, algorithm='tf_idf', top_k=3)
        print("TF-IDF结果:")
        for doc_id, score in tf_idf_results:
            print(f"  {doc_id}: {score:.4f}")

        bm25_results = retrieval_system.search(query, algorithm='bm25', top_k=3)
        print("BM25结果:")
        for doc_id, score in bm25_results:
            print(f"  {doc_id}: {score:.4f}")


if __name__ == "__main__":
    main()