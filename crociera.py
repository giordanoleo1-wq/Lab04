import csv



class Crociera:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self.nome = nome
        self.cabine= []
        self.passeggeri= []
    def stampa_cabine_passeggeri(self):
        print(len(self.cabine))
        for cabina in self.cabine:
            print(cabina)


    class Cabina:
        def __init__(self, codice_cabina, posti_letto, num_ponte, prezzo):
            self.codice_cabina = codice_cabina
            self.posti_letto = posti_letto
            self.num_ponte = num_ponte
            self.prezzo_base = prezzo
            self.occupata = False
            self.passeggero= None

        def prezzo(self):
            return self.prezzo_base
        def __lt__(self, other):
            return self.prezzo() < other.prezzo()


        def __str__(self):
            return (f"{self.codice_cabina} | Standard | {self.posti_letto} letti, ponte: {self.num_ponte}, "
                    f"prezzo: {self.prezzo_base:.2f}€, {'Occupata' if self.occupata else 'Disponibile'}")

        def __repr__(self):
            return self.__str__()



    class CabinaDeluxe(Cabina):
        def __init__(self, codice_cabina, posti_letto, num_ponte, prezzo, tipologia):
            super().__init__( codice_cabina, posti_letto, num_ponte, prezzo)
            self.tipologia = tipologia
        def prezzo(self):
            return self.prezzo_base * 1.20
        def __str__(self):
            stato = "Disponibile" if not self.occupata else "Occupata"
            return (f"{self.codice_cabina} | Deluxe ({self.tipologia}) | {self.posti_letto} letti, "
                    f"ponte: {self.num_ponte}, prezzo: {self.prezzo():.2f}€, {stato}")


    class CabinaAnimali(Cabina):
        def __init__(self, codice_cabina, posti_letto, num_ponte, prezzo, num_max_animali):
            super().__init__(codice_cabina, posti_letto, num_ponte, prezzo)
            self.num_max_animali = num_max_animali
        def prezzo(self):
            return self.prezzo_base + (1+ 0.1 * self.num_max_animali)
        def __str__(self):
            stato = "Disponibile" if not self.occupata else "Occupata"
            return (f"{self.codice_cabina} | Animali (max {self.num_max_animali}) | {self.posti_letto} letti, "
                    f"ponte: {self.num_ponte}, prezzo: {self.prezzo():.2f}€, {stato}")

    class Passeggero:
        def __init__(self, codice_passeggero, nome, cognome):
            self.codice_passeggero = codice_passeggero
            self.__nome = nome
            self.__cognome = cognome

        def __str__(self):
            return f"nome: {self.__nome}, cognome: {self.__cognome}, ({self.codice_passeggero})"

        def __repr__(self):
            return self.__str__()

        """Aggiungere setter e getter se necessari"""

        # TODO
        @property
        def nome(self):
            return self.__nome

        @nome.setter
        def nome(self, nome):
            self.__nome = nome

        @property
        def cognome(self):
            return self.__cognome

        @cognome.setter
        def cognome(self, cognome):
            self.__cognome = cognome

    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        # TODO
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                lettore = csv.reader(csv_file)

                for riga in lettore:
                    if not riga:
                        continue
                    if riga[0].startswith("CAB"):
                        codice_cabina = riga[0]
                        posti_letto=int(riga[1])
                        num_ponte= int(riga[2])
                        prezzo= float(riga[3])
                        if len(riga)==4:
                            cab= self.Cabina(codice_cabina, posti_letto, num_ponte, prezzo)
                        elif len(riga)==5:
                            extra= riga[4]
                            try:
                                n_animali= int(extra)
                                cab= self.CabinaAnimali(codice_cabina, posti_letto, num_ponte, prezzo, n_animali)
                            except ValueError:
                                cab= self.CabinaDeluxe(codice_cabina, posti_letto, num_ponte, prezzo, extra)

                        else:
                            raise ValueError("Formato riga non corretto")

                        self.cabine.append(cab)

                    elif riga[0].startswith("P"):
                        codice_passeggero= riga[0]
                        nome= riga[1]
                        cognome= riga[2]
                        passeggero= self.Passeggero(codice_passeggero, nome, cognome)

                        self.passeggeri.append(passeggero)





        except FileNotFoundError:
            print("Errore: file non trovato")

    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        # TODO
        cabina= next ((c for c in self.cabine if c.codice_cabina==codice_cabina ), None)
        passeggero= next ((p for p in self.passeggeri if p.codice_passeggero== codice_passeggero), None)
        if cabina and passeggero and not cabina.occupata:
            cabina.occupata = True
            cabina.passeggero= passeggero
            print (f"Assegnato {passeggero} alla cabina {cabina}")
        else:
            print("Errore: cabina non trovata/occupata o passeggero inesistente")


    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        # TODO
        return sorted(self.cabine)

    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        # TODO
        for passeggero in self.passeggeri:
            cabina= next((c for c in self.cabine if c.passeggero == passeggero), None)
            if cabina:
                print(f"{passeggero} : {cabina}")
            else:
                print(f"Nessuna cabina assegnata a {passeggero} ")
