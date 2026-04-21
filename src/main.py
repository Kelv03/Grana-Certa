from .stores import MercadoLivreStore, AmazonStore, MagaluStore
from .ranking import (
    cheapest_cash_offer,
    cheapest_card_offer,
    sort_by_cash_price,
    sort_by_card_price,
)
from .models import ProductOffer


def format_price(value: float | None) -> str:
    if value is None:
        return "não encontrado"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def print_offer(offer: ProductOffer) -> None:
    print(f"\nLoja: {offer.store}")
    print(f"Produto encontrado: {offer.title}")
    print(f"Preço à vista: {format_price(offer.cash_price)}")
    print(f"Preço no cartão: {format_price(offer.card_price)}")
    print(f"Link: {offer.url}")


def main() -> None:
    print("=" * 60)
    print("GRANA CERTA COMPARADOR")
    print("=" * 60)

    query = input("Digite o nome do produto: ").strip()
    if not query:
        print("Você precisa informar um produto.")
        return

    stores = [
        MercadoLivreStore(),
        AmazonStore(),
        MagaluStore(),
    ]

    offers: list[ProductOffer] = []

    print("\nPesquisando nas lojas...\n")

    for store in stores:
        try:
            result = store.search(query)
            if result:
                offers.append(result)
                print(f"[OK] {store.store_name}")
            else:
                print(f"[SEM RESULTADO] {store.store_name}")
        except Exception as exc:
            print(f"[ERRO] {store.store_name}: {exc}")

    if not offers:
        print("\nNenhuma oferta encontrada.")
        return

    print("\n" + "=" * 60)
    print("OFERTAS ENCONTRADAS")
    print("=" * 60)

    for offer in offers:
        print_offer(offer)

    print("\n" + "=" * 60)
    print("RANKING À VISTA")
    print("=" * 60)

    for idx, offer in enumerate(sort_by_cash_price(offers), start=1):
        print(f"{idx}. {offer.store} — {format_price(offer.cash_price)}")

    print("\n" + "=" * 60)
    print("RANKING NO CARTÃO")
    print("=" * 60)

    for idx, offer in enumerate(sort_by_card_price(offers), start=1):
        print(f"{idx}. {offer.store} — {format_price(offer.card_price)}")

    best_cash = cheapest_cash_offer(offers)
    best_card = cheapest_card_offer(offers)

    print("\n" + "=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)

    if best_cash:
        print(
            f"Mais barato à vista: {best_cash.store} — {format_price(best_cash.cash_price)}"
        )
    else:
        print("Mais barato à vista: não encontrado")

    if best_card:
        print(
            f"Mais barato no cartão: {best_card.store} — {format_price(best_card.card_price)}"
        )
    else:
        print("Mais barato no cartão: não encontrado")

    other_stores = [offer.store for offer in offers]
    print("Outras lojas encontradas:", ", ".join(other_stores))


if __name__ == "__main__":
    main()