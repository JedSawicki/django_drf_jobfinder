import logging
import undetected_chromedriver as uc

from selectolax.parser import *
from selenium import webdriver
from typing import Optional, List
from webdriver_manager.chrome import ChromeDriverManager
from .const import Offer
from .common import generic_url_maker


log = logging.getLogger('django')


class IndeedWorker:
    def __init__(self):
        ''' 
        Init fuction
        '''
        
        self.domain = f'http://pl.indeed.com/jobs?q='
        self.indeed_list = []
        
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
        offers = self.parse_indeed_offers(html)
        
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
        
        # THIS WORKS!
        options = webdriver.ChromeOptions() 
        options.headless = True
        options.add_argument("start-maximized")
        driver_exec_path = ChromeDriverManager().install()
        
        with uc.Chrome(options=options, driver_executable_path=driver_exec_path) as driver:
            url = self.domain + technology
            if any(url_dict.keys()):
                url = generic_url_maker(url_dict, url, '+')
            driver.get(url)
            log.info(f'Indeed url: {url}')
            return HTMLParser(driver.page_source)
        
        
    def parse_indeed_offers(self, html: str) -> List:
        ''' 
            Function to find needed text and create Offer dataobject based on required params
        
            Parameters
            ----------
            html : str
                Text from parsed html website
                
            Returns
            ------
            List of dataclass objects Offer
        '''
        offers = html.css('ul')
        
        for item in offers:
            offer_lists_elem = item.css('div.cardOutline')
            for offer_detail in offer_lists_elem:
                offer = Offer(
                    name = offer_detail.css_first('span').text(),
                    href = offer_detail.css_first('a').attrs['href'],
                    offer_root = 'Indeed',
                    company_name = offer_detail.css_first('span.companyName').text(),
                    location = offer_detail.css_first('div.companyLocation').text())
                self.indeed_list.append(offer)
        log.info(f'Indeed_worker items: {len(self.indeed_list)}')

        return self.indeed_list
    