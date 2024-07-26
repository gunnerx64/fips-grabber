import re

class Program:
    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('<.*?>')  # удаляет тэги и содержимое
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