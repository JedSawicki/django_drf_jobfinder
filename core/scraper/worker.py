from typing import Optional
import time
import random
from requests_html import HTMLSession
import concurrent
from concurrent.futures import wait
import re


class Scraper:
    def __init__(self):
        self.domain = f'https://pl.linkedin.com/jobs/'
        self.linkedin_items_list = []

    def linkedin_worker(self, key1: str, key2: Optional[str] = None, key3: Optional[str] = None) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.linkedin.com/jobs/search?keywords={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []
        print(r.status_code)
        try:
            jobs = r.html.find('ul.jobs-search__results-list')
            for j in jobs:
                items = j.find('li')
                for idx, elem in enumerate(items):
                    if len(items):
                        (href, ) = j.find('a')[idx].absolute_links
                        item = {'name': j.find('h3.base-search-card__title')[idx].text.strip(), 
                                'company_name': j.find('h4.base-search-card__subtitle')[idx].text.strip(), 
                                'href': href, 
                                'location': j.find('span.job-search-card__location')[idx].text.strip(),
                                'offer_root': 'LinkedIn'}
                        urllist.append(item)
                    else:
                        raise IndexError
        except IndexError:
            print('LinkedInWorker - No items found')
        print('linkedin len:', len(urllist))  
        return urllist

    def no_fluff_jobs_worker(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None, page: Optional[int] = 1) -> object:
        # url = f'https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Djunior&page=2'
        url = f'https://nofluffjobs.com/pl/praca-it/{technology}?page={page}'
        if seniority is not None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?criteria=seniority%3D{seniority}&page={page}'
        if second_tech is not None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?criteria=seniority%3D{seniority}%20%20keyword%3D{second_tech}&page={page}'
        if second_tech is not None and seniority is None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?page={page}&criteria=requirement%3D{second_tech}'
                    
        print(url)
        s = HTMLSession()
        r = s.get(str(url))
        urllist = []
        try:
            jobs = r.html.find('div.list-container.ng-star-inserted')

            for j in jobs:
                # a for hrefs
                items = j.find('a')
                if len(items):
                # elements for text
                    for idx, elem in enumerate(items):
                        text = elem.text.split('\n')       
                        if idx % 2 == 0:
                            href = 'https://nofluffjobs.com' + elem.attrs['href']
                            item = {
                                        'href': href, 
                                        'offer_root': 'NoFluffJobs'
                                        }
                            if len(text) > 1:
                                item['name'] = text[0]
                                item['company_name'] = text[1]
                            else:
                                item['name'] = text[0]
                            urllist.append(item)
                else:
                    raise IndexError
        except IndexError:
            print('NofluffWorker - No items found')
        print('nofluff len:', len(urllist))  
        return urllist
    
    def indeed_jobs_worker(self, key1: str, key2: Optional[str] = None, key3: Optional[str] = None) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.indeed.com/jobs?q={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
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
            else:
                raise IndexError
        except IndexError:
            print('indeed - No items found')
        print('indeed len:', len(urllist))  
        return urllist

    def jooble_jobs_worker(self, key1: str, key2: Optional[str] = None, key3: Optional[str] = None) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.jooble.org/SearchResult?ukw={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        try:
            jobs = r.html.find('div.infinite-scroll-component')
            for j in jobs:
                # a for hrefs
                items = j.find('article')
                if len(items):
                    # elements for text
                    for idx, elem in enumerate(items):
                        text = j.find('p')[idx].text.strip()
                        # st = re.findall(r'^.*zł.*$', text)
                        # salary = ''
                        # if len(st):
                        #     st = salary
                        (href, ) = j.find('a')[idx].absolute_links
                        item = { 'href': href, 
                                'name': j.find('a')[idx].text.strip(),
                                'company_name': j.find('p.Ya0gV9')[idx].text.strip(),
                                'location': j.find('div.caption')[idx].text.strip(), 
                                'offer_root': 'Jooble'
                        }
                        urllist.append(item)
                else:
                    raise IndexError
        except IndexError:
            print('jooble - No items found')
        print('jooble len:', len(urllist))    
        return urllist
    
    def jobted_jobs_worker(self, key1: str, key2: Optional[str] = None, key3: Optional[str] = None) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://www.jobted.pl/?j={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        try:
            jobs = r.html.find('div.res-list')
            for j in jobs:
                # a for hrefs
                items = j.find('div.res-item-info')
                if len(items):
                    # elements for text
                    for idx, elem in enumerate(items):
                        (href, ) = j.find('a.res-link-job')[idx].absolute_links
                        item = { 
                                'name': j.find('span.res-data-title')[idx].text.strip(),
                                'location': j.find('span.res-data-location')[idx].text.strip(),
                                'company': j.find('span.res-data-company')[idx].text.strip(),
                                'href': href,
                                'offer_root': 'Jobted'
                        }
                        urllist.append(item)
                else:
                    raise IndexError
        except IndexError:
            print('jobted - Item not found')
        print('jobted len:', len(urllist))   
        return urllist
    
    def grand_scraper(self, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None) -> object:
        print("Scraping...")
        threads = [self.linkedin_worker, self.no_fluff_jobs_worker, self.jobted_jobs_worker, self.indeed_jobs_worker, self.jooble_jobs_worker]
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
        
        # print(results)
        print(f'Scrap time: {end -start}')
        random.shuffle(results)
        return results