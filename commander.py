from webbot import Browser
import operator, time
from bot import sichern, login, get_items, erfolg_pruefen
from datetime import datetime
import json



acc = int(input("Welcher Nutzer? (0 Bubu, 1 Baer)"))


with open('settings.txt') as json_file:
    data = json.load(json_file)
    User = data[acc]["User"]
    Pass = data[acc]["Pass"]
    Window = data[acc]["Window"]
    if Window == "False":
        Window = False
    wait = int(data[acc]["wait"])



web = Browser(showWindow= Window)
print("Login")
login(User, Pass, web)

run = True
while run:
    print("Favoriten durchsuchen")
    Items, IDs = get_items(web)
    Items.sort(key = operator.itemgetter("Zeit"))
    Wartezeit = Items[0]["Zeit"] - int(datetime.today().timestamp())
    if Wartezeit > 120:
        print(str(Wartezeit) + " s bis nächster Deal, 1 min warten")
        time.sleep(60)
    else:
        Versuche = 0
        print("Versuche Deal " + str(Items[0]["Name"]) + " in " + str(Wartezeit) + " s zu sichern")
        print(sichern(Items[0]["ID/Link"], Items[0]["Zeit"], wait, web))
        Versuche += 1
        for Item in Items[1:]:
            if Item["Zeit"] - int(datetime.today().timestamp()) < 10:
                print("Versuche Deal " + str(Item["Name"]) + " in " + str(Item["Zeit"] - int(datetime.today().timestamp())) + " s zu sichern")
                print(sichern(Item["ID/Link"], Item["Zeit"], wait, web))
                Versuche += 1
            else:
                break
        erfolg = erfolg_pruefen(Items, Versuche, web, User)

web.quit()

