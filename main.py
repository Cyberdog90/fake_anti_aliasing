import cv2 as cv
import os
import tkinter.filedialog
import subprocess
import glob


def main(img):
    file_name = file_survey()
    img = cv.imread(img)
    edge = cv.Canny(img, 70, 200)
    blur = cv.blur(img, (2, 2))
    img = blur_f(img, blur, edge)
    cv.imwrite("./data/{}.jpg".format(file_name), img)
    dir_name = os.path.dirname(os.path.abspath(__file__)).replace("/", "\\")
    subprocess.run("explorer {}\\data".format(dir_name))


def blur_f(img, blur, edge):
    w, h = img.shape[:2]
    mask = make_mask(edge.copy(), w, h)
    for i in range(w):
        for j in range(h):
            if mask[i][j] == 255:
                img[i][j] = blur[i][j]
    return img


def make_mask(edge, w, h):
    blank_img = edge.copy()
    for i in range(w):
        for j in range(h):
            blank_img[i][j] = 0
    for i in range(w):
        for j in range(h):
            try:
                if edge[i][j] == 255:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            blank_img[i + k][j + l] = 255
            except IndexError:
                pass
    return blank_img


def file_survey():
    flag = 0
    while True:
        print("Please enter filename for save. : ", end="")
        file_name = input()
        dir_files = glob.glob("./data/*")
        for name in dir_files:
            name = os.path.basename(name)
            name = name.strip(".jpg")
            if name == file_name:
                flag += 1
        if flag == 1:
            print("This filename already exist. Do you want to overwrite?(y/other) : ", end="")
            yn = input()
            if yn == "y":
                return file_name
            else:
                flag -= 1
        else:
            return file_name


if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    file_type = [("image", "*")]
    initial_dir = os.path.abspath(os.path.dirname(__file__))
    main(img=tkinter.filedialog.askopenfilename(filetypes=file_type,
                                                initialdir=initial_dir))
