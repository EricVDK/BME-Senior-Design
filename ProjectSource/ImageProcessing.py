import os
from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence
import cv2
import shutil
import random

def bandpassFFT(img):
    if type(img) is str:
        img = cv2.imread(img,0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))

    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])


    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2

    mask = np.zeros((rows,cols),np.uint8)
    mask[int(crow-40):int(crow+40), int(ccol-40):int(ccol+40)] = 1

    fshift = fshift*mask

    fshift[int(crow-3):int(crow+3), int(ccol-3):int(ccol+3)] = 0



    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    print(img_back.shape)
    img_back = img_back.astype(np.uint8)
    contrast = cv2.equalizeHist(img_back)



    plt.subplot(131),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
    plt.title('Image after BPF'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(contrast, cmap = 'gray')
    plt.title('after contrast'), plt.xticks([]), plt.yticks([])
    #plt.subplot(133),plt.imshow(img_back, cmap = 'gray', vmin = 30)
    #plt.title('after contrast'), plt.xticks([]), plt.yticks([])

    plt.show()

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
    # filenames = sorted(os.listdir(image_source))    # Python doesn't read files in order
    # images = []
    # for file in filenames:
    #     if not file.endswith('.txt'):
    #         I = misc.imread(os.path.join(image_source,file),mode='I')
    #         images.append(I)
    # old = images.pop(0)

    # images = images[100:]
    im = Image.open(image_source)
    old = []
    count = 0
    for i, page in enumerate(ImageSequence.Iterator(im)):
        count+=1
        if(i==0):
            old = np.array(page)
            differentialArray = np.zeros(old.shape, dtype='int16')
        else:
            differentialArray = np.add(np.array(page), differentialArray)
            #differentialArray = (differentialArray + difference)
            old = np.array(page)
    #differentialArray = np.where(differentialArray<np.average(differentialArray),0,255)
    differentialArray = np.divide(differentialArray,count)
    return differentialArray
    #plt.imshow(differentialArray,cmap="gray")
    #plt.show()

def filter(file):
    im = Image.open(file)

    image_array = []
    count = 0
    average_intensity = []
    found = False
    for i,page in enumerate(ImageSequence.Iterator(im)):
        img = np.array(page)
        if(i<50):
            average_intensity.append(np.sum(img))
        else:
            try:
                alpha = (np.sum(img)-np.average(average_intensity))/np.average(average_intensity)
                if alpha>0.08 and not found:
                    plt.imsave("D:/YSet/" + str(i) + ".tif",img,cmap="gray")
                    found = True
                    print("saved")
                    break
            except Exception as e:
                print(e)
        if(i ==500) and not found:
            plt.imsave("D:/YSet/" + str(random.randint(0,5000)) + ".tif", img, cmap="gray")
            print("saved")


# You can test the above function by uncommenting and changing the path for now.
#image_source = '../TestImages/Pos0'
#differentialSquash(r'D:\ZSet\24.tif')


def moveGoodFiles(file,filename):
    stack = False
    try:
        with Image.open(file) as im:
            image_array = []

            for i, page in enumerate(ImageSequence.Iterator(im)):
                if i > 100:
                    stack = True
                    break
    except Exception as e:
        print("Error")
        print(e)
    if(stack):
        shutil.move(file,"D:/ZSet/"+filename)
        print("Send File:" + filename)


def squash(file,filename):
    with Image.open(file) as im:
        y,x = im.size
        max_arr = np.empty((x,y))
        min_arr = np.empty((x,y))
        average_arr = np.empty((x,y))
        count = 0
        for i,page in enumerate(ImageSequence.Iterator(im)):
            page_arr = np.array(page)
            if i == 2:
                min_arr = page_arr
            count+=1
            truth_max = page_arr > max_arr
            max_arr = max_arr*(1-truth_max) + page_arr*truth_max
            truth_min = page_arr < min_arr
            min_arr = min_arr*(1-truth_min) + page_arr*truth_min
            average_arr = np.add(average_arr, page_arr)
        average_arr=np.divide(average_arr,count)
        new_arr = np.divide(average_arr,np.subtract(max_arr,min_arr))
        print(filename.split('.')[0])
        misc.imsave(r'C:\Users\ksg13004\Desktop\BME-Senior-Design\Data\\'+filename.split('.')[0]+'.png', new_arr,'png')

mutable = [0]
def press(event):
    print('press', event.key)
    if event.key == 'n':
        mutable[0]=0
    elif event.key == 'y':
        mutable[0]=1


def showAndMove(file,filename):
    im = Image.open(file)
    for i, page in enumerate(ImageSequence.Iterator(im)):
        page_arr = np.array(page)
        if i == 2:
            fig = plt.figure()
            plt.imshow(page_arr)
            fig.canvas.mpl_connect('key_press_event', press)
            plt.show()
            fig.clear()
            if(mutable[0] == 1):

                #shutil.move(file,'D:/WSet/'+filename)
                print(filename)

            break
    im.close()






def moveFiles():
    root ='D:/ZSet'
    for path, subdirs, files in os.walk(root):
        for name in files:
                    #shutil.move(os.path.join(path, name),root+'/'+str(i)+".tif")
            showAndMove(os.path.join(path, name),name)
def open_and_close():
    img = misc.imread(r'C:\Users\ksg13004\Desktop\BME-Senior-Design\Results\src\img_000000238_Default_000.png')
    img = img*(img>230)
    plt.subplot(221)
    plt.imshow(img)
    img_bw = (255*(img>0)).astype('uint8')
    se1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    plt.subplot(222,title='Mask1')
    plt.imshow(mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)
    plt.subplot(223,title='mask2')
    plt.imshow(mask)
    plt.show()
moveFiles()