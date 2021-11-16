from moviepy.editor import VideoFileClip
import moviepy.editor
from pyunpack import Archive
import requests
import PIL
import cv2
import re
import glob
import shutil, time
import os
from tqdm import tqdm as tbar
from PIL import Image, ImageFont, ImageOps, ImageDraw
import easygui
from tkinter import Tk
import tkinter as tk
from shutil import copyfile
global directory_path
global images_save_type
global file_padding
global FIXED_NEW_WIDTH
FIXED_NEW_WIDTH = 200
global target_directory
global current_list
directory_path = os.path.dirname(os.path.realpath(__file__))  # gets directory
supported_types = [".jpg", ".png", "jpg", "png"]
main_body_run = False
def delete_check(target,typeof):
    if typeof == "file":
        if os.path.isfile(target):
            os.remove(target)
    if typeof == "path":
        if os.path.exists(directory_path + target) == True:
            shutil.rmtree(directory_path + target)
def delete():
    delete_check_list_file = ["clip_audio.mp3","output.mp4","ffmpeg_compile_log.txt","output_with_audio.mp4","ffmpeg.7z"]
    delete_check_list_path = ["\\output","\\data","\\ffmpeg","\\ffmpeg_initial","\\fonts","\\iteration"]
    for target in delete_check_list_file:
        delete_check(target,"file")
    for target in delete_check_list_path:
        delete_check(target,"path")
    delete_list = []
    # gets up to date list of files in directory
    current_list = os.listdir(directory_path)
    for i in current_list:  # for each file in current_list it checks to see if the file is .jpg and if it is it adds it to new_list
        if i.endswith((".jpg", ".png", "jpg", "png")):
            delete_list.append(i)
    if not delete_list == []:
        for i in delete_list:
            delete_check((directory_path + "\\" + i), "file")

def get_inputs(prexisting_or_not):
    global FIXED_NEW_WIDTH
    global file_padding
    global vid_name
    global images_save_type
    if prexisting_or_not == "not":
        if easygui.ynbox('Would you like to choose advanced options?', "Ascii Video Tools", ('Yes', 'No')) == True:
            if easygui.ynbox('Would you like to choose file type?', "Ascii Video Tools", ('Yes', 'No')) == True:
                images_save_type = easygui.buttonbox('What image type to save as?', "Ascii Video Tools", ('jpg', 'png'))
                images_save_type = "." + images_save_type
            else:
                images_save_type = ".png"
            if easygui.ynbox('Would you like to choose padding amount?', "Ascii Video Tools", ('Yes', 'No')) == True:
                file_padding = int(easygui.integerbox('What amount of file padding to use? Reccomended amount is 1-5\n Max amount is 99',"File padding"))
            else:
                file_padding = 0
            if easygui.ynbox("Would you like to choose the level of detail?", "Ascii Video Tools", ('Yes', 'No')) == True:
                FIXED_NEW_WIDTH = int(easygui.buttonbox('What detail level would you like to use? Choose from 1-5.\n The higher the detail level, the more computing power required and longer this will take.', "Ascii Video Tools", ('1', '2','3', '4', '5'))) * 100
            else:
                FIXED_NEW_WIDTH = 200
        else:
            easygui.msgbox("Using default config")  
            images_save_type = ".png"
            file_padding = 0
            FIXED_NEW_WIDTH = 200
        easygui.msgbox('Choose video...')
        vid_name = easygui.fileopenbox("Select video","","*.mp4")
        vid_name = str(vid_name)  # converts to string
    if prexisting_or_not == "non_ascii_folder":
        vid_name = False
        if easygui.ynbox('Would you like to choose advanced options?', "Ascii Video Tools", ('Yes', 'No')) == True:
            if easygui.ynbox('Would you like to choose file type?', "Ascii Video Tools", ('Yes', 'No')) == True:
                images_save_type = easygui.buttonbox('What image type to save as?', "Ascii Video Tools", ('jpg', 'png'))
                images_save_type = "." + images_save_type
            else:
                images_save_type = ".png"
            if easygui.ynbox('Would you like to choose padding amount?', "Ascii Video Tools", ('Yes', 'No')) == True:
                file_padding = int(easygui.integerbox('What amount of file padding to use? Reccomended amount is 1-5\n Max amount is 99',"File padding"))
            else:
                file_padding = 0
            if easygui.ynbox("Would you like to choose the level of detail?", "Ascii Video Tools", ('Yes', 'No')) == True:
                FIXED_NEW_WIDTH = int(easygui.buttonbox('What detail level would you like to use? Choose from 1-5.\n The higher the detail level, the more computing power required and longer this will take.', "Ascii Video Tools", ('1', '2','3', '4', '5'))) * 100
            else:
                FIXED_NEW_WIDTH = 200
        else:
            easygui.msgbox("Using default config")  
            images_save_type = ".png"
            file_padding = 0
            FIXED_NEW_WIDTH = 200
    if prexisting_or_not == "ascii_folder":
        vid_name = False
        if easygui.ynbox('Would you like to choose advanced options?', "Ascii Video Tools", ('Yes', 'No')) == True:
            if easygui.ynbox('Would you like to choose file type?', "Ascii Video Tools", ('Yes', 'No')) == True:
                images_save_type = easygui.buttonbox('What image type to save as?', "Ascii Video Tools", ('jpg', 'png'))
                images_save_type = "." + images_save_type
            else:
                images_save_type = ".png"
            if easygui.ynbox('Would you like to choose padding amount?', "Ascii Video Tools", ('Yes', 'No')) == True:
                file_padding = int(easygui.integerbox('What amount of file padding to use? Reccomended amount is 1-5\n Max amount is 99',"File padding"))
            else:
                file_padding = 0
        else:
            easygui.msgbox("Using default config")  
            images_save_type = ".png"
            file_padding = 0
            FIXED_NEW_WIDTH = 200



