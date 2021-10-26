import PySimpleGUI as psg
from main_geo import *


class GeoWindow:
    def __init__(self):
        self.layout = [
            [psg.Text('Файл'), psg.InputText(), psg.FileBrowse(),
             psg.Checkbox('адреса'), psg.Checkbox('города')
             ],
            [psg.Text('Радиус \n(по умолчанию 500)'), psg.InputText()
             ],
            [psg.Output(size=(88, 20))],
            [psg.Submit(), psg.Cancel()]
        ]
        self.values = []
        self.sample = ''
        self.option = False

    def start_app(self):
        window = psg.Window('Get Coordinates', self.layout)
        while True:  # The Event Loop
            event, self.values = window.read()
            # print(event, values) #debug
            if event == psg.WIN_CLOSED or event in ('Exit', 'Cancel'):
                break
            if event == 'Submit':
                if self.values[0]:
                    self.sample = GetCoordinates()
                    self.choose_search_option()
                    self.sample.check_search_option() if self.option == 'ok' else print(self.option)
                else:
                    print('Необходимо задать путь до файла с адресами')

    def choose_search_option(self):
        self.option = 'ok'
        if self.values[1] is self.values[2]:
            self.option = 'Выберите одну опцию для поиска'
        elif self.values[1]:
            self.sample.search_option = 'addresses'
            self.saving_path()
            if self.values[3]:
                self.sample.radius = self.values[3]
        elif self.values[2]:
            self.sample.search_option = 'regions'
            self.saving_path()

    def saving_path(self):
        self.sample.path = self.values[0]
        self.sample.save = False
        self.sample.path_to_save = ''
        self.option = 'ok'


if __name__ == '__main__':
    obj = GeoWindow()
    obj.start_app()
