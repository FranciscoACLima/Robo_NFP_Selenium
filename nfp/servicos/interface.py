import PySimpleGUI as sg


def abrir_popup(texto='', tempo=None):
    if tempo:
        sg.PopupAutoClose(texto, auto_close_duration=tempo)
    else:
        sg.Popup(texto)
