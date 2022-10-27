'''
Python code that converts mp3 audio clips to wav
'''


import subprocess
import os

input_path = r"NewData2/"
bird_list=os.listdir(input_path)

output_path = r"OutputData2/"


#Create the folder if it doesn't exist
'''
for bird in bird_list:
    print(bird)
    os.mkdir(output_path+bird)
    #subprocess.call(['ffmpeg', '-i', 'XC2628.mp3','audio.wav'])
''' 


#Convert files   
for bird in bird_list:
    print(bird)
    input_folder = input_path+bird+'/'
    print(os.listdir(input_folder))
    output_folder = output_path+bird+'/'
    for file in os.listdir(input_folder):
        mp3 = input_folder+file
        wav = output_folder+file[:-3]+"wav"
        print(mp3,wav)
        subprocess.call(['ffmpeg', '-i', mp3, wav])


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