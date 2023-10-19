import asyncio
import time
import random
import concurrent
import logging

from typing import Optional

from concurrent.futures import wait

from .modules.common import filter_offers_results
from .modules.nofluff_worker import NofluffWorker
from .modules.linkedin_worker import LinkedInWorker
from .modules.jobted_worker import JobtedWorker
from .modules.jooble_worker import JoobleWorker
from .modules.indeed_worker import IndeedWorker

log = logging.getLogger('django')


class Scraper:
    def __init__(self):
        ''' 
        Init fuction
        '''
        self.results = []
    
    def grand_scraper(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> object:
        ''' 
        This function is using multihreading in order to execute multiple scraper classes at once. 
        
            Parameters
            ----------
            technology : str
                First argument from POST form
            seniority: str, optional
                Optional second argument from POST form
            second_tech : str, optional
                Optional third argument from POST form
                
            Returns
            ------
            List of collected results from multiple scrapers.
        '''
        threads = [LinkedInWorker(), NofluffWorker(), JobtedWorker(), JoobleWorker(), IndeedWorker()]
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for thread in threads:
                futures.append(executor.submit(thread, technology, seniority, second_tech))
            wait(futures)
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    self.results += result
                except Exception as exc:
                    log.error(exc)
        end = time.time()
        log.info(f'Scrap time: {end - start}')
        self.results = filter_offers_results(technology, seniority, second_tech, offers=self.results)
        
        random.shuffle(self.results)
        return self.results