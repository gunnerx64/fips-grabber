from typing import List, Any
from seleniumrequests import Firefox
from datetime import datetime
import openpyxl
import os
from pathlib import Path

from program import Program
class FipsSpider():
    base_url = 'https://fips.ru/'
    entry_url = 'iiss/db.xhtml'
    search_url = 'iiss/search.xhtml'
    programs: List[Program] = []
    output_col_titles = ['дата регистрации','№ свидетельства', 'тип', 'название', 'авторы', 'правообладатель']
    
    def __init__(self):
        self.ids_seen = set()
        self.programs_seen = 0
        self.driver = Firefox()
        self.driver.get(self.base_url + self.entry_url)
        assert(self.driver.title == 'Информационно-поисковая система')
        self.driver.find_element_by_xpath('//form/div[8]').click()
        self.driver.find_element_by_id('db-selection-form:dbsGrid9:0:dbsGrid9checkbox').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_class_name('save').click()
        self.driver.implicitly_wait(3)

    def add_program(self, program):
        self.programs_seen += 1
        if program.id in self.ids_seen:
            pass
            # print(f'пропущена программа {program.id} (уже найдена у другого автора)')
        else:
            self.ids_seen.add(program.id)
            self.programs += [program]

    def parse_program(self):
        res = Program()
        try:
            res.id = self.driver.find_element_by_xpath('//td[@id="top4"]/a').get_attribute("innerHTML")
            res.reg_date = self.driver.find_element_by_xpath('//p[contains(text(),"Дата регистрации:")]/b').get_attribute("innerHTML")
            res.title = self.driver.find_element_by_xpath('//div[@id="mainDoc"]/p[1]/b').get_attribute("innerHTML")
            res.referat = self.driver.find_element_by_xpath('//div[@id="mainDoc"]/p[2]').get_attribute("innerHTML")
            res.authors = self.driver.find_element_by_xpath('//td[@id="bibl"]/p[1]/b').get_attribute("innerHTML")
            res.owner = self.driver.find_element_by_xpath('//td[@id="bibl"]/p[2]/b').get_attribute("innerHTML")

        except Exception as e:
            print(f'ошибка обработки: {e}')
            return None
        # print(f'found {res.id=}')
        # print(f'found {res.authors=}')
        # print(f'found {res.owner=}')
        return res

    def fetch_author_programs(self, credentials):
        # переходим на страницу поиска
        self.driver.get(self.base_url + self.search_url)
        # вбиваем имя автора и нажимаем поиск
        search_input = self.driver.find_element_by_xpath('//input[contains(@id,"fields:5")]')
        search_input.clear()
        search_input.send_keys(f'"{credentials}"')
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_class_name('save').click()
        self.driver.implicitly_wait(1)
        try:
            # открываем ссылку на первую программу
            first_program = self.driver.find_element_by_xpath('//a[@class="tr"]')
            #print(f'found first program {first_program}')
            is_done = False
            self.driver.get(first_program.get_attribute("href"))
        except Exception:
            # print(f'у автора {credentials} программы не найдены')
            is_done = True

        n = 0
        # в цикле пробегаем по всем страницам
        while not is_done:
            program = self.parse_program()
            if program is not None:
                self.add_program(program)
                n += 1
            print(f'Обработка {credentials} #{n}. В базе {len(self.programs)} уникальных программ (из {self.programs_seen}).', end='\r')
            try:
                next_page = self.driver.find_element_by_xpath('//a[@class="ui-link ui-widget modern-page-next"]')
                next_page.click()
            except Exception:
                is_done = True
        else:
            # print(f'\n')
            pass

    def fetch(self, authors):
        for author in authors:
            self.fetch_author_programs(author)

    def write_output(self, file_name: str) -> None:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(self.output_col_titles)
        for program in self.programs:
            ws.append([program.reg_date,
                       program.id,
                       program.kind,
                       program.title,
                       program.authors,
                       program.owner])
        wb.save(file_name + '.xlsx')

    def parse_dir(self, dir_name: str) -> None:
        files = []
        files += [fname for fname in os.listdir(dir_name) if fname.endswith('.xlsx')]
        print(f'файлы для обработки: {files}')
        payload = []
        for file in files:
            try:
                wb = openpyxl.load_workbook(Path(dir_name, file))
                ws = wb.active
                if ws is None:
                    continue
                fios = []
                fio_col = next((col for col in ws.iter_cols(1, ws.max_column) if 'фио' in str(col[0].value).lower()), None)
                if fio_col is None:
                    print(f'файл {file} не содержит ФИО в заголовках!')
                    continue
                fio_col_idx = fio_col[0].col_idx
                print(f'ФИО в стобце {fio_col_idx}')
                for row in ws.iter_rows(2, ws.max_row):
                    fio = row[fio_col_idx - 1].value
                    if fio is None:
                        break
                    fio = str(fio).strip()
                    if fio == '':
                        print(f'некорректное имя в строке {row[fio_col_idx - 1].row}')
                        continue
                    fios += [fio]
                print(f'добавлено {len(fios)} имен из {file}')
                payload += [fios]
            except Exception as e:
                print(f'ошибка при обработке файла: {e}')
        return payload

    def process_dir(self, dir_name: str) -> None:
        payload = self.parse_dir(dir_name)
        for names in payload:
            self.fetch(names)
        now = datetime.now()
        self.write_output(f'Поиск_{now.year}-{now.month}-{now.day}')
        print(f'РАБОТА ЗАВЕРШЕНА. Выгружено {len(self.programs)} программ.')