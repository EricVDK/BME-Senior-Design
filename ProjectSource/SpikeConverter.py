from neo import Block
from neo.io import Spike2IO
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
import numpy as np
import random
import pandas as pd

def readText():
    f = open(r"C:\Users\ksg13004\Desktop\BME-Senior-Design\Data\asdf.txt")
    load_data = False
    spike = False
    full_data = []
    current_data = []
    template = []
    for line in f:
        if('"channel"\t"5"' in line.lower()):
            load_data = True
        elif('"channel"\t' in line.lower()):
            load_data=False
        if(load_data):
            if(spike):
                if(len(line)>1):
                    current_data.append(float(line))
                else:
                    spike=False
            if("wavmk" in line.lower() or "start" in line.lower()):
                full_data.append(current_data)
                template.append(line.split()[3])
                current_data = []
                spike=True
    spikes=pd.DataFrame({'spike_data':full_data,'template':template})

    spikes = spikes[spikes['template']!='0']
    return spikes

def mixSpikes(data):
    mixed_spike = []
    secondary_spike = []
    template = data['template']
    full_data = data['spike_data']
    print(len(full_data))

    random_offset = random.randint(-10,10)


    n = len(full_data)
    first = random.randint(0,n)
    second = random.randint(0,n)
    while(template[first] == template[second]):
        second = random.randint(0, n)
    for i in range(len(full_data[first])):
        alpha = full_data[first][i]
        try:
            beta = full_data[second][i+random_offset]
        except:
            beta = 0
        secondary_spike.append(beta)
        mixed_spike.append(alpha+beta)

    return mixed_spike, (template[first],template[second]), (full_data[first],secondary_spike)



def help():
    r = Spike2IO(r'C:\Users\ksg13004\Desktop\BME-Senior-Design\Data\new.smr')
    block = r.read_segment()
    alpha = block.spiketrains
    # alpha = preprocessing.scale(alpha)
    old = 0
    rolling_window_length = 500
    difference = []
    # for number in alpha:
    #    difference.append((number - old)**2)
    #    if len(difference)>rolling_window_length:
    #        difference.pop(0)



    plt.plot(alpha[0])
    plt.show()
def getSpike(display = False):
    data = readText()
    mix,extra, parts = mixSpikes(data)
    if display:
        plt.plot(mix)
        print(extra[0], extra[1])
        plt.plot(parts[0])
        plt.plot(parts[1])
        plt.show()


if __name__ =="__main__":
    print("OWO")