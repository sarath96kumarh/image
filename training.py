import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import random
import gc

from sklearn.model_selection import train_test_split
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array, load_img
from keras.models import load_model

from pydub import AudioSegment
import librosa
import pydub
import contextlib
import wave
from os import listdir
import os
import audiosegment
import numpy as np
import matplotlib.pyplot as plt
import itertools
import librosa.display
from sys import byteorder
from array import array
from struct import pack

from scipy import signal
from scipy.io import wavfile
import random
from skimage.measure import block_reduce
import time
from keras import models
from keras import layers
from skimage.transform import resize

import datetime
import scipy as sp
from scipy.io.wavfile import read
from scipy.io.wavfile import write 

import sys
import math

pat=['C:/Users/sarathkumar.h/Desktop/train_datatt',
     'C:/Users/sarathkumar.h/Desktop/test_datatt',
     'C:/Users/sarathkumar.h/Desktop/train_data/',
     'C:/Users/sarathkumar.h/Desktop/test_data/',
     'C:/Users/sarathkumar.h/Desktop/1sec_train',
     'C:/Users/sarathkumar.h/Desktop/1sec_test',
    'C:/Users/sarathkumar.h/Desktop/1sec_training_image/',
    'C:/Users/sarathkumar.h/Desktop/1sec_testing_image/']

paths = [pat[0],pat[1]]
outname =[pat[2],pat[3]]
for l in range(len(paths)):
    fname =  [f for f in listdir(paths[l])] 
    #print(fname)
    #outname = 'filtered.wav'
    cutOffFrequency = 400.0
    
    for h in range(len(fname)):
        def running_mean(x, windowSize):
            cumsum = np.cumsum(np.insert(x, 0, 0)) 
            return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

        def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):
            if sample_width == 1:
                dtype = np.uint8
            elif sample_width == 2:
                dtype = np.int16 
            else:
                raise ValueError("Only supports 8 and 16 bit audio formats.")
            channels = np.fromstring(raw_bytes, dtype=dtype)
            if interleaved:
                channels.shape = (n_frames, n_channels)
                channels = channels.T
            else:
                channels.shape = (n_channels, n_frames)
            return channels
        with contextlib.closing(wave.open(paths[l]+'/'+fname[h],'rb')) as spf:
            sampleRate = spf.getframerate()
            ampWidth = spf.getsampwidth()
            nChannels = spf.getnchannels()
            nFrames = spf.getnframes()
            signal = spf.readframes(nFrames*nChannels)
            spf.close()
            channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)
            freqRatio = (cutOffFrequency/sampleRate)
            N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
            filtered = running_mean(channels[0], N).astype(channels.dtype)
            wav_file = wave.open(outname[l]+fname[h], "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()
            
def hh(s,e,file):
    frrames=[]
    so=audiosegment.from_file(file)
    with contextlib.closing(wave.open(file,'r')) as f:
        firames = f.getnframes()
        irate = f.getframerate()
        iduration = firames / float(irate)
        
    ss=s
    sec_ee=0
    lllpo=[]
    while sec_ee <= iduration:
        ee=ss+e
        lllpo.append([ss,ee])
        frrames.append(so[ss:ee])
        ss=ee
        drf=ee/1000
        sec_ee=drf
    return frrames,lllpo

pathhs=[pat[2]]
inr=0
inm=0
for l in range(len(pathhs)):
    number_of_image=0
    name_ff= [f for f in listdir(pathhs[l])] 
    for o in name_ff:
        frame=audiosegment.from_file(pathhs[0]+'/'+o)
        ss=frame.set_channels(1)
        ss.export(pat[4]+'/'+o,format='wav')
        

            
pathhhs=[pat[3]]
inrr=0
inmm=0
for l in range(len(pathhhs)):
    number_of_image=0
    name_ff= [f for f in listdir(pathhhs[l])] 
    #print('over_all_file_in_path',len(name_ff))
    for o in name_ff:
        frame=audiosegment.from_file(pathhhs[0]+'/'+o)
        ss=frame.set_channels(1)
        ss.export(pat[5]+'/'+o,format='wav')
        

seconds_path=[pat[4],pat[5]]
image_path=[pat[6],pat[7]]
#label=['music','other']
number_of_image=0
for l in range(len(seconds_path)):
    number_of_image=0
    name_ff= [f for f in listdir(seconds_path[l])] 
    #print('over_all_file_in_path',len(name_ff))
    for o in range(len(name_ff)):
        s=str(o)
        u1,su = librosa.load(seconds_path[l]+'/'+name_ff[o])
        s_fullu,phaseu= librosa.magphase(librosa.stft(u1))
        hh=plt.figure(figsize=(2,2))
        librosa.display.specshow(librosa.amplitude_to_db(s_fullu[:], ref=np.max) ,sr=su)
        if 'm' in name_ff[o]:
            plt.tight_layout()
            plt.savefig(image_path[l]+s+'music')
            plt.close()
        elif 'i' in name_ff[o]:
            plt.tight_layout()
            plt.savefig(image_path[l]+s+'ivr')
            plt.close()
        elif 'c' in name_ff[o]:
            plt.tight_layout()
            plt.savefig(image_path[l]+s+'client')
            plt.close()
        elif 'r' in name_ff[o]:
            plt.tight_layout()
            plt.savefig(image_path[l]+s+'rep')
            plt.close()
        elif 'n' in name_ff[o]:
            plt.tight_layout()
            plt.savefig(image_path[l]+s+'noise')
            plt.close()
            
def process_and_labeling(img):
    X=[]
    y=[]
    
    for image in img:
        X.append(cv2.resize(cv2.imread(image, cv2.IMREAD_COLOR), (nrows,ncloumns),interpolation=cv2.INTER_CUBIC))
        
        if 'client' in image:
            print(image)
            y.append(2)
        elif 'rep' in image:
            print(image)
            y.append(1)
        elif 'ivr' in image:
            print(image)
            y.append(0)
        elif 'music' in image:
            print(image)
            y.append(3)
        elif 'noise' in image:
            print(image)
            y.append(4)
        
    return X,y 
    
train_fo=pat[6]
test_fo=pat[7]

train_img= [train_fo + '/' + f for f in listdir(train_fo)] 
test_img=[test_fo + '/' + f for f in listdir(test_fo)]
random.shuffle(train_img)   


nrows=150
ncloumns=150
channels=3


def process_and_labeling(img):
    X=[]
    y=[]
    
    for image in img:
        X.append(cv2.resize(cv2.imread(image, cv2.IMREAD_COLOR), (nrows,ncloumns),interpolation=cv2.INTER_CUBIC))
        
        if 'client' in image:
            
            y.append(2)
        elif 'rep' in image:
            
            y.append(1)
        elif 'ivr' in image:
            
            y.append(0)
        elif 'music' in image:
            
            y.append(3)
        elif 'noise' in image:
            
            y.append(4)
        
    return X,y   
    
train_fo=pat[6]
test_fo=pat[7]

train_img= [train_fo + '/' + f for f in listdir(train_fo)] 
test_img=[test_fo + '/' + f for f in listdir(test_fo)]
random.shuffle(train_img)   


nrows=150
ncloumns=150
channels=3



X,y=process_and_labeling(train_img)
del train_img

X=np.array(X)
y=np.array(y)

y=to_categorical(y)
print((y).shape)

X_train,X_val,y_train,y_val = train_test_split(X,y, test_size=0.10, random_state=2)

del X
del y
gc.collect()
ntrain=len(X_train)
nval=len(X_val)
batch_size=64
print(nval)
num_class=5


model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)))
model.add(layers.MaxPooling2D((2,2)))
#model.add(layers.BatchNormalization(name='block1_norm0'))

