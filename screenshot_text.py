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
            return

        if path.exists(self.__cwd + '/tmp.png'):
            remove(self.__cwd + '/tmp.png')
        # Pop up an interface to show that user must use an screen capture
        layout = [[sg.Text('Debe copiar una captura de Pantalla')], [sg.Button('OK')]]
        window = sg.Window('Información', layout)
        while True:
            event, values = window.read()
            if event == 'OK' or event == sg.WIN_CLOSED:
                break
        window.close()

text = CText()
text._to_clipboard()
