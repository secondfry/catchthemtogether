#!/usr/bin/python

import argparse
import numpy as np

from face_recognition import FaceRecognizer
from PIL import Image
from pymongo import MongoClient
from scipy.spatial import distance


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Face recognition')
  parser.add_argument('--root', help='Image root', default='../result/', type=str)
  parser.add_argument('--vod', help='VOD id', required=True, type=int)
  conf = parser.parse_args()

  # CV
  model = FaceRecognizer()

  # DB
  db = MongoClient('localhost', 27017).schoolcv

  stream = db.streams.find_one({'id': conf.vod})
  if not stream:
    stream = {'id': conf.vod, 'persons': []}

  for image_name in tqdm(os.listdir(conf.root)):
    img = Image.open(os.path.join(conf.root, image_name))
    res = model.get_descriptor(img)

    flag = 0
    for p in stream['persons']:
      if distance.euclidean(p, res) < 1:
        p = np.mean([p, res], axis=0)
        flag = 1

    if not flag:
      stream['persons'].append(res)

    try:
      db.streams.replace_one(stream, upsert=True)
    except Exception as e:
      print(e)
      pass
