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

TABLE_ADRESSEN = "Adressen"
TABLE_BANKVERBINDUNG = "Bankverbindung"
TABLE_PREISE = "Preise"
TABLE_RECHNUNGEN = "Rechnungen"
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
    adress = table_service.get_entity(TABLE_ADRESSEN,'272-1','1')
    adressData272_1 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-1")

try:
    adress = table_service.get_entity(TABLE_ADRESSEN,'272-2','2')
    adressData272_2 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-2")

try:
    adress = table_service.get_entity(TABLE_ADRESSEN,'272-3','3')
    adressData272_3 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-3")

try:
    adress = table_service.get_entity(TABLE_ADRESSEN, '272-4','4')
    adressData272_4 = CustomerData(adress.Wohnung,adress.Vorname,adress.Name,adress.Adresse,adress.Ort,adress.PLZ,adress.email)
except:
    logging.warning("failed to load adress data from azure table 272-4")

# Bank --------------------------------------------------
try:
    bank = table_service.get_entity(TABLE_BANKVERBINDUNG,'Universalkonto','1')
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

total = 0
line = 1
open_invoice = list(open_invoice)
inv = generate_invoice(address_kunde=adressData272_1,address_an=adressData272_4,bank=bankData)

for oi in open_invoice:
    # Preise ------------------------------------------------
    # Grundgebühr
    f = "PartitionKey eq 'Grundgebühr' and Year eq " + str(oi.year)
    try:
        grundgebühr = table_service.query_entities(TABLE_PREISE, filter=f , timeout=60)
        grundgebühr = list(grundgebühr) 
    except:
        logging.warning("failed to load adress data from azure table " + TABLE_PREISE)
    # Hochtarif / Tag
    f = "PartitionKey eq 'Hochtarif' and Year eq " + str(oi.year)
    try:
        hochtarif = table_service.query_entities(TABLE_PREISE, filter=f , timeout=60)
        hochtarif = list(hochtarif)
    except:
        logging.warning("failed to load adress data from azure table " + TABLE_PREISE)
    # Niedertarif / Nacht
    f = "PartitionKey eq 'Niedertarif' and Year eq " + str(oi.year)
    try:
        niedertarif = table_service.query_entities(TABLE_PREISE , filter=f , timeout=60)
        niedertarif = list(niedertarif)   
    except:
        logging.warning("failed to load adress data from azure table " + TABLE_PREISE)

    if "day" in oi.tarif:
        tarif = "Hochtarif / Tag"
        preis = str(hochtarif[0].Preis) + " " +  str(hochtarif[0].Währung)
        total += (hochtarif[0].Preis * oi.value)
        subtotal = str(round(hochtarif[0].Preis * oi.value,2)) + " " +  str(hochtarif[0].Währung)
    else:
        tarif = "Niedertarif / Nacht"
        preis = str(niedertarif[0].Preis) + " " +  str(niedertarif[0].Währung)
        total += (niedertarif[0].Preis * oi.value)
        subtotal = str(round(niedertarif[0].Preis * oi.value,2)) + " " +  str(niedertarif[0].Währung)

    value = str(oi.value) + " " + str(oi.unit)
    inv.newEntity(line,MONTHS[oi.month] ,tarif, value ,preis ,subtotal)
    line += 1


# Grundgebühr
periode = MONTHS[open_invoice[0].month] + " - " + MONTHS[open_invoice[-1].month]
anzMonate = round((line -1) /2)
preis = str(grundgebühr[0].Preis) + " " +  str(grundgebühr[0].Währung)
total += (grundgebühr[0].Preis / 12 * anzMonate)
subtotal = str(round(grundgebühr[0].Preis / 12 * anzMonate,2)) + " " +  str(grundgebühr[0].Währung)

inv.newEntity(line,periode ,"Grundgebühr pro Jahr", (str(anzMonate) + " Monate") , preis , subtotal)
line += 1
inv.newLine(line)
line += 1
total = round(total,2)
inv.drawTotal(line,total, niedertarif[0].Währung)
inv.drawTotalFancy(total, niedertarif[0].Währung)
inv.save()




