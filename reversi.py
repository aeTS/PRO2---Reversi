import tkinter
import argparse
import logging

MINIMAX_GLOBINA = 4


from logika import *
from clovek import *
from racunalnik import *

##########################################################################
#Uporabniški vmesnik


class Gui():

    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 50

    X_0=7
    Y_0=7


    def __init__(self, master, globina):
        # Objekti, ki predstavljajo belega, črnega igralca in igro
        self.igralec_beli = None
        self.igralec_crni = None
        self.igra = None
        self.id_matrika = [8*[0] for _ in range(8)]

        # Če uporabnik zapre okno, se pokliče self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu)


        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="črni=Človek, beli=Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self)))
        menu_igra.add_command(label="črni=Človek, beli=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="črni=Računalnik, beli=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Racunalnik(self, Minimax(globina))))

        menu_pomoc = tkinter.Menu(menu)
        menu.add_cascade(label="Pomoč", menu=menu_pomoc)
        menu_pomoc.add_command(label="Navodila",
                              command=lambda: self.navodila())





        self.napis = tkinter.Canvas(master, width=8*Gui.VELIKOST_POLJA + 2*Gui.X_0,
                                     height=Gui.VELIKOST_POLJA+ 2*Gui.Y_0)
        self.napis.grid(row=0, column=0, columnspan=4)

        # Napisi, ki prikazujejo stanje igre
        # Števca žetonov
        self.napis1 = tkinter.StringVar(master, value='ČRNI: 2')
        tkinter.Label(master, textvariable=self.napis1, font=("Verdana", 16, "bold")).grid(row=1, column=1)
        self.napis2 = tkinter.StringVar(master, value='BELI: 2')
        tkinter.Label(master, textvariable=self.napis2, font=("Verdana", 16, "bold")).grid(row=1, column=2)

        # Igralno območje
        self.plosca = tkinter.Canvas(master, width=8*Gui.VELIKOST_POLJA + 2*Gui.X_0,
                                     height=8*Gui.VELIKOST_POLJA+ 2*Gui.Y_0)
        self.plosca.grid(row=2, column=0, columnspan=4)



        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)


        # Prični igro v načinu človek proti računalniku
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)))

    def navodila(self):
        self.napis.delete("all")
        self.plosca.delete("all")
        self.napis1.set('')
        self.napis2.set('')
        self.napis.create_text(200, 25, text = "Navodila za igro Reversi",
                               font=("Verdana", 16, "bold"))
        self.plosca.create_text(Gui.X_0, Gui.Y_0, anchor = "nw", font=("Verdana", 10),
                                text="Igra se odvija na igralni plošči velikosti 8x8.\n"
                                "Na voljo je 64 žetonov, ki so na eni strani beli, \nna drugi pa črni.\n \n"
                                "PRAVILA IGRE:\n \n"
                                "1. Igralca izbereta barvo svojih žetonov.\n"
                                "2. Dana je začetna pozicija žetonov, vedno začne črni.\n"
                                "3. Svoj žeton mora vsakič postaviti poleg nasprotnikovega,\n"
                                "lahko vertikalno, horizontalno ali diagonalno.\n"
                                "4. Tako položeni žeton ujame enega ali več nasprotnikovih\n"
                                "žetonov med enega ali več svojih.\n"
                                "Ujeti žetoni se obrnejo in zato zamenjajo barvo.\n"
                                "5. Naslednji na potezi je beli.\n"
                                "Igralca tako nadaljujeta, dokler ne zapolnita vseh polj\n"
                                "ali dokler še imata možnost izvesti nadaljnjo potezo.\n"
                                "6. Zmaga tisti, ki ima na plošči več žetonov svoje barve.")



    def zacni_igro(self, igralec_crni, igralec_beli):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        self.prekini_igralce()
        self.plosca.delete("all")
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        self.napis.delete("all")
        # Ustvarimo novo igro
        self.igra = Logika()

        # Nastavimo igralce
        self.igralec_crni = igralec_crni
        self.igralec_beli = igralec_beli

        self.narisi_zacetno_pozicijo()

        self.napis1.set('ČRNI: 2')
        self.napis2.set('BELI: 2')
        # Črni igralec je prvi na potezi
        self.napis.create_text(200, 25, text = "Na potezi je: ",
                               font=("Verdana", 16, "bold"))
        self.zeton = self.napis.create_oval(300, 15, 325, 40,fill='black')
        self.igralec_crni.igraj()

    def koncaj_igro(self, crni, beli):
        """Nastavi stanje igre na konec igre."""

        if crni > beli:
            self.napis.delete("all")
            self.napis.create_text(200, 25, text = "Zmagal je: ",
                                   font=("Verdana", 16, "bold"))
            self.zeton = self.napis.create_oval(300, 15, 325, 40,fill='black')
            pass
        elif beli > crni:
            self.napis.delete("all")
            self.napis.create_text(200, 25, text = "Zmagal je: ",
                                   font=("Verdana", 16, "bold"))
            self.zeton = self.napis.create_oval(300, 15, 325, 40)
            pass
        else:
            self.napis.delete("all")
            self.napis.create_text(200, 25, text = "Neodločeno...",
                                   font=("Verdana", 16, "bold"))
            pass



    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.igralec_beli:
            self.igralec_beli.prekini()
        if self.igralec_crni:
            self.igralec_crni.prekini()

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        self.prekini_igralce()
        master.destroy()


    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        for k in range(10):
            self.plosca.create_line(k*d + Gui.X_0, 0*d + Gui.Y_0,
                                    k*d + Gui.X_0, 8*d + Gui.Y_0, tag=Gui.TAG_OKVIR)
            self.plosca.create_line(0*d + Gui.X_0, k*d + Gui.Y_0,
                                    8*d + Gui.X_0, k*d + Gui.Y_0, tag=Gui.TAG_OKVIR)

    def narisi_zacetno_pozicijo(self):
        self.narisi_crte()
        self.narisi_belega((3,3))
        self.narisi_belega((4,4))
        self.narisi_crnega((3,4))
        self.narisi_crnega((4,3))


    def narisi_belega(self, p):
        """Nariši bel žeton v polje (i, j)."""
        x = p[1] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[0] * Gui.VELIKOST_POLJA + Gui.Y_0
        a = (1/5) * Gui.VELIKOST_POLJA
        b = (4/5) * Gui.VELIKOST_POLJA
        zeton = self.plosca.create_oval(x+a, y+a, x+b, y+b,
                                        width=1, tag=Gui.TAG_FIGURA)
        self.id_matrika[p[0]][p[1]] = zeton

    def narisi_crnega(self, p):
        """Nariši črn žeton v polje (i, j)."""
        x = p[1] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[0] * Gui.VELIKOST_POLJA + Gui.Y_0
        a = (1/5) * Gui.VELIKOST_POLJA
        b = (4/5) * Gui.VELIKOST_POLJA
        zeton = self.plosca.create_oval(x+a, y+a, x+b, y+b,
                                        width=1,tag=Gui.TAG_FIGURA,
                                        fill='black')
        self.id_matrika[p[0]][p[1]] = zeton

    def plosca_klik(self, event):
        """Odzovi se na klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        st = (event.x - Gui.X_0)// Gui.VELIKOST_POLJA
        vr = (event.y - Gui.Y_0) // Gui.VELIKOST_POLJA

        if 0 <= vr <= 7 and 0 <= st <= 7:
            if self.igra.na_potezi == IGRALEC_C:
                self.igralec_crni.klik((vr, st))
            elif self.igra.na_potezi == IGRALEC_B:
                self.igralec_beli.klik((vr, st))
            else:
                # Nihče ni na potezi
                pass
        else:
            # klik izven plošče
            logging.debug("klik izven plošče {0}, polje {1}".format((event.x,event.y), (st,vr)))
            pass


    def pobarvaj_vmesne(self):
        plosca = self.igra.plosca
        for vr in range(len(plosca)):
            for st in range(len(plosca[0])):
                if plosca[vr][st] == "B":
                    self.plosca.delete(self.id_matrika[vr][st])
                    self.narisi_belega((vr, st))
                elif plosca[vr][st] == "C":
                    self.plosca.delete(self.id_matrika[vr][st])
                    self.narisi_crnega((vr, st))



    def povleci_potezo(self, p):
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        igralec = self.igra.na_potezi
        s = self.igra.povleci_potezo(p)
        if s is None:
            pass
        else:
            self.pobarvaj_vmesne()
            (stanje, crni, beli) = s
            self.napis1.set('ČRNI: '+str(crni))
            self.napis2.set('BELI: '+str(beli))

            if stanje == NI_KONEC:
                if self.igra.na_potezi == IGRALEC_C:
                    self.napis.delete("all")
                    self.napis.create_text(200, 25, text = "Na potezi je: ",
                               font=("Verdana", 16, "bold"))
                    self.zeton = self.napis.create_oval(300, 15, 325, 40,fill='black')

                    self.igralec_crni.igraj()
                elif self.igra.na_potezi == IGRALEC_B:
                    self.napis.delete("all")
                    self.napis.create_text(200, 25, text = "Na potezi je: ",
                               font=("Verdana", 16, "bold"))
                    self.zeton = self.napis.create_oval(300, 15, 325, 40)

                    self.igralec_beli.igraj()
            elif stanje == KONEC:
                self.koncaj_igro(crni, beli)
            else:
                assert False, "nedifinirano stanje igre"









#############################################################################
#Glavni program





if __name__ == "__main__":
    # Iz ukazne vrstice poberemo globino za minimax, uporabimo
    # modul argparse, glej https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica Reversi.")
    # Argument --globina n, s privzeto vrednostjo MINIMAX_GLOBINA
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Reversi")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, args.globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
