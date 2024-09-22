import sys
class Deadlock:
    def __init__(self):
        self.procs_num, self.resources_num = self.procs_and_resources()

    def procs_and_resources(self):
        procs_num = int(input("Inserisci il numero di processi: "))
        resources_num = int(input("Inserisci il numero di risorse: "))
        return procs_num, resources_num
    
    def on_nested_list(self, procs_num, resources_num, X):  #riempe la nested list creata con mat()
        M = self.mat(procs_num, resources_num)
        print(f"Matrice {X}: \n")
        for i in range(procs_num):
            print("\n")
            for j in range(resources_num):
                M[i][j] = input(" ")
        return M
    
    def mat(self, m, n):  # crea una nested list di lunghezza m vuota
        list = []
        for i in range(m):
            list.append([])
            for j in range(n):
                list[i].append(0)
        return list # cre #crea una e #crea una
    
    def need(self, Max, Allocation, m, n): #crea la matrice Need
        need = self.mat(m, n)
        for i in range(m):
            for j in range(n):
                need[i][j] = Max[i][j] - Allocation[i][j]
        return need
    
    def total(self, All, Av, m, n): #crea il vettore Tot
        tot = []
        s = 0
        for j in range(n):
            for i in range(m):
                s += All[i][j]
            s += Av[j]
            tot.append(s)
            s = 0
        return tot
    
    def available(self, n, X): #crea la matrice Available
        Available = [0] * n
        print(f"Vettore {X}: ")
        for i in range(n):
            Available[i] = input(" ")
        return Available
    
    def on_create_1(self, m, n): #istanzio i dati iniziali
        Allocation = self.on_nested_list(m, n, "Allocation")
        Max = self.on_nested_list(m, n, "Max")
        Available = self.available(n, "Available")
        Need = self.need(Max, Allocation, m, n)
        Tot = self.total(Allocation, Available, m, n)
        print(f"Allocation:\n {Allocation}\n Max:\n {Max}\n Available:\n {Available}\n Need: {Need}\n Tot:\n{Tot}")
        return Allocation, Max, Available, Need, Tot
    
    def on_create_2(self, m, n):
        Allocation = self.on_nested_list(m, n, "Allocation")
        Request = self.on_nested_list(m, n, "Request")
        Available = self.available(n, "Available")
        print(f"Allocation:\n {Allocation}\n Request:\n {Request}\n Available:\n {Available}\n")
        Work = Available
        Finish = []
        # creo il vettore Finish
        c = 0
        for i in range(m):
            for j in range(n):
                if Allocation[i][j] == 0:
                    c += 1
            if c == n:  # Allocation(i) è un vettore nullo
                Finish.append("T")
            else:
                Finish.append("F")
        return Allocation, Request, Work, Finish
    
    def is_admissible(self, need, max, tot, m, n): #controlla l'ammissibilità del sistema
        for i in range(m):
            for j in range(n):
                if need[i][j] < 0:
                    print("Sistema inammissibile.")
                    sys.exit(0)
        for p in range(m):
            for q in range(n):
                if max[p][q] > tot[q]:
                    print("Sistema inammissibile. ")
                    sys.exit(0)
            else:
                return True
            
    def request_1(self, n, need, av, all): #gestisce la richiesta di risorse nell'algoritmo del banchiere
        # k=1 richiesta ammissibile
        # k=0 richiesta non ammissibile
        r = [0] * n
        c = 0
        print("Vettore richiesta: ")
        for i in range(n):
            r[i] = int(input(" "))
        q = int(input("Inserisci il numero del processo che ha fatto richiesta: ")) - 1
        for j in range(n):
            if r[j] <= need[q][j] and r[j] <= av[j]:
                c += 1
        if c == n:
            print("Richiesta ammissibile!")
            k = 1
            for p in range(n):
                av[p] -= r[p]
            for l in range(n):
                all[q][l] += + r[l]
                need[q][l] -= r[l]
        else:
            print("Richiesta non ammissibile.")
            k = 0
        return k, av, all, need
    
    def request_2(self, resources_num, req):  #gestisce la richiesta di risorse nell'algoritmo di rilevamento del deadlock
        r = [0] * resources_num
        Req = req
        print("Inserisci il vettore richiesta: ")
        for i in range(resources_num):
            r[i] = int(input(" "))
        q = int(input("Inserisci il numero del processo che fa richiesta: ")) - 1
        for j in range(resources_num):
            Req[q][j] = r[j] + req[q][j]
        return Req
    
    def sequenza_sicura(self, All, Av, N, m, n):  # trova la sequenza sicura e l'evoluzione del vettore Available
        temp = [0] * m  # variabile temporanea utilizzata per tracciare i processi i cui need<=available
        temp2 = [0] * m  # seconda variabile temporanea usata nel caso in cui due o più processi hanno need<=available (len(temp) >1)
        n_temp = N  # variabile temporanea di need, che ha righe corrispondenti a processi già scelti marcate con "X"
        contatore = 0
        # q = indice del processo scelto. Esempio: q = 0, P1 scelto.
        print("Sequenza sicura ed evoluzione del vettore Available: \n")
        for s in range(m):
            for i in range(m):
                for j in range(n):
                    if (str(n_temp[i][j]) != "-999") and (n_temp[i][j] <= Av[j]):  # trovare un processo non ancora scelto t.c. need<=available
                        contatore += 1
                if contatore == n:  # significa che need(i) <= Available
                    temp[i] = i
                else:
                    temp[i] = -999
                contatore = 0
            if self.conteggio(temp) == 1:  # conteggio è una funzione che calcola il numero di valori diversi da zero in un vettore
                q = max(temp)
            else:  # conteggio(temp) > 1 ergo due o più processi i cui need<=available.
                for z in range(m):
                    if temp[z] != -999:
                        temp2[z] = sum(All[z])
                max_allocation = max(temp2)
                q = temp2.index(max_allocation)
            print(f"P{q+1}", end=" ")
            for i in range(n):
                Av[i] += All[q][i]
            for c in range(n):
                n_temp[q][c] = -999
            temp = [0] * m
            temp2 = [0] * m
            print(Av)
    def conteggio(self, v):
        n = 0
        for i in range(len(v)):
            if v[i] != -999:
                n += 1
        return n
    
    def vett(self, procs_num): #crea il vettore di tutti i processi del sistema, usato per identificare quali sono in stallo
        v = []
        for i in range(procs_num):
            v.append(i + 1)
        return v
    
    def detection(self, All, Req, Work, Finish, m, n):  # trova la sequenza sicura e l'evoluzione del vettore Work
        temp = [0] * m  # variabile temporanea utilizzata per tracciare i processi i cui need<=available
        temp2 = [0] * m  # seconda variabile temporanea usata nel caso in cui due o più processi hanno need<=available (len(temp) >1)
        req_temp = Req  # variabile temporanea di req, che ha righe corrispondenti a processi già scelti marcate con "-999"
        procs = []  # lista usata per tenere traccia dei processi scelti
        contatore = 0
        # q = indice del processo scelto. Esempio: q = 0, P1 scelto.
        for s in range(m):
            for i in range(m):
                for j in range(n):
                    if Finish[i] == "F" and req_temp[i][j] <= Work[j] and req_temp[i][j] != -999:  # trovare un processo non ancora scelto t.c. req<=work
                        contatore += 1
                    elif (Finish[i] == "F" and req_temp[i][j] > Work[j]) or req_temp[i][j] == -999:
                        temp[i] = -999
                if contatore == n:  # processo i è un candidato per entrare in sequenza sicura
                    temp[i] = i
                contatore = 0

            if self.conteggio(temp) == 0:  # stallo rilevato temp = -999 per ogni i
                v = self.vett(m)
                for element in v:
                    if element not in procs:
                        print(f"P{element} ", end=" ")
                print("sono in stallo")
                sys.exit(0)

            elif self.conteggio(temp) == 1:  # conteggio è una funzione che calcola il numero di valori diversi da -999 in un vettore
                q = max(temp)
                procs.append(q+1)

            elif self.conteggio(temp) > 1:  # ergo due o più processi i cui req<=work.
                for z in range(m):
                    if temp[z] != -999:
                        temp2[z] = sum(All[z])
                    else:  # temp[z] = -999
                        temp2[z] = -999
                max_allocation = max(temp2)
                q = temp2.index(max_allocation)
                procs.append(q+1)

            for i in range(n):
                Work[i] += All[q][i]
            Finish[q] = "T"

            for c in range(n):
                req_temp[q][c] = -999  # in questo modo traccio i processi già scelti, che hanno req(i) = -999
            temp = [0] * m
            temp2 = [0] * m
        # output sequenza sicura
        print("Sequenza sicura: ")
        for t in range(m):
            print(f"P{procs[t]} ", end=" ")
            print(Work)

    def handle_request_1(self, Allocation, Available, Need):
        response = input("C'è un'ulteriore richiesta di risorse? y/n")
        if response == "n":
            print("Sistema ammissibile. ", end=" ")
            self.sequenza_sicura(Allocation, Available, Need, self.procs_num, self.resources_num)
        elif response == "y":
            [k, Available, Allocation, Need] = self.request_1(self.resources_num, Need, Available, Allocation)
            if k == 1:
                self.sequenza_sicura(Allocation, Available, Need, self.procs_num, self.resources_num)
            else:
                print("La richiesta di risorse porta il sistema in uno stato non sicuro.")
        else:
            print("Devi premere y o n!")
            self.handle_request_1(Allocation, Available, Need)

    def handle_request_2(self, Allocation, Request, Work, Finish):
        response = input("C'è un'ulteriore richiesta di risorse = y/n")
        if response == "n":
            self.detection(Allocation, Request, Work, Finish, self.procs_num, self.resources_num)
        elif response == "y":
            Req = self.request_2(self.resources_num, Request)
            self.detection(Allocation, Req, Work, Finish, self.procs_num, self.resources_num)
        else:
            print("Devi premere y o n!")
            self.handle_request_2(Allocation, Request, Work, Finish)

    def main_1(self):
        [Allocation, Max, Available, Need, Tot] = self.on_create_1(self.procs_num, self.resources_num)
        if self.is_admissible(Need, Max, Tot, self.procs_num, self.resources_num):
            self.handle_request_1(Allocation, Available, Need)
            
    def main_2(self):
        [Allocation, Request, Work, Finish] = self.on_create_2(self.procs_num, self.resources_num)
        self.handle_request_2(Allocation, Request, Work, Finish)

