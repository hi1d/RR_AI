import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Recommand_Repository:
    def __init__(self, repo_id:int, name):
        self.repo = repo_id
        self.path = os.path.join(BASE_DIR, name)
        self.read_csv()

    def read_csv(self):
        repo = pd.read_csv(self.path)
        df = pd.DataFrame(repo)
        self.Data_Preprocessing(df)

    def Data_Preprocessing(self, df):
        rows = df.iloc
        data = {}
        for row in rows:
            topics = list(filter(lambda x:x != '', row['topics'].split(',')))
            repo_id = row['repo_id']
            topics.append(row['keyword'])
            topics.append(row['language'])
            data[repo_id] = ' '.join(topics)
        self.index = list(data.keys())
        self.keywords = list(data.values())
        self.transform_Tfidvec()

    def transform_Tfidvec(self):
        keywords = self.keywords
        vect = TfidfVectorizer(max_features=300)
        tfvect = vect.fit_transform(keywords).toarray()
        tfdiv_df = pd.DataFrame(tfvect, columns = sorted(vect.vocabulary_))
        tfdiv_df.index = self.index
        self.run_cosine_similarity(tfdiv_df)

    def run_cosine_similarity(self, tfdiv_df):
        similarity = cosine_similarity(tfdiv_df, tfdiv_df)
        item_based_similarity = pd.DataFrame(similarity, index=self.index, columns=self.index)
        self.repositories = item_based_similarity[self.repo].sort_values(ascending=False)[:20]
        print(self.repositories)