import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(base_url):
    url = base_url
    quotes_data = []

    while url:
        try:
            response = requests.get(url)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, 'html.parser')

            for quote in soup.find_all('div', class_='quote'):
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                tags = [tag.text for tag in quote.find_all('a', class_='tag')]

                quotes_data.append({
                    'author': author,
                    'tags': tags,
                    'quote': text
                })

            next_page = soup.find('li', class_='next')
            url = base_url + next_page.find('a')['href'] if next_page else None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break  

    with open('quotes.json', 'w') as f:
        json.dump(quotes_data, f, indent=4)

    return quotes_data 

def scrape_authors(quotes_data):
    authors_data = {}

    for quote in quotes_data:
        author = quote['author']
        if author not in authors_data:
            authors_data[author] = {
                'fullname': author,
                'born_date': "",  
                'born_location': "",
                'description': ""
            }

    with open('authors.json', 'w') as f:
        json.dump(list(authors_data.values()), f, indent=4)

if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com"
    quotes_data = scrape_quotes(base_url)
    scrape_authors(quotes_data)
