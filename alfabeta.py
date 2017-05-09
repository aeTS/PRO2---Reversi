import logging

from logika import (IGRALEC_B, IGRALEC_C, PRAZNO, KONEC, NI_KONEC, nasprotnik)

import random


######################################################################
## Algoritem alfa-beta rez

class Alfabeta:
    # Algoritem alfa-beta rez predstavimo z objektom, ki hrani stanje igre in
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
        """Izračuna potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo alfa-beta
        (poteza, vrednost) = self.alfabeta(self.globina, True, -Alfabeta.NESKONCNO, Alfabeta.NESKONCNO)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 1000000000
    NESKONCNO = ZMAGA + 1 # Več kot zmaga
    # Vrednost žetona, ki se mu barva ne bo več spremenila
    VREDNOST_PERMANENTNEGA = 100000 
    VREDNOST_MOZNE_POTEZE = 100

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije:
        1. prešteje, koliko je možnih potez
        oz. iz koliko polj lahko do njih pridemo,
        2. prešteje koliko kotov in zaporednih žetonov na robu,
        ki se držijo kotnega, imata igralec na potezi in njegov nasprotnik."""
        plosca = self.igra.plosca
        (stanje, crni, beli) = self.igra.stanje_igre()
        stevilo_moznih_potez = 0
        slovar_potez = self.igra.mozne_poteze()

        for elem in slovar_potez:
            stevilo_moznih_potez += len(elem) * Alfabeta.VREDNOST_MOZNE_POTEZE

        permanentni_jaz = set()
        permanentni_nasprotnik = set()
        if plosca[0][0] != PRAZNO:
            zeton = plosca[0][0]
            for k in range(0,8):
                if plosca[0][k] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[0][k] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((0, k))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((0, k))
            for k in range(0,8):
                if plosca[k][0] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[k][0] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((k, 0))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((k, 0))
                        
        if plosca[0][7] != PRAZNO:
            zeton = plosca[0][7]
            for k in range(0,8):
                if plosca[k][7] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[k][7] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((k, 7))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((k, 7))
            for k in range(7, 0, -1):
                if plosca[0][k] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[0][k] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((0, k))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((0, k))

        if plosca[7][7] != PRAZNO:
            zeton = plosca[7][7]
            for k in range(7, 0, -1):
                if plosca[k][7] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[k][7] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((k, 7))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((k, 7))
            for k in range(7, 0, -1):
                if plosca[7][k] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[7][k] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((7, k))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((7, k))
                        
        if plosca[7][0] != PRAZNO:
            zeton = plosca[7][0]
            for k in range(0, 7):
                if plosca[7][k] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[7][k] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((7, k))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((7, k))
            for k in range(7, 0, -1):
                if plosca[k][0] in [PRAZNO, nasprotnik(zeton)]:
                    break
                elif plosca[k][0] == zeton:
                    if zeton == self.jaz:
                        permanentni_jaz.add((k, 0))
                    elif zeton == nasprotnik(self.jaz):
                        permanentni_nasprotnik.add((k, 0))

        return (len(permanentni_jaz)*Alfabeta.VREDNOST_PERMANENTNEGA -
                len(permanentni_nasprotnik)* Alfabeta.VREDNOST_PERMANENTNEGA
                + stevilo_moznih_potez)


    def alfabeta(self, globina, maksimiziramo, alfa, beta):
        """Glavna metoda alfa-beta rez."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Alfa-beta prekinja, globina = {0}".format(globina))
            return (None, 0)
        (stanje, crni, beli) = self.igra.stanje_igre()
        if stanje == KONEC:
            # Igre je konec, vrnemo njeno vrednost
            if crni > beli and IGRALEC_C == self.jaz:
                return (None, Alfabeta.ZMAGA)
            elif crni < beli and IGRALEC_B == self.jaz:
                return (None, Alfabeta.ZMAGA)
            elif crni < beli and IGRALEC_C == self.jaz:
                return (None,-Alfabeta.ZMAGA)
            elif crni > beli and IGRALEC_B == self.jaz:
                return (None, -Alfabeta.ZMAGA)
            else:
                return (None, 0)

        elif stanje == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:

                # Naredimo eno stopnjo alfa-beta
                if maksimiziramo:
                    sez_najboljsih_potez = []
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Alfabeta.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            sez_najboljsih_potez = [p]
                            vrednost_najboljse = vrednost
                        elif vrednost == vrednost_najboljse:
                            sez_najboljsih_potez.append(p)
                            vrednost_najboljse = vrednost
                        alfa = max(alfa, vrednost_najboljse)
                        if beta <= alfa:
                            break
                    najboljsa_poteza = random.choice(sez_najboljsih_potez)


                else:
                    # Minimiziramo
                    sez_najboljsih_potez = []
                    najboljsa_poteza = None
                    vrednost_najboljse = Alfabeta.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            sez_najboljsih_potez = [p]
                            vrednost_najboljse = vrednost
                        elif vrednost == vrednost_najboljse:
                            sez_najboljsih_potez.append(p)
                            vrednost_najboljse = vrednost
                        beta = min(beta, vrednost_najboljse)
                        if beta <= alfa:
                            break
                    najboljsa_poteza = random.choice(sez_najboljsih_potez)

                assert (najboljsa_poteza is not None), "Alfa-beta: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "Alfa-beta: nedefinirano stanje igre"
