import os
from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt


def reject_outliers(data, m=2):
    data[abs(data - np.mean(data)) < m * np.std(data)] = 0
    return data

def differentialSquash(image_source):
    """
    Creates a differential image using a given stack.  Squishes large stacks
    into a single image that should highlight areas of  high activity.

    :param image_source: Path to directory of image sequence
    :return: A heatmap of the sequence
    """
    filenames = sorted(os.listdir(image_source))    # Python doesn't read files in order
    images = []
    for file in filenames:
        if not file.endswith('.txt'):
            I = misc.imread(os.path.join(image_source,file),mode='I')
            images.append(I)
    old = images.pop(0)
    differentialArray = np.zeros(old.shape, dtype='uint16')
    images = images[100:]

    for image in images:
        difference = np.subtract(image, old)
        differentialArray = (differentialArray + difference)
        old = image
    differentialArray = np.where(differentialArray<np.average(differentialArray),0,255)
    misc.imshow(differentialArray)

def filter():
    image = misc.imread(r'C:\Users\ksg13004\Desktop\BME-Senior-Design\Data\sample\Converted\img_000000230_Default_000.jpg')
    plt.imshow(image)
# You can test the above function by uncommenting and changing the path for now.
image_source = '../TestImages/Pos0'
#differentialSquash(image_source)
filter()
