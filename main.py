import cv2
import pytesseract as tess
import sys


def GetArgs():
    args = list()
    for i, arg in enumerate(sys.argv):
        args.append(str(arg))
    return args

args = GetArgs()

if len(args) < 4:
    print("You have to add arguments!")
    print("For further information read README.md")
    exit()

current_names = args[1]
all_names = args[2]
language = args[3]



def GetAllNames(file_path):
    names = list()
    with open(file_path, 'r', encoding="utf-8", ) as file:
        names = file.read().splitlines()
    return names


def ReadImage(img_path):
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, None, fx = 2, fy = 2, interpolation=cv2.INTER_CUBIC)
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    img_inverted = cv2.bitwise_not(img_gray)
    return img_inverted


def GetNames(img, language):
    raw_names = tess.image_to_string(img, lang=language).strip()
    names = list()
    for name in raw_names.split("\n"):
        if name != "":
            names.append(name)
    return names


def ShowImage(img, desc=""):
    cv2.namedWindow(desc)
    cv2.moveWindow(desc, -1000, 100)
    cv2.imshow(desc,img)
    cv2.waitKey(0)


def GetAbsentNames(img_path, classmates_path, language):
    img = ReadImage(img_path)
    names = GetNames(img, language)
    #ShowImage(img)
    all_names = GetAllNames(classmates_path)
    absent_names = [x for x in all_names if x not in names]
    return absent_names


def PrintAbsentNames(img_path, classmates_path, language):
    absent_names = GetAbsentNames(img_path, classmates_path, language)
    for name in absent_names:
        print(name)

        
PrintAbsentNames(current_names, all_names, language)