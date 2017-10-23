import os
from scipy import misc
from scipy import ndimage
import numpy as np


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
    old_max = np.max(old)
    differentialArray = np.zeros(old.shape, dtype='uint16')
    images = images[100:]

    for image in images:
        difference = np.subtract(image,old)

        differentialArray = differentialArray + difference
        old = image
    print(differentialArray)
    diffMax = np.max(differentialArray)
    factor = 20         # The factor should be dynamically chosen

    differentialArray[differentialArray<diffMax/factor] = 0
    differentialArray[differentialArray>diffMax/factor] = 1000

    misc.imshow(differentialArray)


# You can test the above function by uncommenting and changing the path for now.
# image_source = '../TestImages/Pos0'
# differentialSquash(image_source)
