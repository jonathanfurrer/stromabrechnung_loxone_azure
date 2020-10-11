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

    def __init__(self):
        pass

    def newInvoice(self, wohnung, empfänger , email ,month_kwh_day, month_kwh_night, kwh_preis_day, kwh_preis_night, grundgebühr):
        today = date.today()
        pdfName = "Stromrechnung_" + wohnung + "_" + today.strftime("%Y-%m") + ".pdf"
        canv = Canvas(pdfName, pagesize=A4) # 21cm * 29.7cm

        # X Abstände 
        l = 2 * cm  #linker abstand
        r = 19 * cm #rechter abstand
        
        # Farben
        u_blue = Color( 0, 0.6, 0.6)
        
        #ÜBERSCHRIFT / Rechnungs Periode 
        x = 12 * cm
        y = 27 * cm
        canv.setFont('Helvetica', 30)
        canv.setFillColor(black)  
        canv.drawString(x, y, "#Rechnung")
        canv.setFont('Helvetica', 13)
        canv.setFillColor(gray)  
        canv.drawString(x, y + (-0.5 * cm), today.strftime("%B %Y") + " / " + wohnung)

        # D41 Strom 
        x = l
        y = 27 * cm
        canv.setFont('Helvetica-Bold', 30)
        canv.setFillColor(black)  
        canv.drawString(x, y, "D41")
        canv.setFont('Helvetica-Oblique', 30)
        canv.setFillColor(gray)  
        canv.drawString(x + (2 * cm), y, "electricity")
        

        # Kunde
        x = l
        y = 24 * cm
        z = 0.45 * cm
        canv.setFont('Helvetica', 10)
        canv.setFillColor(u_blue)  
        canv.drawString (x , y, "Kunde:")
        canv.setFillColor(black)  
        x = 3.3 * cm
        canv.setFont('Helvetica-Bold', 10)
        canv.drawString(x , y, wohnung)
        canv.setFont('Helvetica', 10)
        canv.drawString(x , y - (1*z), empfänger)
        canv.drawString(x , y - (2*z), "Diessbachgrabenstrasse 41")
        canv.drawString(x , y - (3*z) , "3672 Oberdiessbach")

        # zu bezahlen an
        x = 11 * cm
        y = 24 * cm
        z = 0.45 * cm
        abstand = 0.2 *cm
        canv.setFont('Helvetica', 10)
        canv.setFillColor(u_blue)  
        canv.drawRightString (x - abstand , y , "bezahlen an:")
        canv.setFillColor(black)  
        canv.drawString(x , y, "Samuel Hossmann & Jonathan Furrer")
        canv.drawString(x , y - z, "Diessbachgrabenstrasse 41")
        canv.drawString(x , y - (2*z) , "3672 Oberdiessbach")

        # Bank Verbindung
        y = 22.5 * cm
        z = 0.45 * cm
        canv.setFont('Helvetica', 10)
        canv.setFillColor(u_blue)  
        canv.drawRightString (x - abstand, y , "Bank:")
        canv.setFillColor(black)  
        canv.drawString(x , y, "Bank SLM Konolfingen")
        canv.drawString(x , y - z, "IBAN: 023840982923498234")

        # Fragen an
        y = 21 * cm
        z = 0.45 * cm
        canv.setFont('Helvetica', 10)
        canv.setFillColor(u_blue)  
        canv.drawRightString (x - abstand, y , "Fragen:")
        canv.setFillColor(black)  
        canv.drawString(x , y, "Jonathan Furrer")
        canv.drawString(x , y - z, "jonathan.furrer@gmail.com")

        # offizielle Preise
        y = 19.5 * cm
        z = 0.45 * cm
        canv.setFont('Helvetica', 10)
        canv.setFillColor(u_blue)  
        canv.drawRightString (x - abstand, y , "Info's:")
        canv.setFillColor(black)  
        canv.drawString(x , y, "Preise Strom Oberdiessbach")
        canv.setFont('Helvetica-Oblique', 7)
        canv.drawString(x , y - z, "oberdiessbach.ch/artikel/896/Verwaltung/Bauverwaltung/Elektrizitätsversorgung")



        # Zussamenstellung 
        y = 17 * cm
        z = 0.45 * cm
        #Spalten
        x1 = l # Periode
        x2 = 5 * cm # Beschreibung
        x3 = 10 * cm # Anzahl
        x4 = 14 * cm # Preis pro Stück
        x5 = r # Total

        # 1 Linie
        p = canv.beginPath()
        p.moveTo(l,y)
        p.lineTo(r,y)
        canv.drawPath(p, stroke=1, fill=1)

        
        # Überschriften
        canv.setFillColor(u_blue)  
        canv.setFont('Helvetica', 10)
        canv.drawString (x1 , y - z, "Periode")
        canv.drawString (x2 , y - z, "Beschreibung")
        canv.drawString (x3 ,y - z, "Anzahl")
        canv.drawString (x4 , y - z, "Preis pro Stück")
        canv.setFont('Helvetica-Bold', 10)
        canv.drawRightString (x5 , y - z, "Total")

        # 2 Linie
        i = 2
        p = canv.beginPath()
        p.moveTo(l,y -i*z)
        p.lineTo(r,y -i*z)
        canv.drawPath(p, stroke=1, fill=1)

        # Total init
        total = 0
        # 1er Eintrag
        i = 3
        canv.setFillColor(black)  
        canv.setFont('Helvetica', 10)
        canv.drawString (x1 , y - (i*z), today.strftime("%B %Y"))
        canv.drawString (x2 , y - (i*z), "Hochtarif / Tag")
        canv.drawString (x3 ,y - (i*z), str(month_kwh_day) + " kWh")
        canv.drawString (x4 , y - (i*z), str(kwh_preis_day) + " CHF")
        canv.setFont('Helvetica-Bold', 10)
        subtotal = round(month_kwh_day * kwh_preis_day, 2)
        total += subtotal
        canv.drawRightString (x5 , y - (i*z), str(subtotal) + " CHF")

        # 2er Eintrag
        i = 4
        canv.setFillColor(black)  
        canv.setFont('Helvetica', 10)
        canv.drawString (x1 , y - (i*z), today.strftime("%B %Y"))
        canv.drawString (x2 , y - (i*z), "Niedertarif / Nacht")
        canv.drawString (x3 ,y - (i*z), str(month_kwh_night) + " kWh")
        canv.drawString (x4 , y - (i*z), str(kwh_preis_night) + " CHF")
        canv.setFont('Helvetica-Bold', 10)
        subtotal = round(month_kwh_night * kwh_preis_night, 2)
        total += subtotal
        canv.drawRightString (x5 , y - (i*z), str(subtotal) + " CHF")

        # 3er Eintrag
        i = 5
        canv.setFillColor(black)  
        canv.setFont('Helvetica', 10)
        canv.drawString (x1 , y - (i*z), today.strftime("%B %Y"))
        canv.drawString (x2 , y - (i*z), "Grundgebühr")
        canv.drawString (x3 ,y - (i*z),"1x pro Jahr")
        canv.drawString (x4 , y - (i*z), str(grundgebühr) + " CHF")
        canv.setFont('Helvetica-Bold', 10)
        subtotal = round(grundgebühr / 12, 2)
        total += subtotal
        canv.drawRightString (x5 , y - (i*z), str(subtotal) + " CHF")

        # 3 Linie
        i = 6
        p = canv.beginPath()
        p.moveTo(l,y -i*z)
        p.lineTo(r,y -i*z)
        canv.drawPath(p, stroke=1, fill=1)

        # Total Tabelle
        i = 7
        canv.setFillColor(black)  
        canv.setFont('Helvetica-Bold', 10)
        canv.drawRightString (x5 , y - (i*z), str(total) + " CHF")


        # Total Fancy
        canv.setFillColor(black)  
        canv.setFont('Helvetica-BoldOblique', 18)
        x = 5 * cm
        y = 19.5 * cm
        canv.drawRightString (x , y, str(total))
        canv.setFont('Helvetica-Oblique', 10)
        canv.drawString (x , y, " CHF")

        # Linie
        p = canv.beginPath()
        p.moveTo(x + 1 * cm,y + 0.2 * cm)
        p.lineTo(x + 3 * cm,y + 0.2 * cm)
        p.lineTo(x + 3 * cm,24.1 * cm)
        p.lineTo(x + 3.5 * cm,24.1 * cm)

        canv.drawPath(p, stroke=1)



        canv.save()


def main():
    g = generate_invoice()
    g.newInvoice("272-4", "Jonathan Furrer", "jonathan.furrer@gmail.com", 30,60,0.22,0.15,100)


if __name__ == '__main__':
    main()
