import httpx
import logging
from typing import Generator

from selectolax.parser import *
from typing import Optional, List
from .const import Offer
from .common import generic_url_maker

log = logging.getLogger('django')


class JoobleWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'https://pl.jooble.org/SearchResult?ukw='
        
    def __call__(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> List:
        ''' 
        Function defined in order to excecute Class methods while calling the Class:'NofluffWorker' object, 
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
        
        html = self.get_jooble_html_text(technology, seniority, second_tech)
        
        offers = [offer for offer in self.parse_jooble_offers(html)]
        log.info(f'Jooble_worker items: {len(offers)}')
        
        return offers
         
    def get_jooble_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> str:
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
            url = self.domain + f'search?keywords={technology}'
            if any(url_dict.keys()):
                url = generic_url_maker(url_dict, url)

            r = client.get(url, follow_redirects=True)
            log.info(f'Jooble url: {url}')
            
            return HTMLParser(r.text)


    def parse_jooble_offers(self, html: str) -> Generator[Offer, None, None]:
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
            offers = html.css('div.infinite-scroll-component')
            for item in offers:
                offer_lists_elem = item.css('article')
                for offer_detail in offer_lists_elem:
                    offer = Offer(
                        name = offer_detail.css_first('a').text(),
                        href = offer_detail.css_first('a').attrs['href'],
                        offer_root = 'Jooble',
                        company_name = ' '.join([text.text() for text in offer_detail.css('p')]),
                        location = offer_detail.css_first('div.caption').text())
                    yield offer
        except AttributeError as css_error:
            log.error(f'AttributeError for {self.domain} Worker: {css_error}')
            
        


            
