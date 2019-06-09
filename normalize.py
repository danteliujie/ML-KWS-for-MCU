import sys
import input_data
import os.path
import math

TARGET_DB = -20
DEFAULT_SAMPLE_RATE = 16000

def rms(file_path):
  try:
    data = input_data.load_wav_file(file_path)
  except:
    print('failed to load ', file_path)
    raise
  if data.size == 0 :
    print('too small', file_path)

  s = data*data
  start_index = 0
  end_index = 0
  for i in range(0, data.size):
    if (data[i] > 10E-4):
      start_index = i
      break
  for i in range(data.size-1, -1, -1):
    if (data[i] > 10E-4):
      end_index = i
      break
  
  dB = math.log10(s[start_index:end_index+1].mean())*10
  if abs(TARGET_DB-dB) < 0.1 :
    print('skip ', file_path, ' as no need')
    return

  mm = math.pow(10, (TARGET_DB-dB)*0.05)
  data = data * mm
  s = data*data
  print(file_path, ' : ', dB, ' - ', math.log10(s[start_index:end_index+1].mean())*10)
  input_data.save_wav_file(file_path, data, DEFAULT_SAMPLE_RATE)
  
def folder_handle(path) :
  for root, _, files in os.walk(path):
    for filename in files:
      if(filename.endswith(".wav")):
        rms(root + os.path.sep + filename)

def main(args):
  folder_handle(r"D:\tmp\speech_dataset")

if __name__ == '__main__':
  main(sys.argv[1:])
  #rms(r"D:\tmp\speech_dataset\backward\0a2b400e_nohash_0.wav")
