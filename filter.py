import re

def get_data_from_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []
    
class Filter:
    __blacklist = get_data_from_file('input/blacklist.txt')
    __blacklist = [re.compile(key.strip(), flags=re.IGNORECASE) for key in __blacklist]
    __whitelist = get_data_from_file('input/whitelist.txt')
    __whitelist = [re.compile(key.strip(), flags=re.IGNORECASE) for key in __whitelist]
    
    # def __init__(self):
    #     self.__blacklist = get_data_from_file('input/blacklist.txt')
    #     self.__blacklist = [re.compile(key, flags=re.IGNORECASE) for key in self.__blacklist]
    #     self.__whitelist = get_data_from_file('input/whitelist.txt')
    #     self.__whitelist = [re.compile(key, flags=re.IGNORECASE) for key in self.__blacklist]
    
    @staticmethod
    def is_blacklisted(input: str | None) -> bool:
        if input is None:
            return False
        for key in Filter.__blacklist:
            if re.search(key, input.lower()):
                return True
        return False
    
    @staticmethod
    def is_whitelisted(input: str | None) -> bool:
        if input is None:
            return False
        for key in Filter.__whitelist:
            if re.search(key, input.lower()):
                return True
        return False

