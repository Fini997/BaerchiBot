import time
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta
from send_email import send_email


def login(User, Pass, web):
    web.go_to("https://tiger.deals/login/")
    web.type(User, into = "Dein Login")
    web.type(Pass, into = "Dein Passwort")
    web.click("Anmelden")
    time.sleep(2)
def sichern (ID, Time, wait, web):
    if isinstance(ID, int):
        url = "https://tiger.deals/snag-cashback/?campaign_id=" + str(ID)
        zeit = Time - int(dt.today().timestamp())
        web.go_to(url)
        web.scrolly(400)
        if Time < 1:
            print("Keine Wartezeit")
        else:
            print("Warte " + str(zeit) + " s")
            time.sleep(zeit)
        for x in range(wait):
            print("Sichern Versuch " + str(x+1))
            try:
                web.click("Jetzt Cashback Deal sichern")
            except:
                time.sleep(0.5)
            time.sleep(0.5)
        return "Fertig"
    else:
        web.go_to(ID)
        zeit = Time - int(dt.today().timestamp())
        web.scrolly(300)
        if Time < 1:
            print("Keine Wartezeit")
        else:
            print("Warte " + str(zeit) + " s")
            time.sleep(zeit+1)
        for x in range(wait):
            print("Sichern Versuch " + str(x + 1))
            try:
                web.click("Deal sichern")
            except:
                time.sleep(0.5)
            time.sleep(0.5)
        return "Fertig"

def get_items(web):
    web.go_to("https://tiger.deals/favorite-products/")
    try:
        web.click("Mach ich später")
    except:
        pass
    x = web.get_page_source()
    soup = BeautifulSoup(x, 'html.parser')
    Sachen = []
    IDs = []
    for Produkte in soup.find_all("article"):
        try:
            Zeit = int(Produkte["data-publish-date"])
        except:
            Zeit = 0
        deal_typ = Produkte["data-discount-type"]
        if deal_typ == "cashback":
            ID = int(Produkte["data-id"])
        else:
            ID = Produkte.find("a")["href"]
        Produkt = Produkte.find("h1", class_="card__title")  # Produktname
        Produkt = Produkt.get_text()
        Art = Produkte["data-discount-type"]
        Sachen.append({"Zeit": Zeit, "ID/Link": ID, "Name": Produkt, "Typ": Art})
        IDs.append(ID)
    return Sachen, IDs

def erfolg_pruefen(Items, Versuche, web, User):
    web.go_to("https://tiger.deals/mein-profil-tiger-deals/")
    time.sleep(2)
    x = web.get_page_source()
    soup = BeautifulSoup(x, 'html.parser')
    artikel = []
    for Produkte in soup.find_all("article"):
        Produkt = Produkte.find("h1", class_="user-deal__title")  # Produktname
        Produkt = Produkt.get_text()
        artikel.append(Produkt)
    for Item in Items[0:Versuche]:
        if Item["Name"] in artikel:
            print(Item["Name"] + " gesichert, sende Email...")
            send_email(Item["Name"], get_zeit(), User)
            print("Email gesendet")

def get_zeit():
    time = dt.today() + timedelta(hours=5)
    return time.strftime("%H:%M:%S")

