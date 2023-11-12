from PIL import Image
from numpy import asarray
from tqdm import tqdm
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


image1 = Image.open('tes4.jpg')
image1.show()
data1 = asarray(image1)

image2= Image.open('tes5.jpg')
image2.show()
data2 = asarray(image2)

def Height(Pict):
    return(Pict.shape[0])

def Width(Pict):
    return(Pict.shape[1])

def RowSplit3(Pict):
    H=Height(Pict)
    p1=H//3
    p2=2*H//3
    if H%3==1:
        p2+=1
    elif H%3==2:
        p1+=1
        p2+=1
    return p1,p2

def ColSplit3(Pict):
    W=Width(Pict)
    p1=W//3
    p2=2*W//3
    if W%3==1:
        p2+=1
    elif W%3==2:
        p1+=1
        p2+=1
    return p1,p2

def RGBtoHSV(Pict):
    return (np.divide(Pict,255.0))

def Cmax(R,G,B):
    N=R
    C=0
    if R>=G and R>=B:
        N=R
        C=0
    elif G>=R and G>=B:
        N=G
        C=1
    else:
        N=B
        C=2
    return N,C

def Cmin(R,G,B):
    N=R
    C=0
    if R<=G and R<=B:
        N=R
        C=0
    elif G<=R and G<=B:
        N=G
        C=1
    else:
        N=B
        C=2
    return N,C

def delta(R,G,B):
    return (Cmax(R,G,B)[0]-Cmin(R,G,B)[0])

def Hue(R,G,B):
    d=delta(R,G,B)
    maxType=Cmax(R,G,B)[1]
    S=0
    if d>0:
        if maxType==0:
            S=(60*(((G-B)/d)%6)%360)
        elif maxType==1:
            S=(60*(((B-R)/d)+2)%360)
        else:
            S=(60*(((R-G)/d)+4)%360)
    return S

def Saturation(R,G,B):
    d=delta(R,G,B)
    max=Cmax(R,G,B)[0]
    if max>0:
        d/=max
    return d

def Value(R,G,B):
    return (Cmax(R,G,B)[0])

def VectorNorm(HSVvector):
    sum=0
    for i in range(0,14):
        sum=sum+HSVvector[i]*HSVvector[i]
    sum=np.sqrt(sum)
    return sum

def VectorDotMult(HSVvector1,HSVvector2):
    sum=0
    for i in range(0,14):
        sum=sum+HSVvector1[i]*HSVvector2[i]
    return sum
    
def CosineSim(HSVvector1,HSVvector2):
    hasil=0.0
    tempDot=VectorDotMult(HSVvector1,HSVvector2)
    tempNorm1=VectorNorm(HSVvector1)
    tempNorm2=VectorNorm(HSVvector2)
    hasil=tempDot/(tempNorm1*tempNorm2)
    return hasil

def Average(Array, N):
    sum=0.0
    for i in range (0,N):
        sum+=Array[i]
    return sum/float(N)

def Quantification(HSVvector,Pixel):
    h=Hue(Pixel[0],Pixel[1],Pixel[2])
    if (h>=316 and h<=360)or h==0:
        HSVvector[0]+=1
    if h>=1 and h<=25:
        HSVvector[1]+=1
    if h>=26 and h<=40:
        HSVvector[2]+=1
    if h>=41 and h<=120:
        HSVvector[3]+=1
    if h>=121 and h<=190:
        HSVvector[4]+=1
    if h>=191 and h<=270:
        HSVvector[5]+=1
    if h>=271 and h<=295:
        HSVvector[6]+=1
    if h>=296 and h<=315:
        HSVvector[7]+=1
    s=Saturation(Pixel[0],Pixel[1],Pixel[2])
    if s>=0 and s<=0.2:
        HSVvector[8]+=1
    if s>0.2 and s<=0.7:
        HSVvector[9]+=1
    if s>0.7 and s<=1:
        HSVvector[10]+=1
    v=Value(Pixel[0],Pixel[1],Pixel[2])
    if v>=0 and v<=0.2:
        HSVvector[11]+=1
    if v>0.2 and v<=0.7:
        HSVvector[12]+=1
    if v>0.7 and v<=1:
        HSVvector[13]+=1


def Compare(data1,data2):
    HSVmatrix1=[[0 for i in range(14)] for i in range (9)]

    rowCoord1=[0,RowSplit3(data1)[0],RowSplit3(data1)[1],Height(data1)]
    colCoord1=[0,ColSplit3(data1)[0],ColSplit3(data1)[1],Width(data1)]

    data1HSV=RGBtoHSV(data1)
    nth1=0
    for i in range (0,3):
        for j in range (0,3):
            print("image 1 is",formatPersen(nth1/9),"done")
            for k in range (rowCoord1[i],rowCoord1[i+1]):
                for l in range (colCoord1[j],colCoord1[j+1]):
                    Quantification(HSVmatrix1[nth1],data1HSV[k][l])
            nth1+=1
    print("image 1 is done")
    print("")

    HSVmatrix2=[[0 for i in range(14)] for i in range (9)]

    rowCoord2=[0,RowSplit3(data2)[0],RowSplit3(data2)[1],Height(data2)]
    colCoord2=[0,ColSplit3(data2)[0],ColSplit3(data2)[1],Width(data2)]

    data2HSV=RGBtoHSV(data2)
    nth2=0
    for i in range (0,3):
        for j in range (0,3):
            print("image 2 is",formatPersen(nth2/9),"done")
            for k in range (rowCoord2[i],rowCoord2[i+1]):
                for l in range (colCoord2[j],colCoord2[j+1]):
                    Quantification(HSVmatrix2[nth2],data2HSV[k][l])
            nth2+=1
    print("image 2 is done")        
    print("")
            
    CosineSimArr=[0 for i in range (9)]
    for i in range (0,9):
        CosineSimArr[i]=CosineSim(HSVmatrix1[i],HSVmatrix2[i])

    hasil=Average(CosineSimArr,9)
    return hasil

def formatPersen(N):
    N*=100
    fN="{:.2f}".format(N)
    sfN=str(fN)+"%"
    return sfN

def printHasil(data1,data2):
    Hasil=Compare(data1,data2)
    print("CosineSimilarity:", formatPersen(Hasil))

printHasil(data1,data2)