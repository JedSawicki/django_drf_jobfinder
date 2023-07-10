from typing import Optional
import time
import random
from requests_html import HTMLSession
import concurrent
from concurrent.futures import wait
from .modules.nofluff_worker import NofluffWorker
from .modules.linkedin_worker import LinkedInWorker
from .modules.jobted_worker import JobtedWorker
from .modules.jooble_worker import JoobleWorker
from .modules.indeed_worker import IndeedWorker


class Scraper:
    def __init__(self):
        self.domain = f'https://pl.linkedin.com/jobs/'
        self.linkedin_items_list = []
    
    def indeed_jobs_worker(self, key1: str, key2: Optional[str] = None, key3: Optional[str] = None) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'http://pl.indeed.com/jobs?q={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'+{key}'
        #print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        try:
            jobs = r.html.find('ul.jobsearch-ResultsList')
            if len(jobs):
                for j in jobs:
                    # a for hrefs
                    items = j.find('div.job_seen_beacon')
                    # elements for text
                    for idx, elem in enumerate(items):
                        (href, ) = j.find('h2')[idx].absolute_links
                        item = {
                                'name': j.find('h2.jobTitle')[idx].text.strip(), 
                                'company_name': j.find('span.companyName')[idx].text.strip(), 
                                'href': href ,
                                'location': j.find('div.companyLocation')[idx].text.strip(),
                                'offer_root': 'Indeed'}
                        urllist.append(item)
                urllist.pop(0) # clear the first unvalid element
            else:
                raise IndexError
        except IndexError:
            print('indeed - No items found')
        #print('indeed len:', len(urllist))  
        return urllist
    
    def grand_scraper(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> object:
        print("Scraping...")
        threads = [LinkedInWorker(), NofluffWorker(), JobtedWorker(), JoobleWorker(), IndeedWorker()]
        results = []
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for idx, t in enumerate(threads):
                futures.append(executor.submit(t, technology, seniority, second_tech))
            wait(futures)
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results += result
        end = time.time()
        print(f'Scrap time: {end -start}')
        random.shuffle(results)
        return results