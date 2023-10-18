import httpx
import asyncio
import logging

from selectolax.parser import *
from typing import Generator, Optional, List
from .const import Offer
from .common import generic_url_maker


log = logging.getLogger('django')


class JobtedWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'https://www.jobted.pl/?j='
        self.jobted_list = []
    
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
        
        html = self.get_jobted_html_text(technology, seniority, second_tech)
        offers = [offer for offer in self.parse_jobted_offers(html)]
        log.info(f'Jobted_worker items: {len(offers)}')
        
        return offers
         
    def get_jobted_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> str:
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
        log.info(f'keywords: {technology}, {seniority}, {second_tech}')
        url_dict = {
            'seniority': seniority,
            'second_tech': second_tech
        }
        
        with httpx.Client() as client:
            url = self.domain + technology
            if any(url_dict.keys()):
                url = generic_url_maker(url_dict, url)

            r = client.get(url, follow_redirects=True)
            log.info(f'Jobted url: {url}')
            
            return HTMLParser(r.text)


    def parse_jobted_offers(self, html: str) -> Generator[Offer, None, None]:
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
            offers = html.css('div.res-item-info')
            for item in offers:
                offer = Offer(
                    name = item.css_first('span.res-data-title').text(),
                    href = item.css_first('a').attrs['href'],
                    offer_root = 'Jobted',
                    company_name = item.css_first('span.res-data-company').text() if item.css_first('span.res-data-company') is not None else '',
                    location = item.css_first('span.res-data-location').text())
                yield offer
        except AttributeError as css_error:
            log.error(f'AttributeError for {self.domain} Worker: {css_error}')
