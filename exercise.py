from typing import Optional
from abc import ABC, abstractmethod
 
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        if price < 0:
            raise ValueError
        pierwsza_cyfra = -1
        for i, char in enumerate(name):
            if char.isdigit():
                pierwsza_cyfra = i
                break
        if pierwsza_cyfra <= 0: 
            raise ValueError
        litery = name[:pierwsza_cyfra]
        cyfry = name[pierwsza_cyfra:]
        if not litery.isalpha() or not cyfry.isdigit():
            raise ValueError
        self.name=name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return (self.name == other.name) and (self.price == other.price)  # FIXME: zwróć odpowiednią wartość
 
    def __hash__(self):
        return hash((self.name, self.price))
 
 
class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 3

    @abstractmethod
    def get_entries(self, n_letters: int = 1):
        pass

class ListServer(Server): 
    def __init__(self, products_list: list[Product]):
        self.products: list[Product]  = list(products_list)
    def get_entries(self, n_letters: int = 1):
        wyniki = []
        for x in self.products:
            nazwa = x.name
            indeks=-1
            for i, j in enumerate(nazwa):
                if j.isdigit():
                    indeks = i # indeks pierwszej cyfry odpowiada długości części literowej
                    break
            if indeks == n_letters and (len(nazwa)-indeks == 2 or len(nazwa)-indeks == 3):
                wyniki.append(x)
        wyniki.sort(key=lambda x: x.price)
        if len(wyniki) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return wyniki
    
 
 
class MapServer(Server):
    def __init__(self, products_list: list[Product]):
        self.products: dict[str, Product]= {}
        for x in products_list:
            self.products[x.name] = x
    def get_entries(self, n_letters: int = 1):
        wyniki = []
        for x, y in self.products.items():
            nazwa = x
            indeks = -1
            for i, j in enumerate(nazwa):
                if j.isdigit():
                    indeks = i # indeks pierwszej cyfry odpowiada długości części literowej
                    break
            if indeks == n_letters and (len(nazwa)-indeks == 2 or len(nazwa)-indeks == 3):
                wyniki.append(y)
        wyniki.sort(key=lambda x: x.price)
        if len(wyniki) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return wyniki
    

class Client:
    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            produkty = self.server.get_entries(n_letters)
            if not produkty:
                return None
            return sum(p.price for p in produkty)
        except TooManyProductsFoundError:
            return None