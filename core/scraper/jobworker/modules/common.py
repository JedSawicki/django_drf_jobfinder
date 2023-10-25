import logging
from .const import Offer

log = logging.getLogger('django')

def generic_url_maker(url_dict: dict, url: str, separator: str = '%20') -> str:
    ''' 
    Function prepare url with given dictionary containing additional keywords.
    
        Parameters
        ----------
        url_dict : dict
            Dictionary of additional keywords
        url : str
            Unprepared URL
        separator: str
            string used for separating keywords
            
        Returns
        ------
        Prepared URL
    '''
    add_keywords = [f'{separator}{keyword}' for keyword in url_dict.values() if keyword is not None]
    url += ''.join([item for item in add_keywords])
    
    return url


def filter_offers_results(*keywords: str, offers: list[Offer, None, None]) -> list[Offer, None, None]:
    ''' 
    Function to filter dataclass objects Offer by name.
    
        Parameters
        ----------
        offers : list[Offer, None, None]
            List of dataclass objects Offer
            
        Returns
        ------
        List of dataclass objects Offer filtered by name(at least 2 keywords must be present)
    '''
    keywords_list = set([keyword.upper() for keyword in keywords if keyword is not None])
    filtered_offers = []

    for offer in offers:
        strings = set([char for char in offer.name.upper().split() if char is not None])
        common_keywords = strings.intersection(keywords_list)   
        if len(common_keywords) > 1 or len(keywords_list) == 1:
            filtered_offers.append(offer)
    
    return filtered_offers