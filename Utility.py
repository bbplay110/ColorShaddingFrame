import glob
import os
from pathlib import Path
from PIL import Image
from PIL import ImageChops
import cv2 as cv
import numpy as np
from shutil import copyfile
from shutil import rmtree
from pathlib import Path
import ipywidgets
import matplotlib.pyplot as plt
from skimage import io

def copy_file(inPath,outPath):
    input_image=glob.glob(inPath+"/*")
    Path(outPath).mkdir(parents=True, exist_ok=True)
    for i in range(len(input_image)):  
        copyfile(input_image[i], outPath+"/"+str(i)+".png")
def delete_folder_content(path):
    rmtree(path)
    Path(path).mkdir(parents=True, exist_ok=True)
    print(path+'\' content are deleted')
def line_thinning(inPath,outPath):
    input_image=glob.glob(inPath+"/*")
    outpath=outPath
    Path(outpath).mkdir(parents=True, exist_ok=True)
    tags=[]
    for i in range(len(input_image)):
        outfile=os.path.join(outpath,str(i)+".png")
        os.system("python line_thinning/thin.py {} {}".format(input_image[i],outfile))
        tags.append(str(i))
        print("Line thining done, file at:"+outfile)
    print("tags:"+str(tags))
def LineNormalizer(inpath,outpath):
    delete_folder_content('LineNormalizer-master/input')
    delete_folder_content('LineNormalizer-master/output')
    #LineDistiller-master
    copy_file(inpath,'LineNormalizer-master/input')
    os.system("python LineNormalizer-master/pytorch_predict_block.py")
    copy_file('LineNormalizer-master/output',outpath)
def LineDistiller(inpath,outpath):
    delete_folder_content('LineDistiller-master/input')
    delete_folder_content('LineDistiller-master/output')
    #LineDistiller-master
    copy_file(inpath,'LineDistiller-master/input')
    os.system("python LineDistiller-master/predict.py")
    copy_file('LineDistiller-master/output',outpath)
def LineCloser(inpath,outpath):
    delete_folder_content('LineDistiller-master/input')
    delete_folder_content('LineDistiller-master/output')
    #LineDistiller-master
    copy_file(inpath,'LineDistiller-master/input')
    os.system("python LineDistiller-master/predict.py")
    copy_file('LineDistiller-master/output',outpath)
def LineNormalizar(inpath,outpath):
    delete_folder_content('LineNormalizer-master/input')
    delete_folder_content('LineNormalizer-master/output')
    #LineDistiller-master
    copy_file(inpath,'LineNormalizer-master/input')
    os.system("python LineNormalizer-master/pytorch_predict_block.py")
    copy_file('LineNormalizer-master/output',outpath)
def LineRelifer(inpath,outpath):
    delete_folder_content('LineRelifer-master/input')
    delete_folder_content('LineRelifer-master/output')
    #LineDistiller-master
    copy_file(inpath,'LineRelifer-master/input')
    os.system("python LineRelifer-master/predict.py")
    copy_file('LineRelifer-master/output',outpath)
def sketchKeras(inPath,outPath):
    os.system("python sketchKeras-master/main.py --input_path {} --output_path {}".format(inPath,outPath))
def canny(inpath,outpath):
    img_list=glob.glob(inpath+'/*')
    Path(outpath).mkdir(parents=True, exist_ok=True)
    for i in img_list:
        
        img = cv.imread(i,0)
        edges = cv.Canny(img,100,20)
        edges=255-edges
        cv.imwrite(outpath+'/'+i.split('\\')[-1],edges)
        print(outpath+'/'+i.split('\\')[-1]+" is saved")
def coloring(inPath,outPath,tag):
    data_dir=Path(inPath).parent
    Path(outPath).mkdir(parents=True, exist_ok=True)
    tagspath = str(Path(inPath).parent)+'/tags.txt'
    f = open(tagspath, 'w')
    f.writelines(tag)
    f.close()
    os.system("python Tag2Pix/main.py  --test --thread=1 --batch=1 --data_dir={} --tag_txt=tags.txt --test_dir={} --result_dir={} --load=Tag2Pix/tag2pix_512.pkl --input_size=512 --no_bn".format(data_dir,inPath.split("/")[-1],outPath))
