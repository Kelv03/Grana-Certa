from typing import Optional
from urllib.parse import quote

from ..base_store import BaseStore
from ..models import ProductOffer
from ..utils import extract_prices_from_text, score_match, absolute_url


class MagaluStore(BaseStore):
    store_name = "Magazine Luiza"
    base_url = "https://www.magazineluiza.com.br"

    def search(self, query: str) -> Optional[ProductOffer]:
        slug = quote(query.replace(" ", "-"))
        url = f"{self.base_url}/busca/{slug}/"
        soup = self.get_soup(url)

        cards = soup.select("li[data-testid='product-card']") or soup.select("div[data-testid='product-card']")
        if not cards:
            return None

        best = None
        best_score = -1

        for card in cards[:10]:
            title_el = (
                card.select_one("h2")
                or card.select_one("p[data-testid='product-title']")
                or card.select_one("a[title]")
            )
            link_el = card.select_one("a[href]")

            if not title_el or not link_el:
                continue

            title = title_el.get_text(" ", strip=True)
            href = link_el.get("href", "").strip()
            card_text = card.get_text(" ", strip=True)

            cash_price, card_price = extract_prices_from_text(card_text)

            if cash_price is None and card_price is None:
                continue

            current_score = score_match(query, title)
            if current_score > best_score:
                best_score = current_score
                best = ProductOffer(
                    store=self.store_name,
                    title=title,
                    cash_price=cash_price,
                    card_price=card_price,
                    url=absolute_url(self.base_url, href),
                    availability="disponível"
                )

        return best