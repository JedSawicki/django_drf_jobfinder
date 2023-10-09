from dataclasses import dataclass
from typing import Optional

@dataclass
class Offer:
    name: Optional[str]
    href: Optional[str]
    offer_root: Optional[str]
    company_name: Optional[str]
    location: Optional[str]