def shadding(inPath,outPath):
    Path(outPath).mkdir(parents=True, exist_ok=True)
    os.system("python ShadeSketch-master/predict.py --use-smooth --use-norm --direction 810 --input-dir {} --output-dir {}".format(inPath,outPath))
def combine(colorPath,shadingPath,outPath):
    #input_image=glob.glob(colorPath+"/tag2pix_512/*")
    input_image=glob.glob(colorPath+"/*")
    print(input_image)
    input_image1=glob.glob(shadingPath+"/*")
    print(input_image1)
    Path(outPath).mkdir(parents=True, exist_ok=True)
    for i in range(len(input_image)):
        color_img=Image.open(input_image[i])
        shading_img=Image.open(input_image1[i])
        #print(shading_img.size)
        #shading_img.show()
        color_img=color_img.resize(shading_img.size)
        #print(color_img.size)
        #color_img.show()
        output_img=ImageChops.multiply(color_img.convert('RGB'),shading_img.convert('RGB'))
        output_img.save(outPath+"/"+input_image[i].split('\\')[-1])
        print(outPath+"/"+input_image[i].split('\\')[-1]+" is done")
def HSI_Line(inpath,outpath_Line,outpath_Color,outpath_Lumin):
    Path(outpath_Color).mkdir(parents=True, exist_ok=True)
    Path(outpath_Color+"_RGB").mkdir(parents=True, exist_ok=True)
    Path(outpath_Line).mkdir(parents=True, exist_ok=True)
    Path(outpath_Lumin).mkdir(parents=True, exist_ok=True)
    all_Image=glob.glob(inpath+"/*")
    for (index,i) in enumerate(all_Image):
        print("processing:"+i)
        Image=io.imread(i)
        Image=cv.cvtColor(Image, cv.COLOR_RGB2HLS)
        gray=np.ones_like(Image[::,::,0])*128
        Image_Color=Image.copy()
        Image_Color[::,::,1]=gray
        Image_Line=Image.copy()
        Image_Line[::,::,0]=np.zeros_like(Image_Line[::,::,0])
        Image_Line[::,::,2]=np.zeros_like(Image_Line[::,::,2])
        Image_Line=cv.cvtColor(Image_Line, cv.COLOR_HLS2RGB)
        Image_Lumin=Image_Line.copy()
        Image_Line = cv.Canny(Image_Line,100,20)
        Image_Line=255-Image_Line

        print(Image_Line.shape)
        io.imsave(outpath_Color+"/"+str(index)+".jpg", Image_Color)
        
        Image_Color=cv.cvtColor(Image_Color, cv.COLOR_HLS2RGB)
        io.imsave(outpath_Color+"_RGB"+"/"+str(index)+".jpg", Image_Color)
        
        io.imsave(outpath_Lumin+"/"+str(index)+".jpg", Image_Lumin)
        io.imsave(outpath_Line+"/"+str(index)+".jpg", Image_Line)
    return None
def HSI_combine_kai(colorPath,luminPath,shadow_path,outPath):
    input_image=glob.glob(colorPath+"/*")
    input_image1=glob.glob(luminPath+"/*")
    input_image2=glob.glob(shadow_path+"/*")
    Path(outPath).mkdir(parents=True, exist_ok=True)
    for i in range(len(input_image)):
        
        lumin_img=Image.open(input_image1[i])
        shading_img=Image.open(input_image2[i])
        lumin=ImageChops.multiply(lumin_img.convert('RGB'),shading_img.convert('RGB'))
        lumin_image_final=np.array(lumin)
        lumin_image_final=cv.cvtColor(lumin_image_final, cv.COLOR_RGB2HLS)
        #print("lumin")
        #print(io.imshow(lumin_image_final))
        #plt.show()
        color_img=io.imread(input_image[i])
        color_img=cv.resize(color_img, lumin_img.size, interpolation=cv.INTER_AREA)
        #color_img=cv.cvtColor(color_img, cv.COLOR_RGB2HLS)
        #print("color")
        #print(io.imshow(color_img))
        #plt.show()
        color_img[::,::,1]=lumin_image_final[::,::,1]
        color_img=cv.cvtColor(color_img, cv.COLOR_HLS2RGB)
        io.imsave(outPath+"/"+input_image[i].split('\\')[-1],color_img)
        print(outPath+"/"+input_image[i].split('\\')[-1]+" is done")
