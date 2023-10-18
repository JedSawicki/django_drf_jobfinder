import httpx
import logging
from typing import Generator

from selectolax.parser import *
from typing import Optional, List
from .const import Offer

log = logging.getLogger('django')

class NofluffWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = 'https://nofluffjobs.com/'
        
    def __call__(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None, page: int = 1) -> List:
        ''' 
        Function defined in order to excecute Class methods while calling the Class:'NofluffWorker' object, 
        returning list of dictionaries by calling self.parse_nofluff_offers().
        
            Parameters
            ----------
            technology : str
                Required text tag for url
            seniority: str, optional
                Optional text tag for url
            second_tech : str, optional
                Optional text tag for url
            page : int
                Required tag for url page number
                
            Returns
            ------
            List of dataclass objects Offer containing job offers from given URL
        '''
        
        html = self.get_nofluff_html_text(technology, seniority, second_tech, page)
        offers = [offer for offer in self.parse_nofluff_offers(html)]
                 
        log.info(f'Nofluff_worker items: {len(offers)}')
        
        return offers
         
    def get_nofluff_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None, page: int = 1) -> str:
        ''' 
        Function to open httpx library client, prepare URL of nofluffjobs and return text of that website.
        
            Parameters
            ----------
            technology : str
                Required text tag for url
            page : int
                Required tag for url page number
            seniority: str, optional
                Optional text tag for url
            second_tech : str, optional
                Optional text tag for url
                
            Returns
            ------
            Text from parsed url website using selectolax HTMLParser
        '''
        url_dict = {
            'seniority': seniority,
            'second_tech': second_tech
        }
        
        with httpx.Client() as client:
            url = self.domain + f'pl/praca-it/{technology}?page={page}' 
            if any(url_dict.values()):
                url = self.domain + f'{technology}?criteria=keyword%3D{seniority}&page=1'
                url = self.domain +  f'pl/{technology}?criteria=requirement%3D{second_tech}%20' \
                f'seniority%3D{seniority}&page={page}' if all(url_dict.values()) else url

            r = client.get(url, follow_redirects=True)
            log.info(f'Nofluff url: {url}')
        
            return HTMLParser(r.text)

    def parse_nofluff_offers(self, html: str) -> Generator[Offer, None, None]:
        ''' 
        Function to find needed text and create Offer dataobject based on required 
        
            Parameters
            ----------
            html : str
                Text from parsed html website
                
            Returns
            ------
            Generator of dataclass objects Offer
        '''
        try:
            offers = html.css('a.posting-list-item')
            for item in offers:
                offer = Offer(
                    name = item.css_first('h3.posting-title__position').text(), 
                    href = 'https://nofluffjobs.com' + item.css_first('a').attrs['href'],
                    offer_root = 'NoFluff',
                    company_name = item.css_first('span.d-block').text(),
                    location = item.css_first('span.tw-text-ellipsis').text())
                yield offer
        except AttributeError as css_error:
            log.error(f'AttributeError for {self.domain} Worker: {css_error}')
