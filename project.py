import os # Импорт модуля для работы с операционной системой
import csv # Импорт модуля для работы с CSV файлами
import re # Импорт модуля для работы с регулярными выражениями
import tabulate # Импорт модуля для создания таблиц из данных


class PriceMachine: # Определение класса PriceMachine

    def __init__(self): # Метод инициализации объекта класса
        self.data = []  # Создание пустого списка для хранения данных

    def load_prices(self, directory):  # Метод загрузки цен из файлов
        '''
        Сканирует указанный путь к каталогу. Ищет файлы со словом price в названии.
        В файле ищет столбцы с названием товара, ценой и весом.
        Возвращает список из списков со строками удовлетворяющим патернам

        :param directory: file path from user_input
        :return: self.data = [[filename, product, price, weight, price/kg)]
        '''
        for filename in os.listdir(directory): # Цикл по файлам в указанной директории
            if filename.endswith('.csv') and 'price' in filename.lower(): # Проверка, что файл является CSV файлом и содержит "price" в имени
                with open(os.path.join(directory, filename), 'r', newline='', encoding='utf-8') as file:  # Открытие файла для чтения
                    reader = csv.DictReader(file) # Создание объекта reader для чтения CSV файла как словаря
                    for row in reader: # Цикл по строкам CSV файла
                        for column in row: # Цикл по столбцам строки
                            if re.search(r'(товар|название|наименование|продукт)', column, re.IGNORECASE): # Поиск ключевых слов в названии столбца
                                product = row[column].strip() # Получение названия продукта
                            elif re.search(r'(розница|цена)', column, re.IGNORECASE): # Поиск ключевых слов в названии столбца
                                price = float(row[column].replace(',', '.').strip()) # Получение цены продукта
                            elif re.search(r'(вес|масса|фасовка)', column, re.IGNORECASE): # Поиск ключевых слов в названии столбца
                                weight = float(row[column].replace(',', '.').strip())  # Получение веса продукта
                        if product: # Если есть название продукта
                            self.data.append([filename, product, price, weight, round(price / weight, 2)])  # Добавление данных о продукте в список

    def export_to_html(self, sorted_result): # Метод экспорта данных в HTML
        '''
        Функция принимает подготовленный  список от поисковика search_ingine,
        добавляет заголовоки для таблицы, записывает файл и выводит в консоль
        :param sorted_result: list
         :return: write file *.html
        '''
        # Инициализируем  HTML
        result = ''' # Формирование начала HTML страницы
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>Позиции продуктов</title>
                </head>
                <body>
                <table>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
                '''
        index = 0  # Нумеруем позиции
        for i in sorted_result: # Цикл по отсортированным результатам
            index += 1  # Увеличение индекса на 1
            result += f'''   # Формирование строки HTML таблицы для каждого результата
                <tr>
                    <td>{index}</td> 
                            <td>{i[1]}</td> 
                            <td>{i[2]}</td>
                            <td>{i[3]}{' кг'}</td>
                            <td>{i[0]}</td>
                            <td>{i[4]}</td>                        
                        </tr>
                    '''
        result += '''  # Формирование конца HTML страницы
        </table>
        </body>
        </html>
        '''
        with open('Out data.html', 'w', encoding='utf8') as file:   # Открытие файла для записи HTML данных
            file.write(result)   # Запись HTML данных в файл

        # вывод в консоль:
        headers = ['№', 'Наименование', 'Цена', 'Вес', 'Цена\кг.', 'Файл']  # Заголовки таблицы
        results_num = [[i + 1] + res[1:] + [res[0]] for i, res in enumerate(sorted_result)]  # Нумеруем строчки
        print(tabulate.tabulate(results_num, headers=headers, tablefmt='simple'))  # Вывод таблицы на экран

    def search_engine(self, input_text):  # Метод поискового движка
        '''
        Ищет переданное слово от пользователя в списке от load_price(self.data)
        Возвращает отсортированный результат поиска на экспорт и в консоль
        :param input_text: value(text) from user_input_find_text
        :return: sorted_results
        '''
        results = []  # Создание пустого списка для результатов поиска
        for row in self.data: # Цикл по данным о продуктах
            if re.search(input_text, row[1], re.IGNORECASE):  # Поиск по столбцу с названием
                results.append(row)  # Добавление найденного результата в список результатов
        sorted_results = sorted(results, key=lambda x: x[4])  # # Сортировка результатов по цене за килограмм
        self.export_to_html(sorted_results)  # Передаем остротированный результат на экспорт

    def user_input(self, file_path):  # Метод пользовательского ввода
        """
        Функция осуществляет ввод пользователя и передает искомое значение в поисковик search_engine
        А так же принимает абсолютный путь к папке с файлами и передает в загрузчик load_prices

        :param file_path: file path
        :return: value(text)
        """
        self.load_prices(file_path)  # Загрузка цен из файлов

        while True: # Бесконечный цикл для пользовательского ввода
            find_text_value = input('Что найти ("exit" или "выход" чтобы закончить работу) ?: \n')  # Запрос на ввод текста для поиска или выхода из программы
            if find_text_value.lower() == 'exit' or find_text_value.lower() == 'выход': # Проверка на выход из программы
                print('Поиск завершен') # Вывод сообщения о завершения поиска
                break  # Выход из цикла
            self.search_engine(find_text_value)  # Передаем введненное слово в поисковик


if __name__ == '__main__':
    pm = PriceMachine()
    local_directory = os.path.dirname(os.path.abspath(__file__))  # Абсолютный путь к файлам
    pm.user_input(local_directory)