

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