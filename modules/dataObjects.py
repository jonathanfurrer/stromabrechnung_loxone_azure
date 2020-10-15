from dataclasses import dataclass

from azure.cosmosdb.table.models import Entity

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
    namebank: str
    iban: str
    kontonr: str
    inhaber1: str
    inhaber2: str


