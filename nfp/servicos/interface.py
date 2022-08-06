import PySimpleGUI as sg


def abrir_popup(texto='', tempo=None, title=None, custom_text="OK"):
    if tempo:
        sg.PopupAutoClose(texto, auto_close_duration=tempo)
    else:
        sg.Popup(texto, title=title, custom_text=custom_text)

if __name__ == '__main__':
    pass