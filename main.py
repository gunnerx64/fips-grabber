from fips_spider import FipsSpider
from datetime import datetime

def main():
    # tmp_authors = ['Попов Петр','Бобровских Алексей','Нечаев Сергей']
    tmp_authors = ['Попов Петр']

    fips = FipsSpider()
    fips.fetch(tmp_authors)
    now = datetime.now()
    fips.write_output(f'Поиск_{now.year}-{now.month}-{now.day}')


main()