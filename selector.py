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
import pytesseract
from os import remove, getcwd, walk, path
from PIL import ImageGrab, Image
import pyperclip
import PySimpleGUI as sg
import fnmatch


class CText:


    def __init__(self) -> None:
        '''
        Initialize the CText Class, find the path and create the file where the path will be saved

        Return None

        '''
        # Check out current working directory
        self.__cwd = getcwd()
        # Name the path where we will save the path of tesseract.exe
        file_path = path.join(self.__cwd, 'path_to_tesseract.txt')

        # Create the file
        if not path.exists(file_path):
            # Search path
            tess_path = CText.find('tesseract.exe')
            tess_path = tess_path.replace('\\', '/')
            # Write Path
            with open(file_path, 'w') as f:
                f.write(tess_path)

        # If file is created
        else:

            # Revise if path is in
            with open(file_path, 'r') as f:
                tess_path = f.readline().strip()

            # If Path is not in, search it and save in it
            if not tess_path:
                tess_path = CText.find('tesseract.exe')
                tess_path = tess_path.replace('\\', '/')
                with open(file_path, 'w') as f:
                    f.write(tess_path)
        self.__tess_path : str = tess_path

    @staticmethod
    def find(pattern: str, path='C:/') -> str:
        """
        Finds the pattern of tesseract.

        Return the pattern.
        Args:
            pattern (str): The pattern we are going to find
            path (str): The path where we are going to start the map. Defaults to 'C:/'.

        Raises:
            ValueError: If there is no file tesseract.exe it raise error

        Returns:
            str: Path of tesseract.exe
        """
        for root, _, files in walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    return root + '/' + name
        raise ValueError(f"No se encontró el archivo '{pattern}'")


    def _to_clipboard(self):
        '''
        Method that instantly without Interface get the text of the image'''

        # Get the clipboard
        im= ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):

            # Save image
            complete_path = self.__cwd + '/tmp.png'
            im.save(complete_path)

            pytesseract.pytesseract.tesseract_cmd = self.__tess_path

            # Send it to the model and put in the clippboard
            pyperclip.copy(pytesseract.image_to_string(Image.open(complete_path)))

            # Removes image
            remove(complete_path)
            pass

        if path.exists(self.__cwd + '/tmp.png'):
            remove(self.__cwd + '/tmp.png')
        pass



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