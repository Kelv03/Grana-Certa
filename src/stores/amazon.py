from typing import Optional
from urllib.parse import quote_plus

from ..base_store import BaseStore
from ..models import ProductOffer
from ..utils import parse_brl, score_match, absolute_url


class AmazonStore(BaseStore):
    store_name = "Amazon Brasil"
    base_url = "https://www.amazon.com.br"

    def search(self, query: str) -> Optional[ProductOffer]:
        url = f"{self.base_url}/s?k={quote_plus(query)}"
        soup = self.get_soup(url)

        cards = soup.select("div.s-result-item[data-component-type='s-search-result']")
        if not cards:
            return None

        best = None
        best_score = -1

        for card in cards[:10]:
            title_el = card.select_one("h2 span")
            link_el = card.select_one("h2 a")
            whole_el = card.select_one(".a-price-whole")
            frac_el = card.select_one(".a-price-fraction")

            if not title_el or not link_el or not whole_el:
                continue

            title = title_el.get_text(" ", strip=True)
            href = link_el.get("href", "").strip()

            price_text = whole_el.get_text(strip=True)
            if frac_el:
                price_text += "," + frac_el.get_text(strip=True)

            price = parse_brl(price_text)
            if price is None:
                continue

            current_score = score_match(query, title)
            if current_score > best_score:
                best_score = current_score
                best = ProductOffer(
                    store=self.store_name,
                    title=title,
                    cash_price=price,
                    card_price=price,
                    url=absolute_url(self.base_url, href),
                    availability="disponível"
                )

        return best