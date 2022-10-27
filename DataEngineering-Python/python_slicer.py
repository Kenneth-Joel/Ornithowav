# -*- coding: utf-8 -*-
"""
Python code that does the following:
    Reads 16kHz wav files
    Filters and estimates signal amplitude envelope
    Segments the signal in 1s slices based on amplitude envelope
    Writes to slices to appropriately names wav files
"""

import numpy as np
import soundfile as sf
from scipy.io import wavfile
import matplotlib.pyplot as plt
import scipy.signal as s
import pandas as pd
import os

#wav = 'testlist/yebsap/XC78062.wav'
#file = 'XC78062.wav'

#wav = 'testlist/brdowl/XC413556.wav'
#file = 'XC413556.wav'

#wav = 'testlist/brdowl/XC333161.wav'
#file = 'XC333161.wav'

#Create the folder if it doesn't exist
#os.mkdir(output_path)

'''
input_path = r"testlist/"
bird_list=os.listdir(input_path)

output_path = r"snipped/"

for bird in bird_list:
    print(bird)
    os.mkdir(output_path+bird)
    #subprocess.call(['ffmpeg', '-i', 'XC2628.mp3','audio.wav'])
'''



#samplerate, data = wavfile.read(wav)

df=pd.read_csv('NewData/train-7.csv')



for folder in os.listdir('testlist/'):
    print(folder)
    for file in os.listdir('testlist/'+folder):
        print(file)

        row=df.loc[df['title'].str.contains(file[:-4])]
        plot_title=file[:-4]+" "+row['ebird_code'].to_string(index=False)+" " +row['type'].to_string(index=False)+ " Rating: " + row['rating'].to_string(index=False)
        
        wav = 'testlist/' +folder+'/' +file
        samplerate, data = wavfile.read(wav)
        
        print("Sample Rate:", samplerate)
        #plt.plot(data)
        
        channels=len(data.shape)
        print(f"number of channels = {channels}")
        
        length = data.shape[0] / samplerate
        print(f"length = {length}s")
              
        
        time = np.linspace(0., length, data.shape[0])
        
        b = [ 0.96345238, -3.85380954,  5.78071431, -3.85380954,  0.96345238]
        a = [ 1.        , -3.92553975,  5.7793789 , -3.78207901,  0.9282405 ]
        c = 1
        if channels == 2:           
            temp = data[:,0]
        
            data_hpf = s.filtfilt(b,a,temp)
            #data_filtered = np.convolve(data_hpf,taps44100,'valid')
            #diff = len(data) - len(data_filtered)
            data_filtered = data_hpf
            data_rect=np.abs(data_filtered[::400])
         
            envelope = np.convolve(data_rect,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])/9
            #plt.plot(time[:-diff], data_filtered, label="Filtered Signal")          
            time2 = np.linspace(0., length, envelope.shape[0])
        
            dr = (max(envelope)/min(envelope))
            mean = (np.ones(len(envelope))*np.mean(envelope))*1.5
        
            print(len(mean),len(envelope))
        
        if channels == 1:                             
            data_hpf = s.filtfilt(b,a,data)
            #data_filtered = np.convolve(data_hpf,taps44100,'valid')
            #diff = len(data) - len(data_filtered)
            data_filtered = data_hpf
            data_rect=np.abs(data_filtered[::400])
        
            envelope = np.convolve(data_rect,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])/9
                     
            time2 = np.linspace(0., length, envelope.shape[0])
            dr = (max(envelope)/min(envelope))
            mean = (np.ones(len(envelope))*np.mean(envelope))*1.5
         
        
        time2 = np.linspace(0., length, envelope.shape[0])
        mean = (np.ones(len(envelope))*np.mean(envelope))*1.5
        
        
        compare = np.zeros(len(envelope))
        sr = 16000
        i=0
        for sample in envelope:
            if(sample > mean[i]):
                compare[i]=1
            i=i+1
        
        zcd=np.convolve(compare,[-1,1])
        
        start,=np.where(zcd == -1)
        end,=np.where(zcd == 1)
        
        timestep = time2[3]-time2[2]
        duration_seconds = np.subtract(end,start)*timestep
        duration_samples = np.floor(duration_seconds*16000)
        
        i = -1
        for duration in duration_samples:
            i = i + 1
            if duration < 16000:
                difference = 16000 - duration
                start_index = int(np.floor(start[i]*timestep*16000 - difference/2))
                end_index = int(np.floor(end[i]*timestep*16000 + difference/2))
                file_name='snipped' + wav[8:-4] + '-' + str(i) + '.wav'
                sf.write(file_name, data[start_index:end_index], sr)
            else:
                difference = np.floor((np.ceil(duration_seconds[i]) - duration_seconds[i])*16000)
                start_index = int(np.floor(start[i]*timestep*16000 - difference/2))
                end_index = int(np.floor(end[i]*timestep*16000 + difference/2))
                stop = int(np.ceil(duration_seconds[i]))
                for k in range (0,stop):
                    file_name = 'snipped'+wav[8:-4]+'-'+str(i)+'-'+str(k)+'.wav'
                    sf.write(file_name, data[(start_index+k*16000):(start_index+((k+1)*16000))], sr)
