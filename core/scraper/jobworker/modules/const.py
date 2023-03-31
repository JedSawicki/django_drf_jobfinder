from dataclasses import dataclass

@dataclass
class Offer:
    name: str
    href: str
    offer_root: str
    company_name: str
    location: str