import logging

from logika import (IGRALEC_B, IGRALEC_C, PRAZNO, KONEC, NI_KONEC, nasprotnik)

import random


######################################################################
## Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True, -Minimax.NESKONCNO, Minimax.NESKONCNO)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1 # Več kot zmaga
    VREDNOST_KOTA = 10000
    VREDNOST_ROBNE = 1000
    VREDNOST_MOZNE_POTEZE = 100

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        robni_jaz = 0
        robni_nasprotnik = 0
        plosca = self.igra.plosca
        koti_jaz = Minimax.VREDNOST_KOTA * [plosca[0][0], plosca[0][7], plosca[7][0], plosca[7][7]].count(self.jaz)
        koti_nasprotnik = -Minimax.VREDNOST_KOTA * [plosca[0][0], plosca[0][7],
                                                    plosca[7][0], plosca[7][7]].count(nasprotnik(self.jaz))
        (stanje, crni, beli) = self.igra.stanje_igre()
        stevilo_moznih_potez = 0
        slovar_potez = self.igra.mozne_poteze()

        for elem in slovar_potez:
            stevilo_moznih_potez += len(elem) * Minimax.VREDNOST_MOZNE_POTEZE

        for k in range(1, 7):
            for j in [0,7]:
                if plosca[j][k] == self.jaz:
                    robni_jaz += Minimax.VREDNOST_ROBNE
                elif plosca[k][j] == self.jaz:
                    robni_jaz += Minimax.VREDNOST_ROBNE
                elif plosca[j][k] == nasprotnik(self.jaz):
                    robni_nasprotnik -= Minimax.VREDNOST_ROBNE
                elif plosca[k][j] == nasprotnik(self.jaz):
                    robni_nasprotnik -= Minimax.VREDNOST_ROBNE



        return (robni_jaz + robni_nasprotnik + koti_jaz +
                koti_nasprotnik + stevilo_moznih_potez)


    def minimax(self, globina, maksimiziramo, alfa, beta):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        (stanje, crni, beli) = self.igra.stanje_igre()
        if stanje == KONEC:
            # Igre je konec, vrnemo njeno vrednost
            if crni > beli and IGRALEC_C == self.jaz:
                return (None, Minimax.ZMAGA)
            elif crni < beli and IGRALEC_B == self.jaz:
                return (None, Minimax.ZMAGA)
            elif crni < beli and IGRALEC_C == self.jaz:
                return (None,-Minimax.ZMAGA)
            elif crni > beli and IGRALEC_B == self.jaz:
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)

        elif stanje == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:

                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    sez_najboljsih_potez = []
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi()
                        if vrednost >= vrednost_najboljse:
                            sez_najboljsih_potez.append(p)
                        alfa = max(alfa, vrednost_najboljse)
                        if beta <= alfa:
                            break
                    najboljsa_poteza = random.choice(sez_najboljsih_potez)


                else:
                    # Minimiziramo
                    sez_najboljsih_potez = []
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi()
                        if vrednost <= vrednost_najboljse:
                            sez_najboljsih_potez.append(p)
                        beta = min(beta, vrednost_najboljse)
                        if beta <= alfa:
                            break
                    najboljsa_poteza = random.choice(sez_najboljsih_potez)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
