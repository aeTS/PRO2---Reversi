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
        self.plosca[3][3] = IGRALEC_B
        self.plosca[3][4] = IGRALEC_C
        self.plosca[4][3] = IGRALEC_C
        self.plosca[4][4] = IGRALEC_B
        

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.plosca[i][:] for i in range(8)]
        self.zgodovina.append((p, self.na_potezi))

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        k = Logika()
        k.plosca = [self.plosca[i][:] for i in range(8)]
        k.na_potezi = self.na_potezi
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi) = self.zgodovina.pop()


    
    def mozne_poteze(self):
        poteze = {}
        igralec = self.na_potezi
        plosca = self.plosca

        for i in range(len(plosca)):
            for j in range(len(plosca[0])):
                if plosca[i][j] == igralec:
                    i1 = i
                    j1 = j
                    #DESNO
                    for elem in plosca[i][j+1:8]:
                        j1 += 1
                        if elem == igralec:
                            
                            break
                        elif elem == PRAZNO and j1 == j+1:
                            
                            break
                        elif elem == PRAZNO:
                            if (i, j1) not in poteze:
                                poteze[(i, j1)] = [(i, j)]
                            else:
                                poteze[(i, j1)].append((i, j))
                            break
                    j1 = j
                           
                        
                
                    #LEVO
                    for elem in plosca[i][0:j][::-1]:
                        j1 -= 1
                        if elem == igralec:
                            
                            break
                        elif elem == PRAZNO and j1 == j-1:
                        
                            break
                        elif elem == PRAZNO:
                            if (i, j1) not in poteze:
                                poteze[(i, j1)] = [(i, j)]
                            else:
                                poteze[(i, j1)].append((i, j))
                            break
                    j1 = j
                            
                    #DOL
                    for elem in plosca[i+1:8]:
                        i1 += 1
                        if elem[j] == igralec:
                            
                            break
                        elif elem[j] == PRAZNO and i1 == i+1:
                            
                            break
                        elif elem[j] == PRAZNO:
                            if (i1, j) not in poteze:
                                poteze[(i1, j)] = [(i, j)]
                            else:
                                poteze[(i1, j)].append((i, j))
                            break
                    i1 = i
                            
                        
                    #GOR
                    for elem in plosca[0:i][::-1]:
                        i1 -= 1
                        if elem[j] == igralec:
                            
                            break
                        elif elem[j] == PRAZNO and i1 == i-1:
                            
                            break
                        elif elem[j] == PRAZNO:
                            if (i1, j) not in poteze:
                                poteze[(i1, j)] = [(i, j)]
                            else:
                                poteze[(i1, j)].append((i, j))
                            break
                    i1 = i
                           
                    #DIAGONALNO DESNO GOR
                    for k in range(j+1,8):
                        
                        i1 += 1
                        if i1 < 8:
                            if plosca[i1][k] == igralec:
                                
                                break
                            elif plosca[i1][k] == PRAZNO and i1 == i+1:
                                
                                break
                            elif plosca[i1][k] == PRAZNO:
                                if (i1, k) not in poteze:
                                    poteze[(i1, k)] = [(i, j)]
                                else:
                                    poteze[(i1, k)].append((i, j))
                                break
                    i1 = i
                                
                            
                    #DIAGONALNO DESNO DOL
                    for k in range(j+1,8):
                        i1 -= 1
                        
                        if i1 >= 0:
                            print((i1, k))
                            if plosca[i1][k] == igralec:
                                
                                break
                            elif plosca[i1][k] == PRAZNO and i1 == i-1:
                                
                                break
                            elif plosca[i1][k] == PRAZNO:
                                if (i1, k) not in poteze:
                                    poteze[(i1, k)] = [(i, j)]
                                else:
                                    poteze[(i1, k)].append((i, j))
                                break
                            
                    i1 = i
                                
                    #DIAGONALNO LEVO GOR
                    for k in range(j - 1, -1, -1):
                        
                        i1 -= 1
                        if i1 >= 0:
                            if plosca[i1][k] == igralec:
                                
                                break
                            elif plosca[i1][k] == PRAZNO and i1 == i-1:
                                
                                break
                            elif plosca[i1][k] == PRAZNO:
                                if (i1, k) not in poteze:
                                    poteze[(i1, k)] = [(i, j)]
                                else:
                                    poteze[(i1, k)].append((i, j))
                                break
                    i1 = i
                               
                            
                    #DIAGONALNO LEVO DOL
                    for k in range(j - 1, -1, -1):
                        
                        i1 += 1
                        if i1 < 8:
                            if plosca[i1][k] == igralec:
                                
                                break
                            elif plosca[i1][k] == PRAZNO and i1 == i+1:
                                
                                break
                            elif plosca[i1][k] == PRAZNO:
                                if (i1, k) not in poteze:
                                    poteze[(i1, k)] = [(i, j)]
                                else:
                                    poteze[(i1, k)].append((i, j))
                                break
                    i1 = i
                                
                    

        return poteze
                    
        
        
        
    def povleci_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
        Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        (i,j) = p
        mozne_poteze = self.mozne_poteze()
        print(p, mozne_poteze)
        if p in mozne_poteze:
            self.shrani_pozicijo()
            self.plosca[i][j] = self.na_potezi
            for (i1, j1) in mozne_poteze[p]:
                #pobarva levo-desno-gor-dol
                if i == i1 and j < j1:
                    for k in range(j + 1, j1 + 1):
                        self.plosca[i][k] = self.na_potezi
                if i == i1 and j > j1:
                    for k in range(j1, j):
                        self.plosca[i][k] = self.na_potezi
                if j == j1 and i < i1:
                    for k in range(i + 1, i1 + 1):
                        self.plosca[k][j] = self.na_potezi
                if j == j1 and i > i1:
                    for k in range(i1, i):
                        self.plosca[k][j] = self.na_potezi
                #pobarva diagonalno
                st = j1
                if i > i1 and j < j1:
                    for k in range(i1 + 1, i):
                        st -= 1
                        self.plosca[k][st] = self.na_potezi
                    st = j1
                if i > i1 and j > j1:
                    for k in range(i1 + 1, i):
                        st += 1
                        self.plosca[k][st] = self.na_potezi
                    st = j1
                if i < i1 and j < j1:
                    for k in range(i1 - 1, i, -1):
                        st -= 1
                        self.plosca[k][st] = self.na_potezi
                    st = j1
                if i < i1 and j > j1:
                    for k in range(i1 - 1, i, -1):
                        st += 1
                        self.plosca[k][st] = self.na_potezi
                    st = j1
                
            
            (stanje, crni, beli) = self.stanje_igre()
            if stanje == NI_KONEC:
                self.na_potezi = nasprotnik(self.na_potezi)
            elif stanje == KONEC:
                self.na_potezi = None
            return (stanje, crni, beli)



    def stanje_igre(self):
        beli = 0
        crni = 0
        plosca = self.plosca

        for i in range(len(plosca)):
            for j in range(len(plosca[0])):
                if plosca[i][j] == IGRALEC_B:
                    beli += 1
                elif plosca[i][j] == IGRALEC_C:
                    crni += 1
        
        if self.mozne_poteze == {}:
            return (KONEC, crni, beli)
        else:
            return (NI_KONEC, crni, beli)
        
            



        
            






















    

















    
