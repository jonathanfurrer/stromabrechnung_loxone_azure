# IMPORT --------------------------------------------------------------
# Utility
import logging
# Azure Cosmos
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
#Local import
from modules.dataObjects import BankData,CustomerData


# Config logging
# logging.basicConfig(filename="/home/pi/git/unifi_loxone_bridge/log.log",
logging.basicConfig(filename="log.log",
                    level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)

try:
    credential = "eFH0EUaE6HU8GaqS9S04vf2MLdQ94vMdbMg6kaMetKG1gXU8g+QUtfAKxbtvyjj6Vrq4X3E0hBVNe5gIzjFZHQ=="
    table_service = TableService(
        account_name="jofustrom456789", account_key=credential)
        
    logging.debug("connected to Azure Table Storage")
except:
    logging.warning("could not connect to Azure Table Storage")

# Get newest Adress Data from Azure
try:
    adress = table_service.get_entity('Adressen','272-1','1')
    adressData272_1 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-1")

try:
    adress = table_service.get_entity('Adressen','272-2','2')
    adressData272_2 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-2")

try:
    adress = table_service.get_entity('Adressen','272-3','3')
    adressData272_3 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-3")

try:
    adress = table_service.get_entity('Adressen','272-4','4')
    adressData272_4 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-4")





