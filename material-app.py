# ----------------------------------------------------------------------------
# Proyecto: JRDevs - text_to_screenshot
# Script: material-app.py
# Descripción: GUI implementation of the OCR mecanism programmed in 'trial.py'
# Fecha de creación: 05/February/2023
# Autor: Adam Maltoni
# ----------------------------------------------------------------------------

# Módulos
from trial import *
import pyautogui
import PySimpleGUI as sg
from os import getcwd, path
from win32clipboard import OpenClipboard,EmptyClipboard,SetClipboardData,CF_DIB,CloseClipboard
from io import BytesIO
from PIL import Image

# Variables globales

# Funciones
def send_to_clipboard(image : Image ):
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


def simplify(x): return x[0] if len(x) == 1 else x


def get_path(s): return getcwd()+'\screenshot.png' if (path.exists(s) == False or (
    s.startswith('Path de guardado:') and s.endswith(' '))) else (s+'\screenshot.png')

# Main


def main():

    sg.theme('LightBrown6')

    # Inicio de la ventana
    layout = [[sg.Text('Sube una imagen, toma la pantalla actual o pulsa CRTL+G\nPara tomar una región, pulsa R en una posición de cursor, muévelo y vuelve a pulsar R')],
              [sg.InputText('Path de guardado:')],
              [sg.Button('Get'), sg.FileBrowse(file_types=(("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg"))), sg.Exit()]]

    window = sg.Window('Screenshot-text', layout,
                       return_keyboard_events=True, use_default_focus=False)

    anterior: str = ''

    # Loop principal
    while True:

        # try:

        event, values = window.read()
        path = get_path(values[0])
        print(event, anterior)

        if event == 'r' and anterior != 'r':
            pos1 = pyautogui.position()

        if event == 'r' and anterior == 'r':
            pos2 = pyautogui.position()

            if (pos2[0] > pos1[0]) and (pos2[1] > pos1[1]):
                reg = (pos1[0], pos1[1], abs(
                    pos2[0]-pos1[0]), abs(pos2[1]-pos1[1]))

            elif (pos2[0] < pos1[0]) and (pos2[1] > pos1[1]):
                reg = (pos2[0], pos1[1], abs(
                    pos2[0]-pos1[0]), abs(pos2[1]-pos1[1]))

            elif (pos2[0] > pos1[0]) and (pos2[1] < pos1[1]):
                reg = (pos1[0], pos2[1], abs(
                    pos2[0]-pos1[0]), abs(pos2[1]-pos1[1]))

            elif (pos2[0] < pos1[0]) and (pos2[1] < pos1[1]):
                reg = (pos2[0], pos2[1], abs(
                    pos2[0]-pos1[0]), abs(pos2[1]-pos1[1]))

            elif (pos2[0] == pos1[0]) or (pos2[1] == pos1[1]):
                continue

            imagen = pyautogui.screenshot(region=reg)
            send_to_clipboard(imagen)
            to_read = CText()
            to_read._to_clipboard()
            sg.popup_timed('Got image successfully')


        if event == 'Get' or (event == 'g' and anterior == 'Control_L:17'):
            try:

                imagen = pyautogui.screenshot()
                send_to_clipboard(imagen)
                to_read = CText()
                to_read._to_clipboard()
                sg.popup_timed('Got image successfully')

            except:
                sg.popup_auto_close('Error al obtener la captura')

        # if event == 'Upload image':

        #     print('de aqui qn me va a sacar mera cabron')

        if event == 'Exit' or event == sg.WIN_CLOSED:
            window.close()

        if anterior == 'r':
            anterior = None
        else:
            anterior = event[:]

        # except:
        # break


if __name__ == '__main__':
    main()


# https://pyautogui.readthedocs.io/en/latest/
