import json
from collections import defaultdict

DOCUMENTS_FILE = 'movie_documents.json'

GENRES_AVAILABLE = [
    '剧情', '犯罪', '爱情', '灾难', '奇幻', '动画', '动作', '喜剧', '战争',
    '科幻', '冒险', '音乐', '历史', '传记', '家庭', '惊悚', '悬疑', '歌舞',
    '古装', '西部', '运动', '儿童', '情色'
]

# 查询字段编号
QUERY_FIELDS = {
    "1": ("title", "电影名称"),
    "2": ("rating", "评分"),
    "3": ("director", "导演"),
    "4": ("actor", "演员"),
    "5": ("year", "年份"),
    "6": ("country", "国家"),
    "7": ("genre", "类型"),
}


class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set)
        self.documents = {}
        self.indexed_fields = ['title', 'rating', 'director', 'actor', 'year', 'country', 'genre']

    def load_documents(self):
        try:
            with open(DOCUMENTS_FILE, 'r', encoding='utf-8') as f:
                docs = json.load(f)
            for doc in docs:
                self.documents[doc['id']] = doc
            print(f"成功加载 {len(self.documents)} 个电影文档。")
        except FileNotFoundError:
            print(f"错误：未找到文件 {DOCUMENTS_FILE}！")
            exit()

    def build_index(self):
        print("开始构建倒排索引...")

        for doc_id, doc in self.documents.items():
            for field in self.indexed_fields:
                term_source = doc.get(field)

                terms = []
                if isinstance(term_source, str):
                    terms.append(term_source.lower())
                elif isinstance(term_source, list):
                    terms.extend([t.lower() for t in term_source])

                for term in terms:
                    processed_term = term.strip().lower()
                    if processed_term:
                        self.index[processed_term].add(doc_id)

        for term in self.index:
            self.index[term] = sorted(list(self.index[term]))

        print("倒排索引构建完成。")

    def query_field(self, field, keyword):
        keyword = keyword.lower().strip()
        doc_ids = []

        for doc_id, movie in self.documents.items():
            value = movie.get(field)

            if isinstance(value, str):
                if value.lower() == keyword:
                    doc_ids.append(doc_id)
            elif isinstance(value, list):
                if keyword in [v.lower() for v in value]:
                    doc_ids.append(doc_id)
            else:
                if str(value) == keyword:
                    doc_ids.append(doc_id)

        return self.format_results(doc_ids)

    def query_by_genre(self, genre_name):
        genre_key = genre_name.strip().lower()
        doc_ids = self.index.get(genre_key, [])
        return self.format_results(doc_ids)

    def format_results(self, doc_ids):
        results = []
        for doc_id in doc_ids:
            movie = self.documents.get(doc_id)
            if movie:
                results.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'rating': movie['rating'],
                    'director': movie['director'],
                    'year': movie['year'],
                    'genre': ', '.join(movie['genre'])
                })
        return results

    def run_cli(self):

        while True:
            print("\n请选择查询字段（输入 exit 退出）：")
            for k, v in QUERY_FIELDS.items():
                print(f"{k}. {v[1]}")

            choice = input("请输入序号： ").strip()

            if choice.lower() == "exit":
                print("已退出系统。")
                break

            if choice not in QUERY_FIELDS:
                print("无效输入，请重试。")
                continue

            field_key, field_name = QUERY_FIELDS[choice]

            if choice == "7":
                print("\n可选类型：")
                print(" ".join(GENRES_AVAILABLE))

                genre = input("请输入要查询的类型： ").strip()
                if genre not in GENRES_AVAILABLE:
                    print("类型不存在，请重新输入。")
                    continue

                results = self.query_by_genre(genre)
                print(f"\n--- 类型查询结果：{genre} ---")

            else:
                keyword = input(f"请输入要查询的 {field_name}： ").strip()
                if not keyword:
                    print("输入不能为空！")
                    continue

                results = self.query_field(field_key, keyword)
                print(f"\n--- {field_name} 查询结果：{keyword} ---")

            if results:
                for movie in results:
                    print(
                        f"[{movie['id']}] {movie['title']} | 评分 {movie['rating']} | "
                        f"{movie['director']} | {movie['year']} | {movie['genre']}"
                    )
            else:
                print("未找到匹配的电影。")


if __name__ == '__main__':
    index_builder = InvertedIndex()
    index_builder.load_documents()
    index_builder.build_index()
    index_builder.run_cli()
