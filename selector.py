# ----------------------------------------------------------------------------
# Proyecto: text-to-screenshot
# Script: selector.py
# Descripción: App funcional de toma de capturas y copia de su contenido
# Fecha de creación: 13/February/2023
# Autor: Josito/Adam
# ----------------------------------------------------------------------------

# Módulos
from __future__ import annotations
from numpy import array
from pyautogui import screenshot
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CF_DIB, CloseClipboard
from io import BytesIO
from os import remove, getcwd, walk
from os.path import exists
from PIL import ImageGrab, Image
from fnmatch import fnmatch
from pytesseract import pytesseract
from pyperclip import copy

from cv2 import EVENT_MOUSEMOVE, EVENT_LBUTTONDOWN, EVENT_LBUTTONUP, namedWindow, WINDOW_NORMAL, setWindowProperty
from cv2 import WND_PROP_FULLSCREEN, setMouseCallback, WINDOW_FULLSCREEN, rectangle, imshow, waitKey, destroyAllWindows


# Clases
class CText:

    def __init__(self):
        cwd = getcwd()
        if not exists(cwd + '/path_to_tesseract.txt'):
            self._file = open('path_to_tesseract.txt', 'w')
            self._tess_path = find('tesseract.exe')
            self._tess_path = self._tess_path.replace('\\', '/')
            self._file.write(self._tess_path)
            self._file.close()
        else:
            self._file = open('path_to_tesseract.txt', 'r')
            self._tess_path = self._file.readlines(1)[0]

    def _to_clipboard(self):
        try:
            im = ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):

                wd = getcwd()
                complete_path = wd + '/tmp.png'
                im.save(complete_path)

                pytesseract.tesseract_cmd = self._tess_path

                copy(pytesseract.image_to_string(
                    Image.open(complete_path)))

                remove(complete_path)

        except:
            pass


# Funciones
def find(pattern, path='C:/'):
    result = []
    for root, _, files in walk(path):
        for name in files:
            if fnmatch(name, pattern):
                result.append(path.join(root, name))

    return result[0]


def send_to_clipboard(image: Image):
    """
    Copies the PIL image passed as an argument to the user's clipboard

    Parameters:
    - image (required): PIL Image -> the image to copy to clipboard

    Returns:
    - None

    """
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    OpenClipboard()
    EmptyClipboard()
    SetClipboardData(CF_DIB, data)
    CloseClipboard()


def take_screenshot():
    image = screenshot()
    return image


def draw_rectangle(event, x, y, __, ___):
    global start, end, drawing
    if event == EVENT_LBUTTONDOWN:
        drawing = True
        start = (x, y)
    elif event == EVENT_MOUSEMOVE:
        if drawing:
            end = (x, y)
    elif event == EVENT_LBUTTONUP:
        drawing = False
        end = (x, y)


# Main
start, end = (-1, -1), (-1, -1)
drawing = False

img = take_screenshot()
img = array(img)

namedWindow("Captura de Pantalla", WINDOW_NORMAL)
setWindowProperty("Captura de Pantalla",
                  WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
setMouseCallback("Captura de Pantalla", draw_rectangle)

while True:
    if start != (-1, -1) and end != (-1, -1):
        img_copy = img.copy()
        rectangle(img_copy, start, end, (134, 218, 235), 2)
        imshow("Captura de Pantalla", img_copy)
    else:
        imshow("Captura de Pantalla", img)

    key = waitKey(1) & 0xFF
    if key == ord("c"):
        break

destroyAllWindows()

x1, y1 = start
x2, y2 = end

if x1 > x2:
    x1, x2 = x2, x1
if y1 > y2:
    y1, y2 = y2, y1

img_cropped = Image.fromarray(img[y1:y2, x1:x2])
# img_cropped.show()
send_to_clipboard(img_cropped)
to_read = CText()
to_read._to_clipboard()
