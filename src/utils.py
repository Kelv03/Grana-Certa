import re
import unicodedata
from typing import Optional
from urllib.parse import urljoin


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().split())


def parse_brl(value: str) -> Optional[float]:
    if not value:
        return None

    value = value.replace("\xa0", " ")
    match = re.search(r"R\$\s*([\d\.\,]+)", value)
    if not match:
        match = re.search(r"([\d\.\,]+)", value)

    if not match:
        return None

    number = match.group(1).replace(".", "").replace(",", ".")
    try:
        return float(number)
    except ValueError:
        return None


def extract_prices_from_text(text: str) -> tuple[Optional[float], Optional[float]]:
    """
    Tenta capturar:
    - preço à vista / pix / boleto
    - preço no cartão / parcelado / preço padrão

    Se não achar preço à vista separado, usa o primeiro preço como preço no cartão.
    """
    clean = " ".join(text.split())

    cash_patterns = [
        r"(?:à vista|no pix|pix|boleto)[^\dR$]{0,20}(R\$\s*[\d\.\,]+)",
        r"(R\$\s*[\d\.\,]+)[^\n]{0,20}(?:à vista|no pix|pix|boleto)",
    ]

    card_patterns = [
        r"(?:no cartão|cartão|em até \d+x)[^\dR$]{0,20}(R\$\s*[\d\.\,]+)",
        r"(R\$\s*[\d\.\,]+)[^\n]{0,20}(?:no cartão|cartão|em até \d+x)",
    ]

    cash_price = None
    card_price = None

    for pattern in cash_patterns:
        match = re.search(pattern, clean, re.IGNORECASE)
        if match:
            cash_price = parse_brl(match.group(1))
            break

    for pattern in card_patterns:
        match = re.search(pattern, clean, re.IGNORECASE)
        if match:
            card_price = parse_brl(match.group(1))
            break

    all_prices = re.findall(r"R\$\s*[\d\.\,]+", clean)
    parsed_prices = [parse_brl(p) for p in all_prices]
    parsed_prices = [p for p in parsed_prices if p is not None]

    if not card_price and parsed_prices:
        card_price = parsed_prices[0]

    if not cash_price and parsed_prices:
        if len(parsed_prices) >= 2:
            cash_price = min(parsed_prices[:2])
        else:
            cash_price = parsed_prices[0]

    return cash_price, card_price


def score_match(query: str, title: str) -> int:
    q_tokens = set(normalize_text(query).split())
    t_tokens = set(normalize_text(title).split())
    return len(q_tokens.intersection(t_tokens))


def absolute_url(base: str, href: str) -> str:
    return urljoin(base, href)