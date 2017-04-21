import os

from datasets.models import Approved, Rejected
import numpy as np
import pandas as pd
import requests
import pickle
import boto
from boto.s3.key import Key
from django.conf import settings


def get_data(approved=True, detail=False, clean=True):
    """Get Data
    returns a numpy array of dicts containing spotteds as specified

    approved: approved or rejected spotteds
    detail: wether or not to return the detailed reject reason
    """

    if approved:
        data = Approved.objects.all()
    else:
        data = Rejected.objects.all()

    if approved:
        return pd.DataFrame([[x.message, "aprovado", x.suggestion] for x in data], columns=['message', "reason", "suggestion"])
    else:
        rejected = pd.DataFrame([[x.message, x.reason, x.suggestion] for x in data], columns=['message', "reason", "suggestion"])
        if clean:
            rejected = clean_details(rejected)
        if detail:
            return rejected
        return rejected.replace({'reason': {'^(.*?)$': 'rejeitado'}}, regex=True)


def clean_details(df):
    """Clean Details
    merges and removes unwanted columns
    """
    details_rej = [
        ("Ofensivo", ["Ofensivo ou Ódio", "Bullying individual"]),
        ("Spam", ["Corrente ou spam", "Conteúdo comercial", "Spam / Propaganda"]),
        ("Obsceno", ["Obsceno ou Assédio"]),
        ("Off-topic", [False]),
        ("Depressivo", [False])
    ]
    res = pd.DataFrame()
    for t in details_rej:
        for c in t[1]:
            if t[0]:
                df = df.replace({'reason': {c: t[0]}})
        res = res.append(df[df['reason'] == t[0]], ignore_index=True)
    return res


def rand_reindex(arr):
    """Random reindex
    randomly reindexes an array
    """

    return arr.reindex(np.random.permutation(arr.index))


def merge_data(approved, rejected, ratio=1):
    """Merge data
    merges approved and rejected arrays using a ratio to size the approved ones
    also reindexes them
    """

    approved = rand_reindex(approved)
    approved = approved.iloc[:(round(len(rejected) * ratio))]
    return rand_reindex(approved.append(rejected, ignore_index=True))


def stop_words():
    response = requests.get("https://gist.githubusercontent.com/alopes/5358189/raw/2107d809cca6b83ce3d8e04dbd9463283025284f/stopwords.txt")
    return response.text.split()


def reload_classifier(class_type, detailed):
    """Reload Classifier
    Reloads a classifier looking for it locally and in S3

    if it does not find it, return None
    """
    custom_path = class_type + ('_detailed' if detailed else '')

    CLASSIFIER_PATH = 'classifier_' + custom_path + '.pkl'

    # Try to find it locally
    if os.path.exists(CLASSIFIER_PATH):
        return pickle.load(open(CLASSIFIER_PATH, 'rb'), encoding='utf-8')

    # Try to find it on S3
    conn = boto.connect_s3(settings.S3_KEY, settings.S3_SECRET)
    bucket = conn.get_bucket(settings.S3_BUCKET)
    try:
        k = Key(bucket, CLASSIFIER_PATH)
        k.get_contents_to_filename(CLASSIFIER_PATH)
        return pickle.load(open(CLASSIFIER_PATH, 'rb'), encoding='utf-8')
    except:
        return None


def save_classifier(classifier, class_type, detailed):
    """Save Classifier
    Saves a classifier to memory so that it can be easily accessed later
    """

    custom_path = class_type + ('_detailed' if detailed else '')

    CLASSIFIER_PATH = 'classifier_' + custom_path + '.pkl'

    pickle.dump(classifier, open(CLASSIFIER_PATH, "wb"))

    with open(CLASSIFIER_PATH, 'rb') as f:

        conn = boto.connect_s3(settings.S3_KEY, settings.S3_SECRET)
        bucket = conn.get_bucket(settings.S3_BUCKET)

        k = Key(bucket)
        k.key = CLASSIFIER_PATH
        k.set_contents_from_file(f)
