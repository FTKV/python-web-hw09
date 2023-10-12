import json

from bs4 import BeautifulSoup
import requests


URL = "https://quotes.toscrape.com/"


if __name__ == "__main__":
    author_info_urls = set()
    authors = []
    quotes = []
    response = requests.get(URL)
    while response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        nav_next = soup.find("nav").find("li", class_="next")
        quote_data = soup.find_all("div", class_="quote")
        for quote_data_el in quote_data:
            quote = quote_data_el.find("span", class_="text").text.strip()
            author = quote_data_el.find("small", class_="author").text.strip()
            tags_data = quote_data_el.find("div", class_="tags")
            tags_data = tags_data.find_all("a", class_="tag")
            tags = []
            for tag in tags_data:
                tags.append(tag.text.strip())
            quotes.append({"tags": tags, "author": author, "quote": quote})
            author_info_url = quote_data_el.find("a")["href"]
            if author_info_url not in author_info_urls:
                author_info_urls.add(author_info_url)
                author_data = requests.get(f"{URL}{author_info_url}")
                soup = BeautifulSoup(author_data.text, "lxml")
                fullname = soup.find("h3", class_="author-title").text.strip()
                born_date = soup.find("span", class_="author-born-date").text.strip()
                born_location = soup.find(
                    "span", class_="author-born-location"
                ).text.strip()
                description = soup.find("div", class_="author-description").text.strip()
                authors.append(
                    {
                        "fullname": fullname,
                        "born_date": born_date,
                        "born_location": born_location,
                        "description": description,
                    }
                )
        if nav_next:
            next_page_url = nav_next.find("a")["href"]
            response = requests.get(f"{URL}{next_page_url}")
        else:
            break

    with open("first/json/authors.json", "w", encoding="utf-8") as fh:
        json.dump(authors, fh, ensure_ascii=False, indent=4)

    with open("first/json/quotes.json", "w", encoding="utf-8") as fh:
        json.dump(quotes, fh, ensure_ascii=False, indent=4)

    print("Done")
