from typing import Optional
from urllib.parse import quote

from ..base_store import BaseStore
from ..models import ProductOffer
from ..utils import parse_brl, score_match, absolute_url


class MercadoLivreStore(BaseStore):
    store_name = "Mercado Livre"
    base_url = "https://lista.mercadolivre.com.br"

    def search(self, query: str) -> Optional[ProductOffer]:
        url = f"{self.base_url}/{quote(query.replace(' ', '-'))}"
        soup = self.get_soup(url)

        cards = soup.select("li.ui-search-layout__item")
        if not cards:
            return None

        best = None
        best_score = -1

        for card in cards[:10]:
            title_el = card.select_one("h3")
            link_el = card.select_one("a[href]")
            price_fraction = card.select_one(".andes-money-amount__fraction")

            if not title_el or not link_el or not price_fraction:
                continue

            title = title_el.get_text(" ", strip=True)
            href = link_el.get("href", "").strip()
            full_price_text = price_fraction.get_text(" ", strip=True)

            price = parse_brl(full_price_text)
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