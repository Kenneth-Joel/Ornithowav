# -*- coding: utf-8 -*-
"""

Python code that converts wav files of different bit rates to 256bps 
(16kHz sampling)

"""

import librosa
import subprocess
import os
import soundfile as sf

input_path = r"OutputData2/"
bird_list=os.listdir(input_path)

output_path = r"Output16ks2/"


#Create the folder if it doesn't exist
#os.mkdir(output_path)
for bird in bird_list:
    print(bird)
    os.mkdir(output_path+bird)
    #subprocess.call(['ffmpeg', '-i', 'XC2628.mp3','audio.wav'])



#Convert files   
for bird in bird_list:
    print(bird)
    input_folder = input_path+bird+'/'
    print(os.listdir(input_folder))
    output_folder = output_path+bird+'/'
    for file in os.listdir(input_folder):
        wav = input_folder+file
        y, s = librosa.load(wav, sr=16000)
        wav16 = output_folder+file[:-3]+"wav"
        #librosa.output.write_wav(wav16, y, s)
        sf.write(wav16, y, s)
        print(wav,wav16)
        print(s)

    
'''
#Number of recordings per bird
input_path = r"birdsong-recognition/train_audio/"
#input_path = r"NewData/"
bird_list=os.listdir(input_path)
for bird in bird_list:
    print()
    input_folder = input_path+bird+'/'
    print(bird,len(os.listdir(input_folder)))
'''