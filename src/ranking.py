from typing import List, Optional
from .models import ProductOffer


def sort_by_cash_price(offers: List[ProductOffer]) -> List[ProductOffer]:
    return sorted(
        offers,
        key=lambda x: float("inf") if x.cash_price is None else x.cash_price
    )


def sort_by_card_price(offers: List[ProductOffer]) -> List[ProductOffer]:
    return sorted(
        offers,
        key=lambda x: float("inf") if x.card_price is None else x.card_price
    )


def cheapest_cash_offer(offers: List[ProductOffer]) -> Optional[ProductOffer]:
    valid = [o for o in offers if o.cash_price is not None]
    return min(valid, key=lambda x: x.cash_price) if valid else None


def cheapest_card_offer(offers: List[ProductOffer]) -> Optional[ProductOffer]:
    valid = [o for o in offers if o.card_price is not None]
    return min(valid, key=lambda x: x.card_price) if valid else None