def HSI_combine(colorPath,luminPath,outPath):
    input_image=glob.glob(colorPath+"/*")
    input_image1=glob.glob(luminPath+"/*")
    Path(outPath).mkdir(parents=True, exist_ok=True)
    for i in range(len(input_image)):
        
        lumin_img=io.imread(input_image1[i])
        #print(lumin_img)
        
        #lumin_img=cv.cvtColor(lumin_img, cv.COLOR_RGB2HLS)
        
        print("lumin")
        print(io.imshow(lumin_img))
        plt.show()
        color_img=io.imread(input_image[i])
        color_img=cv.resize(color_img,(lumin_img.shape[1],lumin_img.shape[0]),interpolation=cv.INTER_AREA)
        print("color")
        print(io.imshow(color_img))
        plt.show()
        color_img[::,::,1]=lumin_img
        color_img=cv.cvtColor(color_img, cv.COLOR_HLS2RGB)
        io.imsave(outPath+"/"+input_image[i].split('\\')[-1],color_img)
        print(outPath+"/"+input_image[i].split('\\')[-1]+" is done")
def HSI_combine_RGB(colorPath,luminPath,outPath):
    input_image=glob.glob(colorPath+"/*")
    input_image1=glob.glob(luminPath+"/*")
    Path(outPath).mkdir(parents=True, exist_ok=True)
    for i in range(len(input_image)):
        
        lumin_img=io.imread(input_image1[i])
        #print(lumin_img)
        
        #lumin_img=cv.cvtColor(lumin_img, cv.COLOR_RGB2HLS)
        
        print("lumin")
        print(io.imshow(lumin_img))
        plt.show()
        color_img=io.imread(input_image[i])
        color_img=cv.resize(color_img,(lumin_img.shape[1],lumin_img.shape[0]),interpolation=cv.INTER_AREA)
        print("color")
        print(io.imshow(color_img))
        plt.show()
        color_img=cv.cvtColor(color_img, cv.COLOR_RGB2HLS)
        color_img[::,::,1]=lumin_img
        color_img=cv.cvtColor(color_img, cv.COLOR_HLS2RGB)
        io.imsave(outPath+"/"+input_image[i].split('\\')[-1],color_img)
        print(outPath+"/"+input_image[i].split('\\')[-1]+" is done")
def erosion(inpath,outpath,iterations_time=1):
    img_list=glob.glob(inpath+'/*')
    Path(outpath).mkdir(parents=True, exist_ok=True)
    for i in img_list:
        image = cv.imread(i,0)
        kernel = np.ones((3,3), np.uint8)
        #dilation=cv.dilate(image, kernel, iterations = 1)
        erosion = cv.erode(image, kernel, iterations = iterations_time)
        cv.imwrite(outpath+'/'+i.split('\\')[-1],erosion)
        print(outpath+'/'+i.split('\\')[-1]+" is saved")
def dilation(inpath,outpath,iterations_time=1):
    img_list=glob.glob(inpath+'/*')
    Path(outpath).mkdir(parents=True, exist_ok=True)
    for i in img_list:
        image = cv.imread(i,0)
        kernel = np.ones((2,2), np.uint8)
        dilation_img=cv.dilate(image, kernel, iterations = iterations_time)
        #erosion = cv.erode(image, kernel, iterations = 1)
        cv.imwrite(outpath+'/'+i.split('\\')[-1],dilation_img)
        print(outpath+'/'+i.split('\\')[-1]+" is saved")
def bilateralFilter(inpath,outpath):
    img_list=glob.glob(inpath+'/*')
    Path(outpath).mkdir(parents=True, exist_ok=True)
    for i in img_list:
        image = cv.imread(i,0)
        bilateral=cv.bilateralFilter(image, 60, 23, 23)
        cv.imwrite(outpath+'/'+i.split('\\')[-1],bilateral)
        print(outpath+'/'+i.split('\\')[-1]+" is saved")
def sketchKeras(inPath,outPath):
    print("start_Sketching")
    os.system("python sketchKeras-master/main.py --input_path {} --output_path {}".format(inPath,outPath))
    print("end_sketching")