def variable_set(type):
    global ASCII_CHARS
    global IMAGE_PATH
    global GRAYSCALE
    global PIXEL_ON 
    global PIXEL_OFF
    global DEFAULT_FONT_PATH
    global duration
    global vid_name
    global clip

    if type == "video":
        clip = VideoFileClip(vid_name)
        duration = clip.duration

    PIL.Image.MAX_IMAGE_PIXELS = (
        FIXED_NEW_WIDTH * FIXED_NEW_WIDTH) * (FIXED_NEW_WIDTH * FIXED_NEW_WIDTH)
    ASCII_CHARS = ['@', '#', '8', '&', 'o', ':', '*', '+', ',', '.', ' ']
    IMAGE_PATH = 1
    GRAYSCALE = 'L'
    PIXEL_ON = 0  # PIL color to use for "on"
    PIXEL_OFF = 255  # PIL color to use for "off"
    DEFAULT_FONT_PATH = 'fonts/Courier New.ttf'
    '''
    * Credits: 
        - https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python
        - https://github.com/kobejohn/polymaze/blob/master/polymaze/polygrid.py#L207-L261
    '''
def choice():
    global run_type
    run_type = easygui.buttonbox('What would you like to run?',"Ascii Video Tools",("Convert mp4 video\ninto ascii video","Convert single non ascii image\nin to ascii image","Convert prexisting folder\nof non ascii images into\nascii video", "Convert prexisting folder\nof ascii images into video"))
choice()
if run_type == "Convert mp4 video\ninto ascii video":
    delete()
    get_inputs("not")
    variable_set("video")
    main_body_run = True
    main_body_type = "video"
def string_image(string, font_path=None):
    """Convert string to a grayscale image with black characters on a white background.
    arguments:
    string - this string will be converted to an image
             if string has "\n" token in it, interpret it as a newline
    font_path - path to a font file (for example impact.ttf)
    """

    ''' For array parsing to lines
    # lines = tuple(l for l in array)
    '''

    lines = string.split('\n')

    # Choosing font
    large_font = 100  # get better resolution with larger size
    font_path = font_path or 'fonts/Courier.dfont'
    try:
        font = ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = ImageFont.load_default()
        print('Chosen font could not bed used. Using default font.')

    # make the background image based on the combination of font and lines
    # convert points to pixels
    def pt2px(pt): return int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = Image.new(GRAYSCALE, (width, height), color=PIXEL_OFF)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    # reduced spacing seems better
    line_spacing = int(round(max_height * 0.65))
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing

    # crop the text
    c_box = ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image


