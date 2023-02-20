from tensorflow.keras.models import load_model
import cv2
import numpy as np
from helper import *
from glob import glob
import argparse
from pathlib import Path

mod = load_model('E:/WORK2/ColorShaddingFrame/sketchKeras-master/mod.h5')

def parse_args():
    desc = "LineDistiller: Make a colored image into line"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input_path', type=str, default='LineDistiller-master/input', help='Path to the test data root directory')
    parser.add_argument('--output_path', type=str, default='LineDistiller-master/output', help='Path to the output data root directory')
    args = parser.parse_args()
    return args

def get(args):
    image_list=glob(args.input_path+'/*')
    print(image_list)
    Path(args.output_path).mkdir(parents=True, exist_ok=True)
    for i in image_list:
        from_mat = cv2.imread(i)
        width = float(from_mat.shape[1])
        height = float(from_mat.shape[0])
        new_width = 0
        new_height = 0
        if (width > height):
            from_mat = cv2.resize(from_mat, (512, int(512 / width * height)), interpolation=cv2.INTER_AREA)
            new_width = 512
            new_height = int(512 / width * height)
        else:
            from_mat = cv2.resize(from_mat, (int(512 / height * width), 512), interpolation=cv2.INTER_AREA)
            new_width = int(512 / height * width)
            new_height = 512
        #cv2.imshow('raw', from_mat)
        cv2.imwrite('raw.jpg',from_mat)
        from_mat = from_mat.transpose((2, 0, 1))
        light_map = np.zeros(from_mat.shape, dtype=np.float)
        for channel in range(3):
            light_map[channel] = get_light_map_single(from_mat[channel])
        light_map = normalize_pic(light_map)
        light_map = resize_img_512_3d(light_map)
        line_mat = mod.predict(light_map, batch_size=1)
        line_mat = line_mat.transpose((3, 1, 2, 0))[0]
        line_mat = line_mat[0:int(new_height), 0:int(new_width), :]
        #show_active_img_and_save('sketchKeras_colored', line_mat, 'sketchKeras_colored.jpg')
        line_mat = np.amax(line_mat, 2)
        #show_active_img_and_save_denoise_filter2('sketchKeras_enhanced', line_mat, 'sketchKeras_enhanced.jpg')
        #show_active_img_and_save_denoise_filter('sketchKeras_pured', line_mat, 'sketchKeras_pured.jpg')
        show_active_img_and_save_denoise('sketchKeras', line_mat, args.output_path+'/'+i.split('\\')[-1])
        print(args.output_path+'/'+i.split('\\')[-1]+' is saved')
    return
    
    
    
arg=parse_args()
get(arg)