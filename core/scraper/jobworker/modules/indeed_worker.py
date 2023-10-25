import sys
import logging
import undetected_chromedriver as uc


from selectolax.parser import *
from selenium import webdriver
from typing import Optional, List, Generator
from .const import Offer
from .common import generic_url_maker


log = logging.getLogger('django')


class IndeedWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'http://pl.indeed.com/jobs?q='
        
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
        
        html = self.get_indeed_html_text(technology, seniority, second_tech)
        offers = [offer for offer in self.parse_indeed_offers(html)]
        
        log.info(f'Indeed_worker items: {len(offers)}')
        
        return offers
    
    def get_indeed_html_text(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> str:
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
        try:
            # THIS WORKS!
            options = webdriver.ChromeOptions() 
            options.headless = True
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                                Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
            options.add_argument("start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            with uc.Chrome(options=options, use_subprocess=True) as driver:
                url = self.domain + technology
                if any(url_dict.keys()):
                    url = generic_url_maker(url_dict, url, '+')
                log.info(f'Indeed url: {url}')
                driver.get(url)
                
                return HTMLParser(driver.page_source)

        except Exception as e:
            log.warning('Timeout for indeed chromedriver parsing url: {e}')
        
        
    def parse_indeed_offers(self, html: str) -> Generator[Offer, None, None]:
        ''' 
            Function to find needed text and create Offer dataobject based on required params
        
            Parameters
            ----------
            html : str
                Text from parsed html website
                
            Returns
            ------
            Generator of dataclass objects Offer
        '''
        try:
            offers = html.css('ul')
            for item in offers:
                offer_lists_elem = item.css('div.cardOutline')
                for offer_detail in offer_lists_elem:
                    company_info = offer_detail.css_first('div.company_location')
                    offer = Offer(
                        name = offer_detail.css_first('span').text(),
                        href = offer_detail.css_first('a').attrs['href'],
                        offer_root = 'Indeed',
                        company_name = company_info.css_first('span').text(),
                        location = company_info.css('div')[-1].text())
                    yield offer
        except AttributeError as css_error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log.error(f'AttributeError for {self.domain} Worker: {css_error}, Traceback:{exc_type, exc_tb.tb_lineno}')
    