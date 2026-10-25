from AccionInversion import Accion

class Portafolio:

    def __init__(self,inversionista):
        self.inversionista = inversionista
        self.lista_acciones = []

    def agregar_accion(self,accion:Accion):
        self.lista_acciones.append(accion)

    @staticmethod
    def es_ticker_valido(ticker:str) -> bool:
        return 1 <= len(ticker) <= 5 and ticker.upper()

    @property
    def balance_total(self):
        return sum(a.precio_actual * a.cantidad for a in self.lista_acciones)

    def __len__(self):
        return len(self.lista_acciones)

    def __getitem__(self, key):
        return self.lista_acciones[key]

    def __add__(self, other):

        if isinstance(other,Accion): 
            self.agregar_accion(other)
            return self

        return NotImplemented
    
        
        