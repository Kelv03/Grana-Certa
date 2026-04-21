from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductOffer:
    store: str
    title: str
    cash_price: Optional[float]
    card_price: Optional[float]
    url: str
    availability: str = "desconhecida"

    def best_known_price(self) -> Optional[float]:
        prices = [p for p in [self.cash_price, self.card_price] if p is not None]
        return min(prices) if prices else None