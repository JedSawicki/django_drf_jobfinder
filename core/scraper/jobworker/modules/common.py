

def generic_url_maker(url_dict: dict, url: str) -> str:
    ''' 
    Function prepare url with given dictionary containing additional keywords.
    
        Parameters
        ----------
        url_dict : dict
            Dictionary of additional keywords
        url : str
            Unprepared URL
            
        Returns
        ------
        Prepared URL
    '''
    add_keywords = [f'%20{keyword}' for keyword in url_dict.values() if keyword is not None]
    url += ''.join([item for item in add_keywords])
    
    return url