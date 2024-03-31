# fips-grabber
выгрузка данных о программах для ЭВМ из ФИПС для указанного списка авторов

# установка Firefox gecko driver

A few things to check out.

1) you need to make sure you have install Firefox.
2) Get the latest gecko driver here
3) Set path in your environment

`export PATH=$PATH:/path/to/directory/of/executable/geckodriver<br>`

4) If you intend to skip 3 , you need to amend this in the your script

`from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('C:\Firefox\Firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)`