model.add(layers.Conv2D(64,(3,3),activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
#model.add(layers.BatchNormalization(name='block1_norm1'))
          
model.add(layers.Conv2D(128,(3,3),activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
#model.add(layers.BatchNormalization(name='block1_norm2'))

model.add(layers.Dropout(0.25)) 
model.add(layers.Conv2D(128,(3,3),activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
#model.add(layers.BatchNormalization(name='block1_norm3'))

model.add(layers.Dropout(0.5)) #if this not work untag this dropout
model.add(layers.Dense(512, activation='relu'))
#model.add(layers.BatchNormalization(name='block1_norm4'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_class, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4), metrics=['accuracy'])
callbacks=[EarlyStopping(monitor='val_loss',mode=min,verbose=1,patience=800),ModelCheckpoint(filepath='C:/Users/sarathkumar.h/Desktop/mmuus/eiep_ho_best_model.h5', monitor='val_loss',mode='min',verbose=1, save_best_only=True)]


train_datagen= ImageDataGenerator(rescale=1./255,rotation_range=20,horizontal_flip=True)
val_datagen=ImageDataGenerator(rescale=1./255)

train_generator =  train_datagen.flow(X_train,y_train,batch_size=batch_size)
val_generator = val_datagen.flow(X_val,y_val,batch_size=batch_size)

history = model.fit_generator(train_generator,steps_per_epoch=ntrain // batch_size,epochs=1200,validation_data=val_generator,validation_steps=nval // batch_size,callbacks=callbacks)

#model.save(r'C:\Users\sarathkumar.h\Desktop\mp33\model.h5')

acc = history.history['acc']
val_acc=history.history['val_acc']
loss = history.history['loss']
val_loss=history.history['val_loss']

epochs = range(1, len(acc) +1)

plt.plot(epochs, acc , 'b',label='Training acc')
plt.plot(epochs,val_acc,'r',label='val acc')
plt.title('training and val acc')
plt.legend()

plt.figure()

plt.plot(epochs, loss , 'b',label='Training loss')
plt.plot(epochs,val_loss,'r',label='val loss')
plt.title('training and val loss')
plt.legend()

plt.show()