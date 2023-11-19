from PIL import Image
from numpy import asarray
from time import process_time 
import numpy as np
import os

t1_start = process_time()  

def RGBNorm(Pict):
    Pict=Pict.astype(np.float32)
    return (np.divide(Pict,255.0))

def subMatrix(matrix,n):
    i=matrix.shape[0] % n
    j=matrix.shape[1] % n
    return np.reshape(matrix,(n,round((matrix.shape[0]+i)/n),n,round((matrix.shape[1]+j)/n),3),order='C')

def HSV(Pict):
    
    red_channel = Pict[:, :, 0]
    green_channel = Pict[:, :, 1]
    blue_channel = Pict[:, :, 2]
    
    cmax=np.max(Pict, axis=2)
    cmin=np.min(Pict, axis=2)
    delta=np.subtract(cmax,cmin)

    boolmaxR = np.logical_and(delta!=0,cmax==red_channel)
    boolmaxG = np.logical_and(delta!=0,cmax==green_channel)
    boolmaxB = np.logical_and(delta!=0,cmax==blue_channel)
    boolG = np.logical_and(delta==0,delta==0)
    
    htemp=np.zeros_like(red_channel,dtype=np.float32)
    stemp=np.zeros_like(red_channel,dtype=np.float32)
    vtemp=np.zeros_like(red_channel,dtype=np.float32)
    
    red_channel=RGBNorm(red_channel)
    green_channel=RGBNorm(green_channel)
    blue_channel=RGBNorm(green_channel)

    cmax=RGBNorm(cmax)
    delta=RGBNorm(delta)

    htemp[boolG]=0
    htemp[boolmaxR]=(60*(((green_channel[boolmaxR]-blue_channel[boolmaxR])/delta[boolmaxR])%6))
    htemp[boolmaxG]=(60*(((blue_channel[boolmaxG]-red_channel[boolmaxG])/delta[boolmaxG])+2))
    htemp[boolmaxB]=(60*(((red_channel[boolmaxB]-green_channel[boolmaxB])/delta[boolmaxB])+4))
    
    stemp[cmax==0]=0
    stemp[cmax!=0]=delta[cmax!=0]/cmax[cmax!=0]

    vtemp=cmax
    
    vector=Quantify(htemp,stemp,vtemp)
    return vector

def Quantify(hue,sat,val):
    h=np.copy(hue)
    s=np.copy(sat)
    v=np.copy(val)

    h[np.logical_and(h>315, h==0)]=0
    h[np.logical_and(h>0, h<=25)]=1
    h[np.logical_and(h>25, h<=40)]=2
    h[np.logical_and(h>40, h<=120)]=3
    h[np.logical_and(h>120, h<=190)]=4
    h[np.logical_and(h>190, h<=270)]=5
    h[np.logical_and(h>270, h<=295)]=6
    h[np.logical_and(h>295, h<=315)]=7
    
    hueRange = [0,1,2,3,4,5,6,7]
    huedict = {value: np.count_nonzero(h==value) for value in hueRange}
    H = np.array(list(huedict.values()),dtype=np.uint32)

    s[np.logical_and(s>0.7, s<=1)]=2
    s[np.logical_and(s>0.2, s<=0.7)]=1
    s[np.logical_and(s>=0, s<=0.2)]=0
    
    satRange = [0,1,2]
    satdict = {value: np.count_nonzero(s==value) for value in satRange}
    S = np.array(list(satdict.values()),dtype=np.uint32)

    v[np.logical_and(v>0.7, v<=1)]=2
    v[np.logical_and(v>0.2, v<=0.7)]=1
    v[np.logical_and(v>=0, v<=0.2)]=0
    
    valRange = [0,1,2]
    valdict = {value: np.count_nonzero(v==value) for value in valRange}
    V = np.array(list(valdict.values()),dtype=np.uint32)

    return np.concatenate((H,S,V))  

def cosineSimAvg(v1,v2):
    hasil=0.0
    for i in range(16):
        vDot=np.dot(v1[i],v2[i])
        vNorm1=np.linalg.norm(v1[i])
        vNorm2=np.linalg.norm(v2[i])
        hasil+=np.divide(vDot,np.multiply(vNorm1,vNorm2))
    return round(hasil/16,4)

def Result(Pict,n):
    Pict=Image.open(Pict).convert("RGB")
    Pict=asarray(Pict)
    result_array = np.zeros((n*n,14), dtype=np.int64)
    h=Pict.shape[0]//n
    w=Pict.shape[1]//n
    nth=0
    for i in range (0,n):
        for j in range (0,n):
            result_array[nth]=HSV(Pict[i*h:h*(i+1)-1, j*w:w*(j+1)-1 ,:])
            nth+=1
    return result_array
    
def get_result_image():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    folder_name = 'archive\dataset'
    folder_path = os.path.join(current_folder, folder_name)
    dataset_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    input_path = os.path.join(current_folder, '18.jpg')
    v1=Result(input_path,4)

    similarities = [(similarity_value, os.path.basename(path)) for path, similarity_value in zip(dataset_paths, [cosineSimAvg(v1, Result(path,4)) * 100 for path in dataset_paths]) if similarity_value > 60]
    similarities.sort(reverse=True, key=lambda x: x[0])
    print(len(similarities))
    print(similarities)

get_result_image()

t1_stop = process_time()

print("Elapsed time:", t1_stop-t1_start)
