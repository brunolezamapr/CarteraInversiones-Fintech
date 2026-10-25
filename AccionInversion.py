from descriptors import ValidarPrecioAccion
class Accion:

    precio_actual = ValidarPrecioAccion("precio_actual")
    def __init__(self,precio_actual:float,ticker:str,cantidad:int):
        self.precio_actual = precio_actual
        self.ticker = ticker
        self.cantidad = cantidad

    @property
    def valor_total(self):
        return self.precio_actual * self.cantidad

    def __repr__(self) -> str:
        return f"Accion(ticker='{self.ticker}', cantidad={self.cantidad}, precio=${self.precio_actual:.2f})"

 


