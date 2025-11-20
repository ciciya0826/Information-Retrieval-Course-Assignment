import pandas as pd
import json

COMMON_GENRES = {
    '剧情', '喜剧', '动作', '爱情', '科幻', '悬疑', '惊悚', '恐怖',
    '犯罪', '冒险', '奇幻', '动画', '纪录片', '短片', '传记', '历史',
    '战争', '西部', '音乐', '歌舞', '家庭', '儿童', '运动', '灾难',
    '武侠', '古装', '黑色电影', '情色'
}


def split_genre(genre_str):
    if pd.isna(genre_str) or not isinstance(genre_str, str) or genre_str.strip() == '':
        return []

    raw_genres = [g.strip() for g in genre_str.split(' / ') if g.strip()]

    final_genres = []
    seen = set()

    for g in raw_genres:
        if g in COMMON_GENRES:
            if g not in seen:
                final_genres.append(g)
                seen.add(g)
            continue

        temp = []
        remaining = g
        for genre in sorted(COMMON_GENRES, key=lambda x: len(x), reverse=True):
            if genre in remaining:
                temp.append(genre)
                remaining = remaining.replace(genre, '', 1).strip()  # 移除已匹配部分
                if remaining == '':
                    break

        if temp:
            for t in temp:
                if t not in seen:
                    final_genres.append(t)
                    seen.add(t)
        else:
            if g not in seen:
                final_genres.append(g)
                seen.add(g)

    genre_order = ['剧情', '喜剧', '动作', '爱情', '科幻', '悬疑', '惊悚', '犯罪', '冒险', '奇幻', '动画']
    final_genres.sort(key=lambda x: genre_order.index(x) if x in genre_order else 99)

    return final_genres

file_path = './豆瓣电影TOP250.xlsx'
df = pd.read_excel(file_path)

df.columns = ['Title', 'Rating', 'Director', 'Actor', 'Year', 'Country', 'Genre']

df['Director'] = df['Director'].str.replace('导演: ', '', regex=False).str.split(' / ').str[0].str.strip()
df['Actor'] = df['Actor'].str.replace('主演: ', '', regex=False).str.split(' / ').str[0].str.strip()

df['Country'] = df['Country'].apply(
    lambda x: [c.strip() for c in x.split(' / ') if c.strip()] if pd.notna(x) and isinstance(x, str) else []
)

df['Genre'] = df['Genre'].apply(split_genre)

df['Rating'] = df['Rating'].astype(str)


def extract_chinese_title(title):
    parts = title.split('/')
    for part in parts:
        if any('\u4e00' <= char <= '\u9fff' for char in part):
            return part.strip()
    return parts[0].strip()


df['Title_zh'] = df['Title'].apply(extract_chinese_title)

documents = []
for index, row in df.iterrows():
    doc = {
        'id': index + 1,
        'title': row['Title_zh'],
        'rating': row['Rating'],
        'director': row['Director'],
        'actor': row['Actor'],
        'year': str(row['Year']),
        'country': row['Country'],
        'genre': row['Genre'],
        'raw_title': row['Title']
    }
    documents.append(doc)

with open('movie_documents.json', 'w', encoding='utf-8') as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)

print('数据预处理完成，保存在movie_documents.json文件中')