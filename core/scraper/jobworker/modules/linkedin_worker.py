import httpx
import logging
from typing import Generator

from selectolax.parser import *
from typing import Optional, List
from .const import Offer
from .common import generic_url_maker

log = logging.getLogger('django')


class LinkedInWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'https://pl.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/'
        self.linkedin_list = []
    
    def __call__(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None, page: int = 200) -> List:
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
        
        # html = self.get_linkedin_html_text(technology, seniority, second_tech, page)
        # offers = [offer for offer in self.parse_linkedin_offers(html)]
        
        for page in range(0, page, 25):
            html = self.get_linkedin_html_text(technology, seniority, second_tech, page)
            if html:
                self.linkedin_list += [offer for offer in self.parse_linkedin_offers(html)]
                 
        log.info(f'Linkedin_worker items: {len(self.linkedin_list)}')
        
        return self.linkedin_list
         
    def get_linkedin_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None, page: int = 0) -> str:
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
        new_url = 'https://pl.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=junior%2Bpython%2Bdeveloper&position=1&pageNum=0&start=200'
        old_url = 'https://pl.linkedin.com/jobs/search?keywords=junior%20python%20developer'
        
        with httpx.Client() as client:
            url = self.domain + f'search?keywords={technology}'
            if any(url_dict.values()):
                url = generic_url_maker(url_dict, url, '%2b')
            
            url += f'&position=1&pageNum=0&start={page}'
            r = client.get(url, follow_redirects=True)
            log.info(f'Linkedin url: {url}')
            
            return HTMLParser(r.text)


    def parse_linkedin_offers(self, html: str) -> Generator[Offer, None, None]:
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
            offers = html.css('li')
            for item in offers:    
                offer = Offer(
                    name = item.css_first('h3.base-search-card__title').text(),
                    href = item.css_first('a').attrs['href'],
                    offer_root = 'LinkedIn',
                    company_name = item.css_first('h4.base-search-card__subtitle').text(),
                    location = item.css_first('span.job-search-card__location').text())
                yield offer
        except AttributeError as css_error:
            log.error(f'AttributeError for {self.domain} Worker: {css_error}')
        
            
