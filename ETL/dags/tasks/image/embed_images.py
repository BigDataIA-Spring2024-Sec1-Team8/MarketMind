import os
import pandas as pd
import json
from helpers.pinecone_helper_functions import generate_image_embedding, store_images_in_pinecone
import re

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)
def embed_image_info(**context):
    # task_instance = context['task_instance']
    # data = task_instance.xcom_pull(task_ids='clean_product_info')
    data = "women_shoes_cleaned.csv"
    cat = data.split('_cleaned.csv')[0]
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    file_path = os.path.join(resources, data)
    summaries_file = f"{cat}_summaries.csv"
    summary_path = os.path.join(resources, summaries_file)
    summaries = pd.read_csv(summary_path)
    
    print(file_path)
    df = pd.read_csv(file_path)
    rows = len(df)
    i=0
    paused = None
    while i<rows:
        if paused:
            i=paused
        sample = df.iloc[i]
        print(sample['imageurlhighres'])
        imgs = sample['imageurlhighres']
        imgs = imgs.replace("'",'"')
        imgs = json.loads(imgs)
        chunk_embeddings = []
        chunk_ids = []
        meta = []
        summary = summaries[summaries['asin'] == sample['asin']].iloc[0]['summary']
        for idx,img in enumerate(imgs):
            try:
                embeding = generate_image_embedding(img, summary_text=summary)
                chunk_embeddings.append(embeding[0])
                id = remove_non_ascii(f"{sample['asin']}_image_{idx}")
                chunk_ids.append(id)
                meta_cur ={ 'asin': sample['asin']}
                meta.append(meta_cur)
                break
            except:
                break
        if len(chunk_embeddings) > 0:
            store_images_in_pinecone(chunk_embeddings, chunk_ids,meta, namespace=cat)
        i+=1
    return "success"