IGRALEC_B = "B"
IGRALEC_C = "C"
PRAZNO = "."
KONEC = "konec igre"
NI_KONEC = "ni konec"


def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_B:
        return IGRALEC_C
    elif igralec == IGRALEC_C:
        return IGRALEC_B
    else:
        assert False, "neveljaven nasprotnik"

class Logika():
    def __init__(self):
        self.plosca = [8*[PRAZNO] for _ in range(8)]
        self.na_potezi = IGRALEC_C
        self.zgodovina = []

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.plosca[i][:] for i in range(8)]
        self.zgodovina.append((p, self.na_potezi))

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        k = Igra()
        k.plosca = [self.plosca[i][:] for i in range(8)]
        k.na_potezi = self.na_potezi
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi) = self.zgodovina.pop()


    
    def mozne_poteze(self):
        poteze = {}
        igralec = self.na_potezi
        plosca = self.plosca()

        for i in range(len(plosca)):
            for j in range(len(plosca[0])):
                if plosca[i][j] == igralec:
                    i1 = i
                    i2 = i
                    j1 = j
                    j2 = j
                    for elem in plosca[i][j+1:8]:
                        j1 += 1
                        if elem == igralec:
                            break
                        elif elem == PRAZNO and j1 == j+1:
                            break
                        elif elem == PRAZNO:
                            poteze[(i, j1)] = (i, j)
                

                    for elem in plosca[i][0:j][::-1]:
                        j2 -= 1
                        if elem == igralec:
                            break
                        elif elem == PRAZNO and j2 == j-1:
                            break
                        elif elem == PRAZNO:
                            poteze[(i, j2)] = (i, j)

                    for elem in plosca[i+1:8][j]:
                        i1 += 1
                        if elem == igralec:
                            break
                        elif elem == PRAZNO and i1 == i+1:
                            break
                        elif elem == PRAZNO:
                            poteze[(i1, j)] = (i, j)
                        

                    for elem in plosca[0:i][j][::-1]:
                        i2 -= 1
                        if elem == igralec:
                            break
                        elif elem == PRAZNO and i2 == i-1:
                            break
                        elif elem == PRAZNO:
                            poteze[(i2, j)] = (i, j)

        return poteze
                    
        
        
        
    def povleci_potezo(self, p):
    """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        (i,j) = p
        if p in self.mozne_poteze:
            self.shrani_pozicijo()
            self.plosca[i][j] = self.na_potezi


            
            (stanje, črni, beli) = self.stanje_igre()
            if stanje == NI_KONEC:
                self.na_potezi = nasprotnik(self.na_potezi):
            else:
                self.na_potezi = None
            return (stanje, črni, beli)



    def stanje_igre(self):
        beli = 0
        črni = 0
        plosca = self.plosca()

        for i in range(len(plosca)):
            for j in range(len(plosca[0])):
                if plosca[i][j] == IGRALEC_B:
                    beli += 1
                elif plosca[i][j] == GRALEC_C:
                    črni += 1
        
        if len(self.mozne_poteze) == 0:
            return (KONEC, črni, beli)
        else:
            return (NI_KONEC, črni, beli)
        
            



        
            






















    

















    
