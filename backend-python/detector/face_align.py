#!/usr/bin/python

import argparse
import numpy as np
import os
import sys
import traceback

from align_trans import get_reference_facial_points, warp_and_crop_face
from detector import detect_faces
from PIL import Image
from tqdm import tqdm


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = "face alignment")
  parser.add_argument("-source_root", "--source_root", help = "specify your source dir", default = "../data/", type = str)
  parser.add_argument("-dest_root", "--dest_root", help = "specify your destination dir", default = "../result/", type = str)
  parser.add_argument("-crop_size", "--crop_size", help = "specify size of aligned faces, align and crop with padding", default = 112, type = int)
  args = parser.parse_args()

  source_root = args.source_root # specify your source dir
  dest_root = args.dest_root # specify your destination dir
  crop_size = args.crop_size # specify size of aligned faces, align and crop with padding
  scale = crop_size / 112.
  reference = get_reference_facial_points(default_square = True) * scale

  cwd = os.getcwd() # delete '.DS_Store' existed in the source_root
  os.chdir(source_root)
  os.system("find . -name '*.DS_Store' -type f -delete")
  os.chdir(cwd)

  if not os.path.isdir(dest_root):
    os.mkdir(dest_root)

  for image_name in tqdm(os.listdir(source_root)):
    print("Processing\t{}".format(os.path.join(source_root, image_name)))
    img = Image.open(os.path.join(source_root, image_name))

    try: # Handle exception
      _, landmarks = detect_faces(img)
    except Exception as e:
      print("{} is discarded due to exception!".format(os.path.join(source_root, image_name)))
      traceback.print_exc(file=sys.stdout)
      print(e)
      continue
    if len(landmarks) == 0: # If the landmarks cannot be detected, the img will be discarded
      print("{} is discarded due to non-detected landmarks!".format(os.path.join(source_root, subfolder, image_name)))
      continue

    i = 0
    for lm in landmarks:
      facial5points = [[lm[j], lm[j + 5]] for j in range(5)]
      warped_face = warp_and_crop_face(np.array(img), facial5points, reference, crop_size=(crop_size, crop_size))
      img_warped = Image.fromarray(warped_face)

      new_image_name = '{}_{}.jpg'.format(image_name, i)
      i += 1

      img_warped.save(os.path.join(dest_root, new_image_name))

    os.unlink(os.path.join(source_root, subfolder, image_name))
