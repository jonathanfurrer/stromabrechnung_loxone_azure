from dataclasses import dataclass

@dataclass
class CustomerData:
    wohnung: str
    vorname: str
    nachname: str
    adresse: str
    ort: str
    plz: str
    email: str

@dataclass
class BankData:
    iban: str
    kontonr: str
    inhaber1: str
    inhaber2: str
