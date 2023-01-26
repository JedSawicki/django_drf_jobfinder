import httpx
import selectolax.parser

class Scraper:
    def __init__(self):
        self.url = 'https://www.pepper.pl/grupa/elektronika'
        self.client = httpx.Client()

    def get_offers(self):
        response = self.client.get(self.url)
        tree = selectolax.parser.HTMLParser(response.text)
        offers = tree.css('article.thread')
        return offers

    def parse_offers(self):
        results = []
        offers = self.get_offers()
        for offer in offers:
            results.append(offer.text())
        print(results[0])
            
            
sc = Scraper()
sc.get_offers()
sc.parse_offers()