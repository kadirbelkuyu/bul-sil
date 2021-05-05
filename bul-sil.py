from imutils import paths
import numpy as np
import argparse
import cv2
import os

def dhash(image, hashSize=8):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))
	diff = resized[:, 1:] > resized[:, :-1]

	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

parser = argparse.ArgumentParser()
parser.add_argument('-d',"--dataset", required=True,
	help="Please specify the path to the data file")
parser.add_argument("-r", "--remove", type=int, default=-1,
	help="whether or not duplicates should be removed (i.e., dry run)")
args = vars(parser.parse_args())


print("[INFO] computing image hashes...")
imagePaths = list(paths.list_images(args["dataset"]))
hashes = {}

for imagePath in imagePaths:

	image = cv2.imread(imagePath)
	h = dhash(image)
	i = hashes.get(h, [])
	i.append(imagePath)
	hashes[h] = i

for (h, hashedPaths) in hashes.items():
	if len(hashedPaths) > 1:
		if args["remove"] <= 0:
			montage = None

			for i in hashedPaths:
				image = cv2.imread(i)
				image = cv2.resize(image, (150, 150))

				if montage is None:
					montage = image

				else:
					montage = np.hstack([montage, image])

			print("[INFO] hash: {}".format(h))
			cv2.imshow("Montage", montage)
			cv2.waitKey(0)

		else:

			for i in hashedPaths[1:]:
				os.remove(i)
