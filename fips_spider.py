import re
from typing import List, Any
# Import any WebDriver class that you would usually import from
# selenium.webdriver from the seleniumrequests module
from seleniumrequests import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# Simple usage with built-in WebDrivers:

class Program:
    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('<.*?>') # удаляет тэги и содержимое
    CLEANTABS = re.compile('\n\t+') # для замены табов и новых строк
    CLEANDOUBLEWS = re.compile('\s\s+') # для замены мульти пробелов

    def __init__(self):
        self.id = None
        self.kind = 'ПрЭВМ'
        self.reg_date = ''
        self.title = ''
        self.__referat = ''
        self.__authors = ''
        self.__owner = ''
    
    @property
    def referat(self):
        return self.__referat
    
    @referat.setter
    def referat(self, value: str):
        self.__referat = value.replace('<b>Реферат:</b><br>','')

    @property
    def authors(self):
        return self.__authors
    
    @authors.setter
    def authors(self, value: str):
        # self.__authors = re.sub(self.CLEANR, '', value)#.replace(',', ', ').strip()
        s = re.sub(self.CLEANR, '', value)
        s = re.sub(self.CLEANTABS, ',', s).replace(',', ', ')
        s = re.sub(self.CLEANDOUBLEWS, ' ', s).strip()
        self.__authors = s
    
    @property
    def owner(self):
        return self.__owner
    
    @owner.setter
    def owner(self, value: str):
        s = re.sub(self.CLEANR, '', value)
        s = re.sub(self.CLEANTABS, ',', s).replace(',', ', ')
        s = re.sub(self.CLEANDOUBLEWS, ' ', s).strip(' ,')
        self.__owner = s

class FipsSpider():
    base_url = 'https://fips.ru/'
    entry_url = 'iiss/db.xhtml'
    search_url = 'iiss/search.xhtml'
    programs = []
    
    def __init__(self):
        self.ids_seen = set()
        self.programs_seen = 0
        self.driver = Firefox()
        self.driver.get(self.base_url + self.entry_url)
        assert(self.driver.title == 'Информационно-поисковая система')
        self.driver.find_element(By.ID, 'db-selection-form:j_idt224').click()
        self.driver.find_element_by_id('db-selection-form:dbsGrid9:0:dbsGrid9checkbox').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.CLASS_NAME, 'save').click()
        self.driver.implicitly_wait(3)

    @classmethod
    def extract_ids(cls, elements: List[Any]):
        res = []
        try:
            for el in elements:
                id = el.get_attribute("id")
                print(f'{id=}')
                if id is not None:
                    res += [id]
        except Exception as e:
            print(e)
        return res

    def add_program(self, program):
        self.programs_seen += 1
        if program.id in self.ids_seen:
            print(f'SKIP PROGRAM {program.id}')
        else:
            self.programs += [program]

    def parse_program(self):
        res = Program()
        try:
            res.id = self.driver.find_element_by_xpath('//td[@id="top4"]/a').get_attribute("innerHTML")
            res.reg_date = self.driver.find_element_by_xpath('//p[contains(text(),"Дата регистрации:")]/b').get_attribute("innerHTML")
            # res.title = self.driver.find_element_by_xpath('//p[@class="TitAbs"]/b').get_attribute("innerHTML")
            res.title = self.driver.find_element_by_xpath('//div[@id="mainDoc"]/p[1]/b').get_attribute("innerHTML")
            res.referat = self.driver.find_element_by_xpath('//div[@id="mainDoc"]/p[2]').get_attribute("innerHTML")
            # res.authors = self.driver.find_element_by_xpath('//p[contains(text(),"Авторы:")]/b').get_attribute("innerHTML")
            res.authors = self.driver.find_element_by_xpath('//td[@id="bibl"]/p[1]/b').get_attribute("innerHTML")
            res.owner = self.driver.find_element_by_xpath('//td[@id="bibl"]/p[2]/b').get_attribute("innerHTML")
            # res.owner = self.driver.find_element_by_xpath('//p[contains(text(),"Правообладател")]/b').get_attribute("innerHTML")

        except Exception as e:
            print(f'ошибка парсинга: {e}')
            return None
        print(f'found {res.id=}')
        print(f'found {res.authors=}')
        print(f'found {res.owner=}')
        return res

    def fetch_author_programs(self, credentials):
        # переходим на страницу поиска
        self.driver.get(self.base_url + self.search_url)
        # вбиваем имя автора и нажимаем поиск
        search_input = self.driver.find_element(By.ID, 'fields:5:j_idt122')
        search_input.clear()
        search_input.send_keys(f'"{credentials}"')
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.CLASS_NAME, 'save').click()
        self.driver.implicitly_wait(1)
        try:
            # открываем ссылку на первую программу
            first_program = self.driver.find_element(By.XPATH, '//a[@class="tr"]')
            #print(f'found first program {first_program}')
            is_done = False
            self.driver.get(first_program.get_attribute("href"))
        except Exception as e:
            print(f'у автора {credentials} программы не найдены')
            is_done = True

        # в цикле пробегаем по всем страницам
        while not is_done:
            program = self.parse_program()
            if program is not None:
                self.add_program(program)
            try:
                next_page = self.driver.find_element(By.XPATH, '//a[@class="ui-link ui-widget modern-page-next"]')
                next_page.click()
            except Exception as e:
                is_done = True
                

    def fetch(self, authors):
        for author in authors:
            self.fetch_author_programs(author)



# driver = Firefox()
# entry_url = 'https://fips.ru/iiss/db.xhtml'
# setup_search_script = "var el=document.getElementById('db-selection-form:j_idt224');" + \
#                 "if (el && el.classList.contains('closed')) el.click();" + \
#                 "setTimeout(()=>{var el=document.getElementById('db-selection-form:dbsGrid9:0:dbsGrid9checkbox');" + \
#                 "if (el && !el.checked) el.click();}, 446);" 
#                 # "setTimeout(()=>document.getElementsByClassName('save')[0].click(), 3000);"
# driver.get(entry_url)
# assert(driver.title == 'Информационно-поисковая система')
# driver.find_element(By.ID, 'db-selection-form:j_idt224').click()
# driver.find_element(By.ID, 'db-selection-form:dbsGrid9:0:dbsGrid9checkbox').click()
# driver.implicitly_wait(1)
# driver.find_element(By.CLASS_NAME, 'save').click()
# driver.implicitly_wait(3)
# search_url = 'https://fips.ru/iiss/search.xhtml'
# print(f'{driver.current_url=}')
# # assert(driver.current_url == 'https://fips.ru/iiss/search.xhtml')
# authors = ['Колбая Камила','Бобровских Алексей']
# found_urls = []
# found_ids = []
# driver.find_element(By.ID, 'fields:5:j_idt122').send_keys(f"'{authors[0]}'")
# driver.implicitly_wait(1)
# driver.find_element(By.CLASS_NAME, 'save').click()
# program_list = driver.find_elements(By.XPATH, '//div[@class="table"]/a')
# ids = extract_ids(program_list)
# print(f'{authors[0]}: {ids=}')

# program_url_prefix = 'https://fips.ru/iiss/document.xhtml?id='

# for id in ids:
#     driver.get(program_url_prefix + id)