def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    def convert(text): return int(text) if text.isdigit() else text
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)


def pixels_to_image_array(ascii_pixels, width):
    ''' Unflattening the array
    * range(0, len(pixels), width)
        - Create a sequence of numbers from 0 to length of pixels
        - but increment by the width instead of 1.
    * pixels[i:i+width]
        - This creates the row of the matrix
    '''
    return [ascii_pixels[i: i + width] for i in range(0, len(ascii_pixels), width)]


def image_array_to_string(image):
    return '\n'.join(image)


def asciify_pixels(image, groups=25):
    pixels = list(image.getdata())
    ascii_pixels = [ASCII_CHARS[pixel_intensity//groups]
                    for pixel_intensity in pixels]
    return ''.join(ascii_pixels)


def convert_to_grayscale(image):
    return image.convert(GRAYSCALE)


def resize(image, new_width=FIXED_NEW_WIDTH):
    initial_width, initial_height = image.size
    aspect_ratio = float(initial_height)/float(initial_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))


def apply_magic(image):
    resized_image = resize(image)
    grayscale_image = convert_to_grayscale(resized_image)
    ascii_pixels = asciify_pixels(grayscale_image)
    final_image = pixels_to_image_array(ascii_pixels, resized_image.width)
    return image_array_to_string(final_image)

def font_get():
    if not os.path.exists(directory_path + "\\fonts") or os.stat(directory_path + "\\fonts").st_size == 0:
        if not os.path.exists(directory_path + "\\fonts"):
            os.mkdir(directory_path + "\\fonts")  # creates directory
    response = requests.get(
        "https://github.com/KhorSL/ASCII-ART/raw/master/fonts/Courier%20New.ttf")
    font_file = open("fonts\\Courier New.ttf", "wb")
    font_file.write(response.content)
    font_file.close()

def convert_main(file,vid_or_image):
    run_default = False
    if vid_or_image == "img_from_non_ascii_folder_iteration":
        image_path = directory_path + "\\iteration\\" + file
        run_default = True
    if vid_or_image == "img_from_non_ascii_folder_data":
        image_path = directory_path + "\\data\\" + file
        run_default = True
    if vid_or_image == "vid":
        image_path = directory_path + "\\data\\" + file
        run_default = True
    if run_default == True:    
        try:
            image = Image.open(image_path)
        except Exception:
            print("Unable to find image in", image_path)
            return

        final_image = apply_magic(image)

        ''' To save a .png file '''
        image = string_image(final_image, DEFAULT_FONT_PATH)
        image.save(directory_path + "\\output\\" + str(file))
        
    if vid_or_image == "image":
        image_path = directory_path + "\\data\\" + file

        try:
            image = Image.open(file)
        except Exception:
            print("Unable to find image in", file)
            return

        final_image = apply_magic(image)

        ''' To save a .png file '''
        image = string_image(final_image, DEFAULT_FONT_PATH)
        save_file = easygui.filesavebox("Select image","",os.path.basename(file),("*.png","*.jpg",".jpeg"))
        image.save(save_file)


def vsplit(vid_name):
    # Importing all necessary libraries
    import cv2
    import os

    # Read the video from specified path
    cam = cv2.VideoCapture(vid_name)

    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while(True):
        # reading from frame
        ret, frame = cam.read()
        currentframename = str(currentframe).zfill(int(file_padding))
        if ret:
            # if video is still left continue creating images
            name = './data/' + str(currentframename) + str(images_save_type)
            # writing the extracted images
            cv2.imwrite(name, frame)
            # increasing counter so that it will
            # show how many frames are created
            (currentframe) += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

def resize_ascii_images():
    images = [file for file in os.listdir(
        "output") if file.endswith((images_save_type))]
    print("Resizing images")
    with tbar(total=len(images)) as pbar:
        for image in images:
            img = Image.open("output\\" + image)
            img.thumbnail((3000, 2000))
            img.save("output\\" + image, optimize=True, quality=40)
            pbar.update(1)

