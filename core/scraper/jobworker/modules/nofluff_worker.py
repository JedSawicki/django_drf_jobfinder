import httpx
import asyncio

from selectolax.parser import *
from typing import Optional, List
from .const import Offer


class NofluffWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = 'https://nofluffjobs.com'
        self.nofluff_list = []
    
    def __call__(self, technology: str, page: int = 1, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> List:
        ''' 
        Function defined in order to excecute Class methods while calling the Class object, 
        returning list of dictionaries by calling self.parse_nofluff_offers().
        
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
            List of dataclass objects Offer containing job offers from given URL
        '''
        
        html = self.get_nofluff_html(technology, page, seniority, second_tech)
        offers = self.parse_nofluff_offers(html)
        
        return offers
         
    def get_nofluff_html(self, technology: str, page: int = 1, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> str:
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
            if technology:
                url = f'https://nofluffjobs.com/pl/praca-it/{technology}?page={page}'
                if None not in url_dict.values():
                    url = f'https://nofluffjobs.com/pl/{technology}?criteria=keyword%3D{second_tech}%20seniority%3D{seniority}&page={page}'
                else:   
                    for key, value in url_dict.items():
                        if value is not None:
                            url = f'https://nofluffjobs.com/pl/Python?criteria=keyword%3D{value}&page=1'

            r = client.get(url, follow_redirects=True)
            
        return HTMLParser(r.text)

    def parse_nofluff_offers(self, html: str) -> List:
        ''' 
        Function to find needed text and create Offer dataobject based on required 
        
            Parameters
            ----------
            html : str
                Text from parsed html website
                
            Returns
            ------
            List of dataclass objects Offer
        '''
        offers = html.css('a.posting-list-item')

        for item in offers:
            offer = Offer(
                name = item.css_first('h3.posting-title__position').text(), 
                href = self.domain + item.css_first('a').attrs['href'],
                offer_root = 'NoFluff',
                company_name = item.css_first('span.d-block').text(),
                location = item.css_first('span.tw-text-ellipsis').text())
            self.nofluff_list.append(offer)
            
        return self.nofluff_list
