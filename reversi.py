import tkinter

class Gui():
    
    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 50

    X_0=7
    Y_0=7

    
    def __init__(self, master):
        # Objekti, ki predstavljajo belega, črnega igralca in igro
        self.igralec_beli = None 
        self.igralec_crni = None
        self.igra = None 

        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu)


        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=lambda: self.zacni_igro())


        # Napis, ki prikazuje stanje igre
        vsota_beli=2
        vsota_crni=2
        self.napis1 = tkinter.StringVar(master, value='ČRNI:'+str(vsota_crni))
        tkinter.Label(master, textvariable=self.napis1).grid(row=0, column=1)
        self.napis2 = tkinter.StringVar(master, value='BELI:'+str(vsota_beli))
        tkinter.Label(master, textvariable=self.napis2).grid(row=0, column=2)

        # Igralno območje
        self.plosca = tkinter.Canvas(master, width=8*Gui.VELIKOST_POLJA + 2*Gui.X_0,
                                     height=8*Gui.VELIKOST_POLJA+ 2*Gui.Y_0)
        self.plosca.grid(row=1, column=0, columnspan=4)


        # Črte na igralnem polju
        self.narisi_crte()
        self.narisi_zacetno_pozicijo()

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Prični igro v načinu človek proti človeku
        self.zacni_igro()

    def zacni_igro(self):
        #NI ŠE
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vse igralce (ki morda razmišljajo)
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_x = Clovek(self)
        self.igralec_o = Clovek(self)
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        # Ustvarimo novo igro
        self.igra = Igra()
        # Križec je prvi na potezi
        self.napis.set("Na potezi je X.")
        self.igralec_x.igraj()
        
    def koncaj_igro(self):
        """Nastavi stanje igre na konec igre."""
        self.napis.set("Konec igre.")

    def prekini_igralce(self):
        #NI ŠE
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.igralec_x: self.igralec_x.prekini()
        if self.igralec_o: self.igralec_o.prekini()

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
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
        self.narisi_belega((3,3))
        self.narisi_belega((4,4))
        self.narisi_crnega((3,4))
        self.narisi_crnega((4,3))
    

    def narisi_belega(self, p):
        """Nariši križec v polje (i, j)."""
        x = p[0] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[1] * Gui.VELIKOST_POLJA + Gui.Y_0
        sirina = 1
        self.plosca.create_oval(x+10, y+10, x+40, y+40,
                                width=sirina,tag=Gui.TAG_FIGURA)
        
    def narisi_crnega(self, p):
        """Nariši krožec v polje (i, j)."""
        x = p[0] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[1] * Gui.VELIKOST_POLJA + Gui.Y_0
        sirina = 1
        self.plosca.create_oval(x+10, y+10, x+40, y+40,
                                width=sirina,tag=Gui.TAG_FIGURA, fill='black')




    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = (event.x - Gui.X_0)// Gui.VELIKOST_POLJA 
        j = (event.y - Gui.Y_0) // Gui.VELIKOST_POLJA 
        print ("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
        self.povleci_potezo((i,j))

    def plosca_klik(self, event):
        #NI ŠE
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = (event.x - Gui.X_0)// Gui.VELIKOST_POLJA 
        j = (event.y - Gui.Y_0) // Gui.VELIKOST_POLJA 
        if 0 <= i <= 2 and 0 <= j <= 2:
            if self.igra.na_potezi == IGRALEC_X:
                self.igralec_x.klik((i,j))
            elif self.igra.na_potezi == IGRALEC_O:
                self.igralec_o.klik((i,j))
            else:
                # Nihče ni na potezi, ne naredimo nič
                pass
        else:
            # klik izven plošče
            pass
    
        
    def povleci_potezo(self, p):
        #NI ŠE
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        # Najprej povlečemo potezo v igri, še pred tem si zapomnimo, kdo jo je povlekel
        # (ker bo self.igra.povleci_potezo spremenil stanje igre).
        # GUI se *ne* ukvarja z logiko igre, zato ne preverja, ali je poteza veljavna.
        # Ta del bo kasneje za njega opravil self.igra.
        igralec = self.igra.na_potezi
        self.igra.povleci_potezo(p)
        if igralec == IGRALEC_B:
            self.narisi_X(p)
        elif igralec == IGRALEC_C:
            self.narisi_O(p)
        # Popravimo napis, kdo je na potezi
        self.napis.set("Na potezi je {0}".format(
            'X' if self.igra.na_potezi == IGRALEC_X else 'O'))













            
        
if __name__ == "__main__":
    
    root = tkinter.Tk()
    root.title("Reversi")
    aplikacija = Gui(root)
    root.mainloop()













        


        
