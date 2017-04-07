import tkinter

from logika import *
from clovek import *

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
                              command=lambda: self.zacni_igro())


        # Napisi, ki prikazujejo stanje igre
        
        # Kdo je na potezi itd.
        #self.napis = tkinter.StringVar(master, value='Othello vas izziva na dvoboj!')
        #tkinter.Label(master, textvariable=self.napis).grid(row=2, column=0)
        # Števca žetonov
        self.napis1 = tkinter.StringVar(master, value='ČRNI: 2')
        tkinter.Label(master, textvariable=self.napis1, font=("Verdana", 16, "bold")).grid(row=0, column=1)
        self.napis2 = tkinter.StringVar(master, value='BELI: 2')
        tkinter.Label(master, textvariable=self.napis2, font=("Verdana", 16, "bold")).grid(row=0, column=2)

        # Igralno območje
        self.plosca = tkinter.Canvas(master, width=8*Gui.VELIKOST_POLJA + 2*Gui.X_0,
                                     height=8*Gui.VELIKOST_POLJA+ 2*Gui.Y_0)
        self.plosca.grid(row=1, column=0, columnspan=4)


        # Črte na igralnem polju
        self.narisi_crte()
        

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Prični igro v načinu človek proti človeku
        self.zacni_igro()

    def zacni_igro(self):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_crni = Clovek(self)
        self.igralec_beli = Clovek(self)
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        # Ustvarimo novo igro
        self.igra = Logika()
        self.narisi_zacetno_pozicijo()
        # Črni igralec je prvi na potezi
        #self.napis.set("Na potezi je črni.")
        self.igralec_crni.igraj()
        
    def koncaj_igro(self, crni, beli):
        """Nastavi stanje igre na konec igre."""
        #self.napis.set("Konec igre.")
        if crni > beli:
            #self.napis.set("Zmagal je črni.")
            pass
        elif beli > crni:
            #self.napis.set("Zmagal je beli.")
            pass
        else:
            #self.napis.set("Neodločeno.")
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
        self.narisi_belega((3,3))
        self.narisi_belega((4,4))
        self.narisi_crnega((3,4))
        self.narisi_crnega((4,3))
    

    def narisi_belega(self, p):
        """Nariši bel žeton v polje (i, j)."""
        x = p[1] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[0] * Gui.VELIKOST_POLJA + Gui.Y_0
        sirina = 1
        zeton = self.plosca.create_oval(x+10, y+10, x+40, y+40,
                                        width=sirina, tag=Gui.TAG_FIGURA)
        self.id_matrika[p[0]][p[1]] = zeton
        
    def narisi_crnega(self, p):
        """Nariši črn žeton v polje (i, j)."""
        x = p[1] * Gui.VELIKOST_POLJA + Gui.X_0
        y = p[0] * Gui.VELIKOST_POLJA + Gui.Y_0
        sirina = 1
        zeton = self.plosca.create_oval(x+10, y+10, x+40, y+40,
                                        width=sirina,tag=Gui.TAG_FIGURA,
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
                    #self.napis.set("Na potezi je X.")
                    self.igralec_crni.igraj()
                elif self.igra.na_potezi == IGRALEC_B:
                    #self.napis.set("Na potezi je O.")
                    self.igralec_beli.igraj()
            else:
                self.koncaj_igro(crni, beli)
            
        











            
        
if __name__ == "__main__":
    
    root = tkinter.Tk()
    root.title("Reversi")
    aplikacija = Gui(root)
    root.mainloop()













        


        
