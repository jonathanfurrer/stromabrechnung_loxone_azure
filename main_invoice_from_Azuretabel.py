# IMPORT --------------------------------------------------------------
# Utility
import logging
import datetime
# Azure Cosmos
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
#Local import
from modules.dataObjects import BankData,CustomerData
from modules.reportlab_invoice import generate_invoice

TABLE_STROMBEZUG = "Strombezug"
MONTHS = [('Januar'),
        ('Februar'),
        ('März'),
        ('April'),
        ('Mai',),
        ('Juni'),
        ('Juli'),
        ('August'),
        ('September'),
        ('Oktober'),
        ('November'),
        ('Dezember')]

now = datetime.datetime.now()

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
    exit

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

# Bank --------------------------------------------------
try:
    bank = table_service.get_entity('Bankverbindung','Universalkonto','1')
    bankData = BankData(namebank=bank.NameBank, iban=bank.IBAN,kontonr=bank.KontoNr,inhaber1=bank.Inhaber1,inhaber2=bank.Inhaber2)
except:
    logging.warning("failed to load adress data from azure table Bankverbindung")



# Generate Invoice for 272-1
# Get Invoice information
f = "PartitionKey eq '272-4' and cleared eq false"        
try:
    open_invoice = table_service.query_entities(TABLE_STROMBEZUG, filter=f , timeout=60)

except:
    logging.warning("failed to load adress data from azure table Bankverbindung")

# Preise ------------------------------------------------
f = "PartitionKey eq 'Grundgebühr' and Year eq " + now.year    
try:
    grundgebühr = table_service.query_entities(TABLE_STROMBEZUG, filter=f , timeout=60)
except:
    logging.warning("failed to load adress data from azure table Bankverbindung")

inv = generate_invoice(address_kunde=adressData272_1,address_an=adressData272_4,bank=bankData)

total = 0
line = 1
open_invoice = list(open_invoice)
for o in open_invoice:
    print()
    inv.newEntity(1,o.Month,"Hochtarif", "30", "0.22 CHF","23.00 CHF")

inv.newLine(4)
inv.drawTotal(5,"30.00", "CHF")
inv.drawTotalFancy("30.00", "CHF")
inv.save()




