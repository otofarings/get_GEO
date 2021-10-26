import pandas as pd
from time import sleep

from config import CLIENT
from config import LIMIT


class GetCoordinates:
    def __init__(self):
        self.result_adresses = {'Address': [], 'Lon': [], 'Lat': []}

        self.path = ''
        self.path_to_save = ''
        self.save = False

        self.radius = '500'
        self.search_option = ''

        self.row_addresses = []
        self.data = pd.DataFrame()
        self.result = pd.DataFrame()

    def check_search_option(self):
        if self.search_option == 'addresses':
            self.get_coordinates()
        elif self.search_option == 'regions':
            self.get_region()

    def get_coordinates(self):
        self.read_file_with_addresses()
        self.take_coordinates()
        if self.save:
            self.format_results()
            self.saving_results()
        else:
            self.format_results()

    def read_file_with_addresses(self):
        with open(self.path, 'r', encoding='UTF-8') as file:
            for i in file.readlines():
                self.row_addresses.append(i.replace('Россия, Московская область,', '').replace('Россия,', '').strip())
        self.data = pd.DataFrame(self.row_addresses, columns=['address'])
        print('Addresses saved successfully')

    def take_coordinates(self):
        for address in self.data.address:
            coordinates = ['-', '-']
            try:
                coordinates = CLIENT.coordinates(address)
            except:
                pass
            # print(address + ' - ' + str(coordinates))
            self.result_adresses['Address'].append(address)
            self.result_adresses['Lon'].append(str(coordinates[0])[:7])
            self.result_adresses['Lat'].append(str(coordinates[1])[:7])
            sleep(2)
        print('Сoordinates received successfully')

    def format_results(self):
        self.result = pd.DataFrame(self.result_adresses)
        for index in range(len(self.result.Lon)):
            self.result['frmt'] = f'{self.result.Lon[index]};{self.result.Lat[index]};{self.radius}'
        for obj in self.result['frmt']:
            print(obj)
        print('Formatting end successfully')

    def saving_results(self):
        self.result.to_excel(f'{self.path_to_save}/{self.search_option}.txt', encoding='UTF-8')
        print('Data saved successfully')

    def get_region(self):
        df = pd.read_excel('source/Regions.xlsx')
        df['Город'] = df['Город'].str.strip()
        df['Регион'] = df['Регион'].str.strip()

        lst = []
        with open(self.path, 'r') as file:
            for i in file.readlines():
                lst.append(i.strip())

        regions = df[df['Город'].isin(lst)].groupby(['Регион']).count()
        for region in regions.index:
            print(region)


if __name__ == '__main__':
    pass