
import json
import pickle
import numpy as np
import os

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

def input_fn(request_body, request_content_type):
    return json.loads(request_body)

def predict_fn(data, model_bundle):
    model, user_ids, item_ids, asin_to_title = model_bundle
    user_id = data["UserID"]

    if user_id not in user_ids:
        return []

    user_index = user_ids[user_id]
    predictions = []
    for asin, item_index in item_ids.items():
        est_rating = model.predict(user_index, item_index).est
        predictions.append((asin, est_rating))

    top10 = sorted(predictions, key=lambda x: x[1], reverse=True)[:10]
    return [
        {
            "ASIN": asin,
            "productName": asin_to_title.get(asin, "Unknown Product"),
            "expectedRating": round(rating, 2)
        }
        for asin, rating in top10
    ]

def output_fn(prediction, content_type):
    return json.dumps(prediction), content_type
