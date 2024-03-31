from fips_spider import FipsSpider

def main():
    tmp_authors = ['Попов Петр','Бобровских Алексей','Нечаев Сергей','Тарасов Александр','Титов Дмитрий']

    fips = FipsSpider()
    fips.fetch(tmp_authors)



main()