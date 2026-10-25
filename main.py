
if __name__ == "__main__":
    from AccionInversion import Accion
    from Portafolio import Portafolio

    print("\n" + "=" * 60)
    print("PRUEBA")
    print("=" * 60)

    a1 = Accion(precio_actual=150.0, ticker="AAPL", cantidad=10)
    a2 = Accion(precio_actual=400.0, ticker="NVDA", cantidad=5)

    portafolio = Portafolio("Bruno")
    portafolio = portafolio + a1
    portafolio = portafolio + a2

    print(
        f"Ticker 'AAPL' válido: {Portafolio.es_ticker_valido('AAPL')}"
    )  # True
    print(f"Acciones distintas en el portafolio: {len(portafolio)}")  # 2
    print(
        f"Balance total de la cartera: ${portafolio.balance_total:.2f}"
    )  # $3500.00