def ffmpeg_install():
    print("Installing FFmpeg...")
    print("Checking for existing ffmpeg installation")
    delete_check("ffmpeg_initial","path")
    delete_check("ffmpeg","path")
    delete_check("ffmpeg.7z","file")

    print("Downloading ffmpeg")
    file_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    response = requests.get(file_url)
    file = open("ffmpeg.7z", "wb")
    file.write(response.content)
    file.close()
    print("Successfully downloaded")
    print("Extracting ffmpeg")
    os.mkdir("ffmpeg_initial")
    Archive('ffmpeg.7z').extractall("ffmpeg_initial")
    time.sleep(1)
    file_name = os.listdir("ffmpeg_initial")
    os.rename(directory_path +"\\ffmpeg_initial\\" + file_name[0],directory_path +"\\ffmpeg")
    print("Successfully extracted ffmpeg")
    print("Removing installation files")
    delete_check("ffmpeg_initial","path")
    delete_check("ffmpeg.7z","file")
    print("FFmpeg successfully installed.")

def extract_audio(clip):
    delete_check((directory_path + "\\clip_audio.mp3"), "file")
    audio = clip.audio
    audio.write_audiofile("clip_audio.mp3")
def main_body(type):
    if type == "video":
        font_get()
        vsplit(vid_name)

        if not os.path.exists(f"{directory_path}\\output"):
            os.mkdir("output")

        old_list = os.listdir(directory_path + "\\data")
        sort_nicely(old_list)
        print("Converting into ascii")
        with tbar(total=len(old_list),) as pbar:
            for f in old_list:
                file_split = f.split(".")
                interger = [s for s in file_split if s.isdigit()]
                file = ((str(interger[0])).zfill(int(file_padding))) + images_save_type
                convert_main(file,"vid")
                pbar.update(1)

        if int(file_padding) <= 0:
            padding = str("%d")
        if int(file_padding) > 0:
            padding = "%" + str(file_padding) + "d"

        ffmpeg_install()
        clip = VideoFileClip(vid_name)
        duration = clip.duration
        fps = round(len(old_list) / duration)

        img= Image.open(directory_path + "\\output\\0.png")
        w,h = img.size
        if not w <= 3000 or not h <= 2000:
            resize_ascii_images()

        ffmpeg_compile_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -f image2 -r " + str(fps) + " -i " + str(
            directory_path) + "\\output\\" + str(padding) + str(images_save_type) + " -vcodec h264 -y " + str(directory_path) + "\\output.mp4"+ " 2>ffmpeg_compile_log.txt"
        os.system('cmd /c' + ffmpeg_compile_command)

        extract_audio(clip)

        audio_combine_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -i "+ str(directory_path) + "\\output.mp4 -i "+ str(directory_path) + "\\clip_audio.mp3 -map 0:v -map 1:a -c:v copy -shortest output_with_audio.mp4 2>ffmpeg_compile_log.txt"
        os.system('cmd /c' + audio_combine_command)

        delete_check("\\fonts","path")
        delete_check("\\data","path")
        delete_check("\\ffmpeg","path")
    
    
    if type == "prexisting":
        if os.path.exists(f"{directory_path}\\output"):
            delete_check("\\output","path")
        if not os.path.exists(f"{directory_path}\\output"):
            os.mkdir("output")
        if os.path.exists(f"{directory_path}\\data"):
            delete_check("\\data","path")    
        if not os.path.exists(f"{directory_path}\\data"):
            os.mkdir("data")     
        font_get()
        old_list = os.listdir(target_directory)
        sort_nicely(old_list)
        iteration = "0"
        iteration_or_not = False
        if os.path.exists(directory_path + "\\iteration"):
            delete_check("\\iteration","path")
        if not os.path.exists(directory_path + "\\" +"iteration"):
            os.mkdir(directory_path + "\\" +"iteration")
        print("Moving Files ")
        with tbar(total=len(old_list),) as pbar:
            for file in old_list:
                if not file == str(iteration) + images_save_type:
                    copyfile(target_directory + "\\" + file, (directory_path + "\\iteration\\" + str(iteration) + images_save_type))
                    pbar.update(1)
                    iteration_or_not = True
                else:
                    copyfile(target_directory + "\\" + file, (directory_path + "\\data\\" + file))
                iteration = int(iteration) + 1
                pbar.update(1)
                
        print("Converting into ascii")
        if iteration_or_not == True:
            new_list = os.listdir(directory_path + "\\iteration")
        if iteration_or_not == False :
            new_list = os.listdir(directory_path + "\\data")
        sort_nicely(new_list)
        with tbar(total=len(new_list),) as pbar:
            for f in new_list:
                file_split = f.split(".")
                interger = [s for s in file_split if s.isdigit()]
                file = ((str(interger[0])).zfill(int(file_padding))) + images_save_type
                if iteration_or_not == True:
                    convert_main(file,"img_from_non_ascii_folder_iteration")
                if iteration_or_not == False:
                    convert_main(file,"img_from_non_ascii_folder_data")
                pbar.update(1)
        
            if int(file_padding) <= 0:
                padding = str("%d")
            if int(file_padding) > 0:
                padding = "%" + str(file_padding) + "d"

            ffmpeg_install()
        if easygui.ynbox("Do you have a clip to find the fps of?\nif no fps is found the final result may be out of sync","Ascii Video Tools") == "Yes":
            clip = VideoFileClip(easygui.fileopenbox("Select Video To Find fps of"))
            duration = clip.duration
            fps = round(len(old_list) / duration)
        else:
            fps = 0
            try:
                while not 20 <= fps <= 30:
                    fps = easygui.integerbox("Please input the fps to compile at.\nMinimum is 20\nMaximum is 30","Ascii Video Tools")
            except TypeError:
                try:
                    restart = easygui.ynbox("Would you like to choose another tool?")
                    if restart == "Yes":
                        choice()
                except TypeError:
                    print("Thanks for trying this tool out")

            img= Image.open(directory_path + "\\output\\0.png")
            w,h = img.size
            if not w <= 3000 or not h <= 2000:
                resize_ascii_images()

            ffmpeg_compile_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -f image2 -r " + str(fps) + " -i " + str(
                directory_path) + "\\output\\" + str(padding) + str(images_save_type) + " -vcodec h264 -y " + str(directory_path) + "\\output.mp4"+ " 2>ffmpeg_compile_log.txt"
            os.system('cmd /c' + ffmpeg_compile_command)

            if easygui.ynbox("Do you have an audio file you would like to combine with the output?","Ascii Video Tools") == "yes":
                audio_file = easygui.fileopenbox("Select audio file","","",("*.mp3"))
                audio_combine_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -i "+ str(directory_path) + "\\output.mp4 -i "+ str(directory_path) + "\\"+ str(audio_file) +" -map 0:v -map 1:a -c:v copy -shortest output_with_audio.mp4 2>ffmpeg_compile_log.txt"
                os.system('cmd /c' + audio_combine_command)
            if easygui.ynbox("Do you have a video you would like to strip audio from and combine with the output?","Ascii Video Tools") == "yes":
                extract_audio(str(VideoFileClip(audio_file = easygui.fileopenbox("Select video","","",("*.mp4")))))
                audio_combine_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -i "+ str(directory_path) + "\\output.mp4 -i "+ str(directory_path) + "\\clip_audio.mp3 -map 0:v -map 1:a -c:v copy -shortest output_with_audio.mp4 2>ffmpeg_compile_log.txt"
                os.system('cmd /c' + audio_combine_command)

