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


class generate_invoice(object):
    # Abstände 
    l = 2 * cm  #linker abstand
    r = 19 * cm #rechter abstand
    o = 2 * cm #oben
    u = 2 * cm #unten
    b = 21 * cm #breite
    h = 29.7 * cm #höhe
    t = 17 * cm #starthöhe Tabelle
    z = 0.45 * cm #Zeilen Abstand Tabelle

    #Spalten
    x1 = l # Periode
    x2 = 5 * cm # Beschreibung
    x3 = 10 * cm # Anzahl
    x4 = 14 * cm # Preis pro Stück
    x5 = r # Total

    # Farben
    u_blue = Color( 0, 0.6, 0.6)

    def __init__(self,wohnung):
        today = date.today()
        pdfName = "Stromrechnung_" + wohnung + "_" + today.strftime("%Y-%m") + ".pdf"
        self.canv = Canvas(pdfName, pagesize=A4) # 21cm * 29.7cm
        self.totalAmount = 0
        pass

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
        self.canv.drawString(x, y + (-0.5 * cm), today.strftime("%B %Y") + " / " + wohnung)

        # Kunde
        x = self.l
        y = 24 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(self.u_blue)  
        self.canv.drawString (x , y, "Kunde:")
        self.canv.setFillColor(black)  
        x = 3.3 * cm
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawString(x , y, self.wohnung)
        self.canv.setFont('Helvetica', 10)
        self.canv.drawString(x , y - (1*z), vorname  + " " + name)
        self.canv.drawString(x , y - (2*z), addresse)
        self.canv.drawString(x , y - (3*z) , plz + " " + ort)
        self.canv.drawString(x , y - (4*z) , email)

        # zu bezahlen an
        x = 11 * cm
        y = 24 * cm
        z = 0.45 * cm
        abstand = 0.2 *cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(u_blue)  
        self.canv.drawRightString (x - abstand , y , "bezahlen an:")
        self.canv.setFillColor(black)  
        self.canv.drawString(x , y - (1*z), vorname  + " " + name)
        self.canv.drawString(x , y - (2*z), addresse)
        self.canv.drawString(x , y - (3*z) , plz + " " + ort)
        self.canv.drawString(x , y - (4*z) , email)
    
        # Bank Verbindung
        y = 22.5 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(u_blue)  
        self.canv.drawRightString (x - abstand, y , "Bank:")
        self.canv.setFillColor(black)  
        self.canv.drawString(x , y, "Bank SLM Konolfingen")
        self.canv.drawString(x , y - z, "IBAN: 023840982923498234")

        # offizielle Preise
        y = 19.5 * cm
        z = 0.45 * cm
        self.canv.setFont('Helvetica', 10)
        self.canv.setFillColor(u_blue)  
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
        self.canv.drawString (x1 , y - (i*z), sPeriode)
        self.canv.drawString (x2 , y - (i*z), sBeschreibung)
        self.canv.drawString (x3 ,y - (i*z), sAnzahl)
        self.canv.drawString (x4 , y - (i*z), sPreisProStück)
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawRightString (x5 , y - (i*z), sTotal)
    
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
        y = 19.5 * cm
        self.canv.drawRightString (x , y, sTotal)
        self.canv.setFont('Helvetica-Oblique', 10)
        self.canv.drawString (x , y, (" " + sCurrency))

        # Linie
        p = self.canv.beginPath()
        p.moveTo(x + 1 * cm,y + 0.2 * cm)
        p.lineTo(x + 3 * cm,y + 0.2 * cm)
        p.lineTo(x + 3 * cm,24.1 * cm)
        p.lineTo(x + 3.5 * cm,24.1 * cm)

        self.canv.drawPath(p, stroke=1)
        self.canv.save()


    def getInvoice(self,  empfänger , email ,month_kwh_day, month_kwh_night, kwh_preis_day, kwh_preis_night, grundgebühr):
        
        self.createHeader()




        


        


def main():
    g = generate_invoice()
    g.newInvoice("272-4", "Jonathan Furrer", "jonathan.furrer@gmail.com", 30,60,0.22,0.15,100)


if __name__ == '__main__':
    main()
