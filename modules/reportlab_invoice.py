# Reportlab
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import Color, black, blue, red, gray, lightblue

# utility
from datetime import date


class generate_invoice():
    # Abstände 
    l = 2 * cm  #linker abstand
    r = 19 * cm #rechter abstand
    o = 2 * cm #oben
    u = 2 * cm #unten
    b = 21 * cm #breite
    h = 29.7 * cm #höhe
    t = 19 * cm #starthöhe Tabelle
    z = 0.45 * cm #Zeilen Abstand Tabelle

    #Spalten
    x1 = l # Periode
    x2 = 5 * cm # Beschreibung
    x3 = 10 * cm # Anzahl
    x4 = 14 * cm # Preis pro Stück
    x5 = r # Total

    # Farben
    u_blue = Color( 0, 0.6, 0.6)

    def __init__(self,address_kunde,address_an,bank,):
        self.today = date.today()
        self.address_kunde = address_kunde
        self.address_an = address_an
        self.bank = bank
        pdfName = "Stromrechnung_" + self.address_kunde.wohnung + "_" + self.today.strftime("%Y-%m") + ".pdf"
        self.canv = Canvas(pdfName, pagesize=A4) # 21cm * 29.7cm
        self.totalAmount = 0
        self.createHeader()

    def createHeader(self):

        # D41 Strom 
        x = self.l
        y = self.h - self.o
        self.canv.setFont('Helvetica-Bold', 30)
        self.canv.setFillColor(black)  
        self.canv.drawString(x, y, "D41")
        self.canv.setFont('Helvetica-Oblique', 30)
        self.canv.setFillColor(gray)  
        self.canv.drawString(x + (2 * cm), y, "electricity")

        #ÜBERSCHRIFT / Rechnungs Periode 
        x = 12 * cm
        self.canv.setFont('Helvetica', 30)
        self.canv.setFillColor(black)  
        self.canv.drawString(x, y, "#Rechnung")
        self.canv.setFont('Helvetica', 13)
        self.canv.setFillColor(gray)  
        self.canv.drawString(x, y + (-0.5 * cm), self.today.strftime("%B %Y") + " / " + self.address_kunde.wohnung)

        # Kunde
        x = self.l
        y = 25 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(self.u_blue)  
        self.canv.drawString (x , y, "Kunde:")
        self.canv.setFillColor(black)  
        x = 3.3 * cm
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawString(x , y, self.address_kunde.wohnung)
        self.canv.setFont('Helvetica', 10)
        self.canv.drawString(x , y - (1*z), self.address_kunde.vorname  + " " + self.address_kunde.nachname)
        self.canv.drawString(x , y - (2*z), self.address_kunde.adresse)
        self.canv.drawString(x , y - (3*z) , self.address_kunde.plz + " " + self.address_kunde.ort)
        self.canv.drawString(x , y - (4*z) , self.address_kunde.email)

        # zu bezahlen an
        x = 11 * cm
        y = 23.5 * cm
        z = 0.45 * cm
        abstand = 0.2 *cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(self.u_blue)  
        self.canv.drawRightString (x - abstand , y , "bezahlen an:")
        self.canv.setFillColor(black)  
        self.canv.drawString(x , y - (0*z), self.bank.inhaber1 )
        self.canv.drawString(x , y - (1*z), self.bank.inhaber2)
        self.canv.drawString(x , y - (2*z), self.address_an.adresse)
        self.canv.drawString(x , y - (3*z) ,self.address_an.plz + " " + self.address_an.ort)
        self.canv.drawString(x , y - (4*z) ,self.address_an.email)
    
        # Bank Verbindung
        y = 25 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(self.u_blue)  
        self.canv.drawRightString (x - abstand, y , "Bank:")
        self.canv.setFillColor(black)  
        self.canv.drawString(x , y, self.bank.namebank)
        self.canv.drawString(x , y - z, self.bank.kontonr)
        self.canv.drawString(x , y - (2*z), self.bank.iban)


        # offizielle Preise
        y = 21 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(self.u_blue)  
        self.canv.drawRightString (x - abstand, y , "Info's:")
        self.canv.setFillColor(black)  
        self.canv.drawString(x , y, "Preise Strom Oberdiessbach")
        self.canv.setFont('Helvetica-Oblique', 7)
        self.canv.drawString(x , y - z, "oberdiessbach.ch/artikel/896/Verwaltung/Bauverwaltung/Elektrizitätsversorgung")

       
        # 1 Linie
        p = self.canv.beginPath()
        p.moveTo(self.l,self.t)
        p.lineTo(self.r,self.t)
        self.canv.drawPath(p, stroke=1, fill=1)
    
        # Überschriften
        self.canv.setFillColor(self.u_blue)  
        self.canv.setFont('Helvetica', 10)
        self.canv.drawString (self.x1 , self.t - self.z, "Periode")
        self.canv.drawString (self.x2 , self.t - self.z, "Beschreibung")
        self.canv.drawString (self.x3 ,self.t - self.z, "Anzahl")
        self.canv.drawString (self.x4 , self.t - self.z, "Preis pro Stück")
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawRightString (self.x5 , self.t - self.z, "Total")

        # 2 Linie
        i = 2
        p = self.canv.beginPath()
        p.moveTo(self.l,self.t - 2*self.z)
        p.lineTo(self.r,self.t - 2*self.z)
        self.canv.drawPath(p, stroke=1, fill=1)


    def newEntity(self,iLineNr, sPeriode, sBeschreibung, sAnzahl, sPreisProStück, sTotal):
        y = self.t - ((3 + iLineNr) * self.z)
        self.canv.setFillColor(black)  
        self.canv.setFont('Helvetica', 10)
        self.canv.drawString (self.x1 , y , sPeriode)
        self.canv.drawString (self.x2 , y , sBeschreibung)
        self.canv.drawString (self.x3 ,y , sAnzahl)
        self.canv.drawString (self.x4 , y , sPreisProStück)
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawRightString (self.x5 , y , sTotal)
    
    def newLine(self,iLineNr):
        y = self.t - ((3 + iLineNr) * self.z)
        p = self.canv.beginPath()
        p.moveTo(self.l,y )
        p.lineTo(self.r,y)
        self.canv.drawPath(p, stroke=1, fill=1)

    def drawTotal(self,iLineNr, sTotal, sCurrency):
        y = self.t - ((3 + iLineNr) * self.z)
        self.canv.setFillColor(black)  
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawRightString (self.x5 , y, sTotal + " " + sCurrency)

    def drawTotalFancy(self, sTotal, sCurrency):
        # Total Fancy
        self.canv.setFillColor(black)  
        self.canv.setFont('Helvetica-BoldOblique', 18)
        x = 5 * cm
        y = 21.5 * cm
        self.canv.drawRightString (x , y, sTotal)
        self.canv.setFont('Helvetica-Oblique', 10)
        self.canv.drawString (x , y, (" " + sCurrency))

        # Linie
        p = self.canv.beginPath()
        p.moveTo(x + 1 * cm,y + 0.2 * cm)
        p.lineTo(x + 3.5 * cm,y + 0.2 * cm)
        p.lineTo(x + 3.5 * cm,25.1 * cm)
        p.lineTo(x + 4.5 * cm,25.1 * cm)

        self.canv.drawPath(p, stroke=1)
        
    def save(self):
        self.canv.save()      
    

