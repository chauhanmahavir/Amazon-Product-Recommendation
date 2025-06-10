
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import os
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_split

def model_fn(model_dir):
    with open(os.path.join(model_dir, "als_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, "user_ids.pkl"), "rb") as f:
        user_ids = pickle.load(f)
    with open(os.path.join(model_dir, "item_ids.pkl"), "rb") as f:
        item_ids = pickle.load(f)
    with open(os.path.join(model_dir, "asin_to_title.pkl"), "rb") as f:
        asin_to_title = pickle.load(f)
    return model, user_ids, item_ids, asin_to_title

def train():
    df = pd.read_csv("/opt/ml/input/data/training/merged_data.csv")
    print("Read File")

    df = df[['User ID', 'ASIN', 'Rating', 'Product Title']].dropna()
    df = df[df['Rating'].between(1, 5)]

    user_ids = {uid: i for i, uid in enumerate(df['User ID'].unique())}
    item_ids = {iid: i for i, iid in enumerate(df['ASIN'].unique())}
    

    df['user_index'] = df['User ID'].map(user_ids)
    df['item_index'] = df['ASIN'].map(item_ids)
    
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_index', 'item_index', 'Rating']], reader)
    trainset = data.build_full_trainset()
    asin_to_title = df.drop_duplicates('ASIN').set_index('ASIN')['Product Title'].to_dict()
    
    print("Training Start")
    
    model = SVD()
    model.fit(trainset)
    
    print("Training Complete")
    

    os.makedirs("/opt/ml/model", exist_ok=True)
    with open("/opt/ml/model/als_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model Saved")
    with open("/opt/ml/model/user_ids.pkl", "wb") as f:
        pickle.dump(user_ids, f)
    print("User Saved")
    with open("/opt/ml/model/item_ids.pkl", "wb") as f:
        pickle.dump(item_ids, f)
    print("Item Saved")
    with open("/opt/ml/model/asin_to_title.pkl", "wb") as f:
        pickle.dump(asin_to_title, f)
    print("ASIN Saved")

if __name__ == '__main__':
    train()