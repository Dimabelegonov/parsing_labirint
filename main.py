import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv

start_time = time.time()
def get_data():
    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
            "Название книги",
            "Автор",
            "Издательство",
            "Цена со скидкой",
            "Цена без скидки",
            "Процент скидки",
            "Наличие на складе"
            )
        )

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36"
    }

    url = "https://www.labirint.ru/genres/2308/?available=1&wait=1&preorder=1&no=1&display=table"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers__right").find_all("a")[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):

        url = f"https://www.labirint.ru/genres/2308/?available=1&wait=1&preorder=1&no=1&display=table&page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for book_item in books_items:
            book_data = book_item.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except Exception:
                book_title = "Нет названия"

            try:
                book_author = book_data[1].text.strip()
                if len(book_author) == 0:
                    book_author = "Нет автора"
            except Exception:
                book_author = "Нет автора"

            try:
                # book_publishing = book_data[2].text.strip()
                book_publishing = ": ".join([item.text.strip() for item in book_data[2].find_all("a")])
            except Exception:
                book_publishing = "Нет издательства"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span", class_="price-val").\
                    find("span").text.strip().replace(" ", ""))
            except Exception:
                book_new_price = "Нет цены со скидкой"

            try:
                book_old_price = int(book_data[3].find("div", class_="price").find("span", class_="price-old").\
                    find("span").text.strip().replace(" ", ""))
            except Exception:
                book_old_price = "Нет цены без скидки"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except Exception:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
            except Exception:
                book_status = "Нет статуса"

            # print(book_title)
            # print(book_author)
            # print(book_publishing)
            # print(book_new_price)
            # print(book_old_price)
            # print(book_sale)
            # print(book_status)
            # print("#" * 20)

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )
        print(f"Обработана {page}/{pages_count}")
        time.sleep(2)
    with open(f"labirint_{cur_time}.json", "w") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное время на работу скрипта: {finish_time}")


if __name__ == '__main__':
    main()