if run_type == "Convert single non ascii image\nin to ascii image":
    delete()
    easygui.msgbox('Choose image...')
    file = easygui.fileopenbox("Select image","","",("*.png","*.jpg",".jpeg"))
    if easygui.ynbox("Would you like to choose the level of detail?", "Ascii Video Tools", ('Yes', 'No')) == True:
        FIXED_NEW_WIDTH = int(easygui.buttonbox('What detail level would you like to use? Choose from 1-5.\n The higher the detail level, the more computing power required and longer this will take.', "Ascii Video Tools", ('1', '2','3', '4', '5'))) * 100
    else:
        FIXED_NEW_WIDTH = 200
    variable_set("image")
    font_get()
    convert_main(file,"image")
    if easygui.ynbox("Would you like to do anything else with this tool","Ascii Video Tools"):
        choice()

if run_type == "Convert prexisting folder\nof non ascii images into\nascii video":
    delete()
    target_directory = easygui.diropenbox("Select folder to combine")
    get_inputs("non_ascii_folder")
    variable_set("prexisting")
    main_body_run = True
    main_body_type = "prexisting"

if run_type == "Convert prexisting folder\nof ascii images into video":
    delete()
    variable_set("prexisting")
    get_inputs("ascii_folder")
    target_directory = easygui.diropenbox("Select folder to combine")
    if os.path.exists(f"{directory_path}\\output"):
        delete_check("\\output","path")
    if not os.path.exists(f"{directory_path}\\output"):
        os.mkdir("output")
    if os.path.exists(f"{directory_path}\\data"):
        delete_check("\\data","path")    
    if not os.path.exists(f"{directory_path}\\data"):
        os.mkdir("data")     
    font_get()
    old_list = os.listdir(target_directory)
    sort_nicely(old_list)
    iteration = "0"
    iteration_or_not = False
    if os.path.exists(directory_path + "\\iteration"):
        delete_check("\\iteration","path")
    if not os.path.exists(directory_path + "\\" +"iteration"):
        os.mkdir(directory_path + "\\" +"iteration")
    with tbar(total=len(old_list),) as pbar:
        for file in old_list:
            if not file == str(iteration) + images_save_type:
                copyfile(target_directory + "\\" + file, (directory_path + "\\iteration\\" + str(iteration) + images_save_type))
                pbar.update(1)
                iteration_or_not = True
            else:
                copyfile(target_directory + "\\" + file, (directory_path + "\\data\\" + file))
            iteration = int(iteration) + 1
            pbar.update(1)
    if int(file_padding) <= 0:
        padding = str("%d")
    if int(file_padding) > 0:
        padding = "%" + str(file_padding) + "d"
    #ffmpeg_install()
    if easygui.ynbox("Do you have a clip to find the fps of?\nif no fps is found the final result may be out of sync","Yes","No") == "Yes":
        clip = VideoFileClip(easygui.fileopenbox("Select Video To Find fps of"))
        duration = clip.duration
        fps = round(len(old_list) / duration)
    else:
        fps = 0
        try:
            while not 20 <= fps <= 30:
                fps = easygui.integerbox("Please input the fps to compile at.\nMinimum is 20\nMaximum is 30","Ascii Video Tools")
        except TypeError:
            try:
                restart = easygui.ynbox("Would you like to choose another tool?")
                if restart == "Yes":
                    choice()
            except TypeError:
                print("Thanks for trying this tool out")
    img= Image.open(directory_path + "\\output\\0.png")
    w,h = img.size
    if not w <= 3000 or not h <= 2000:
        resize_ascii_images()
    ffmpeg_compile_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -f image2 -r " + str(fps) + " -i " + str(
        directory_path) + "\\output\\" + str(padding) + str(images_save_type) + " -vcodec h264 -y " + str(directory_path) + "\\output.mp4"+ " 2>ffmpeg_compile_log.txt"
    os.system('cmd /c' + ffmpeg_compile_command)
    if easygui.ynbox("Do you have an audio file you would like to combine with the output?","Ascii Video Tools") == "yes":
        audio_file = easygui.fileopenbox("Select audio file","","",("*.mp3"))
        audio_combine_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -i "+ str(directory_path) + "\\output.mp4 -i "+ str(directory_path) + "\\"+ str(audio_file) +" -map 0:v -map 1:a -c:v copy -shortest output_with_audio.mp4 2>ffmpeg_compile_log.txt"
        os.system('cmd /c' + audio_combine_command)
    if easygui.ynbox("Do you have a video you would like to strip audio from and combine with the output?","Ascii Video Tools") == "yes":
        extract_audio(str(VideoFileClip(audio_file = easygui.fileopenbox("Select video","","",("*.mp4")))))
        audio_combine_command = str(directory_path) + "\\ffmpeg\\bin\\ffmpeg.exe -i "+ str(directory_path) + "\\output.mp4 -i "+ str(directory_path) + "\\clip_audio.mp3 -map 0:v -map 1:a -c:v copy -shortest output_with_audio.mp4 2>ffmpeg_compile_log.txt"
        os.system('cmd /c' + audio_combine_command)

if main_body_run == True:
    main_body(main_body_type)
