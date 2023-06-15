import httpx
import asyncio
import logging

from selectolax.parser import *
from typing import Optional, List
from .const import Offer

log = logging.getLogger('django')


class LinkedInWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'https://pl.linkedin.com/jobs/'
        self.linkedin_list = []
    
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
        
        html = self.get_linkedin_html_text(technology, seniority, second_tech)
        offers = self.parse_linkedin_offers(html)
        
        return offers
         
    def get_linkedin_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> str:
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
                url = self.domain + f'search?keywords={technology}'
                url_generator = (url + f'%20{key}' for key in url_dict.values() if key is not None)
                *_, url = url_generator

            r = client.get(url, follow_redirects=True)
            log.info(f'Linkedin url: {url}')
            
        return HTMLParser(r.text)


    def parse_linkedin_offers(self, html: str) -> List:
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
        offers = html.css('ul.jobs-search__results-list')
        
        for item in offers:
            offer_lists_elem = item.css('li')
            for offer_detail in offer_lists_elem:
                offer = Offer(
                    name = offer_detail.css_first('h3.base-search-card__title').text(),
                    href = offer_detail.css_first('a').attrs['href'],
                    offer_root = 'LinkedIn',
                    company_name = offer_detail.css_first('h4.base-search-card__subtitle').text(),
                    location = offer_detail.css_first('span.job-search-card__location').text())
                self.linkedin_list.append(offer)
        log.info(f'Linkedin_worker items: {len(self.linkedin_list)}')

        return self.linkedin_list
            
