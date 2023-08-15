from PySimpleGUI import PySimpleGUI as sg
from pygame import mixer
from mutagen.mp3 import MP3
from os import listdir

# Layout
sg.theme('Reddit')

menu_def = [
    ['Menu', ['a']],
    ['Simples'],
    ['Playlist'],
    #['File', ['Open', 'Save', 'Exit',]],
    #['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
    #['Help', 'About...'],
]

# D:\Documents\Projetinhos\PlayerMusica\musica.mp3

treedata = sg.TreeData()

treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
treedata.Insert("", '_B_', 'B', [])
treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )


def listarMusicas(path):
    lista = listdir(path)
    mp3s = []
    for i in lista:
        if i.endswith('.mp3'): mp3s.append(i)
    return mp3s


layoutMusica=[
    [sg.Text('Insira a música: ',size=(11,1))], # Text 'inserir musica'
    [sg.Input(key='path1',size=(34,1)), sg.FileBrowse(key='path2',size=(7,1))], # Selecionar arquivo de musica
    [sg.Text('Volume:'), sg.Slider(key='Volume',range=(0,100), orientation='h', default_value=40, tick_interval=25, enable_events = True)], # Colocar aqui o controlador de volume por Barra
    [sg.Text(size=(5,1), key="progressoOutput"), sg.ProgressBar(100, orientation='h', size=(20, 10), key='progressbar'), sg.Text(size=(5,1), key="duracaoOutput")] # Barra de progresso da musica
]

layoutPlaylist=[
    
]

layoutBaixar=[
    [sg.T('Link:'), sg.T(size=(21,1)), sg.Button('Baixar')],
    [sg.Input(key='mp3Link')],
    [sg.Output(size=(43,5))]
]

pauseReturnButton=[
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAgCAYAAAAbifjMAAAABmJLR0QA/wD/AP+gvaeTAAAALElEQVRIiWNgGAUDDxgZGBj+45FDBljVMVHqglEDRg0YNWDUgMFjwCgYDAAAp1cCJ8o/+mUAAAAASUVORK5CYII='
]

icons = {
    'pauseReturn' : b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAQAAADZc7J/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAHdElNRQfkCQkAHhdmi2TXAAAAzUlEQVRIx+2UsQ7BYBSFv1QnRmKVeAAx9AkkBvauTBIMVh7Byht0rZ2EB7A0IRJGiVXMFpLfIFKDtr/7Lx161nvPybn35F7IkBYUyUmpFgANAhwTBy6KBzMKMT0Khf/Vr3BDBwA2Iw40ZSN8UGWNT0ku8LZ3pGMiAGU8llTkAgAtTox1wrUiK3mmOuFasdU624RwEwQ0YMdW9/QIpCPcmeAk0aMdrBhwkcZ4pUtbj/7LwYIhN+kSz/TZSI/pyZzav/TwgHZmD8XgpWVIA178dyV8odG1BQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMC0wOS0wOVQwMDozMDoyMyswMDowMOWLjhAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjAtMDktMDlUMDA6MzA6MjMrMDA6MDCU1jasAAAAAElFTkSuQmCC',
    'pauseButton' : b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAgCAYAAAAbifjMAAAABmJLR0QA/wD/AP+gvaeTAAAALElEQVRIiWNgGAUDDxgZGBj+45FDBljVMVHqglEDRg0YNWDUgMFjwCgYDAAAp1cCJ8o/+mUAAAAASUVORK5CYII=",
    'playButton' : b'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'


}

layout = [
    #[sg.Menu(menu_def)],
    [sg.TabGroup([[sg.Tab('Musica',layoutMusica), sg.Tab('Playlist', layoutPlaylist), sg.Tab('Baixar', layoutBaixar)]]) ],
    [sg.HSep()],
    [sg.Button('Tocar', size=(5, 1)), sg.Button(key='Pausar', size=(10,1), image_data=icons['pauseReturn'], button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0), sg.Button('Parar', size=(5, 1)), sg.Button('Sair', button_color=('white', 'red'), font=("Arial", 10), size=(5, 1))], # Botoes de Tocar, Pausar, Retomar e Parar
]

icon = [ #data:image/x-icon;base64,
    b"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"
]

# Janela
janela = sg.Window('Player Bolado', layout, icon=icon[0])


comecouTocar = 0

# Ler eventos
while True:
    eventos, valores = janela.read(timeout=100)

    if eventos == sg.WINDOW_CLOSED or eventos == 'Sair': break

    if eventos == 'Tocar':
        try:
            mixer.init()
            if valores['path1'] != '': mixer.music.load(valores['path1']);path=valores['path1']
            elif valores['path2'] != '': mixer.music.load(valores['path2']);path=valores['path2']
            mixer.music.play()
            mixer.music.set_volume(valores['Volume']/100)
            duracao = MP3(path).info.length
            janela['duracaoOutput'].update(f"{int(duracao)} s")
            comecouTocar = 1
        except: pass

    if eventos == 'Volume':
        try: mixer.music.set_volume(valores['Volume']/100)
        except: pass

    if eventos == 'Pausar':
        if(comecouTocar):
            if (mixer.music.get_busy()):
                mixer.music.pause()
                janela['Pausar'].update(image_data=icons['pauseButton'])
            else:
                mixer.music.unpause()
                janela['Pausar'].update(image_data=icons['pauseReturn'])

    if eventos == 'Retomar':  # Ta crashando qnd clica sem musica
        try: mixer.music.unpause()
        except: pass
    if eventos == 'Parar': 
        try: mixer.music.stop()
        except: pass

    try: 
        posicao = mixer.music.get_pos() # Em milisegundos
        posicao = posicao/1000 # Em segundos
        posicaoPorcent = posicao*100/duracao # porcentagem relativa ao total de duracao
        janela['progressbar'].UpdateBar(posicaoPorcent)
        janela['progressoOutput'].update(f"{int(posicao)} s")
    except: pass


    if eventos == 'Baixar':
        pass



"""
TODO :
MenuBar  --> Para, de repente mudar, de single music pra uma interface de playlist e tals

Barra de progresso de musica --> Pra ver o tamanho da track e quanto falta pra acabar (e talves poder avançar e retroceder na musica.)

Colocar 1 botão só pra Pausar e Retomar a musica, mudando o texto do botão.

"""
