from Deadlock import Deadlock

def main():
    response = int(input("Scegli l'algoritmo che vuoi usare per gestire il deadlock:\n"
                         "1) banchiere (deadlock prevention)\n"
                         "2) rilevamento del deadlock (deadlock detection)\n"))
    if response == 1:
        obj = Deadlock()
        obj.main_1()
    elif response == 2:
        obj = Deadlock()
        obj.main_2()
    else:
        print("Input non valido. Riprova")
        main()

if __name__ == "__main__":
    main()
