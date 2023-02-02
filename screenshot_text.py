import pytesseract
from os import remove, getcwd, walk, path
from os.path import exists
from PIL import ImageGrab, Image
import pyperclip
import PySimpleGUI as sg
import fnmatch


def find(pattern, path = 'C:/'):
    result = []
    for root, dirs, files in walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(path.join(root, name))
    return result[0]

class CText:

    def find(pattern, path = 'C:/Program Files/'):
        result = []
        for root, dirs, files in walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(path.join(root, name))
        return result

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
            im= ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):

                wd = getcwd()
                complete_path = wd + '/tmp.png'
                im.save(complete_path)

                pytesseract.pytesseract.tesseract_cmd = self._tess_path

                pyperclip.copy(pytesseract.image_to_string(Image.open(complete_path)))

                remove(complete_path)

        except:
            layout = [[sg.Text('Debe copiar una captura de Pantalla')], [sg.Button('OK')]]
            window = sg.Window('Información', layout)
            while True:
                event, values = window.read()
                if event == 'OK' or event == sg.WIN_CLOSED:
                    break
            window.close()



to_read = CText()
to_read._to_clipboard()