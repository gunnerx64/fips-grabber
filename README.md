# fips-grabber

выгрузка данных о программах для ЭВМ из ФИПС для указанного списка авторов

# установка Firefox gecko driver

A few things to check out.

1. you need to make sure you have install Firefox.
2. Get the latest gecko driver here
3. Set path in your environment

`export PATH=$PATH:/path/to/directory/of/executable/geckodriver<br>`

4. If you intend to skip 3 , you need to amend this in the your script

`from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('C:\Firefox\Firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)`

# Инструкция по использованию в ОС Windows

1. Подготовить список авторов (в формате 'Иванов Иван Иванович') в книге .xlsx. В первой строке столбец с авторами назвать 'ФИО'.
2. Файлы с авторами скопировать в папку input. программа обрабатывает все .xlsx файлы в этой папке.
3. В папке input можно создать 2 файла - blacklist.txt и whitelist.txt - для фильтров по черным и белым спискам правообладателей программы. Фильтр - одна строка в файле для regex. Если правообладатель в белом списке программа индексируется, иначе если правообладатель не в черном списке, программа также индексируется, иначе игнорируется.
4. Запустить программу из 'Run scanner.bat'
5. Выходной файл будет сохранен в корне программы в формате 'Поиск_дата.xlsx'
