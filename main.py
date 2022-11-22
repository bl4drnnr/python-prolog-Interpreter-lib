from src.ppil import KnowledgeDatabase


def main():
    db_payload = """
        lot(a2324, warszawa, 1800, 1845(1, 1, 1, 1, 5, 1, 1), dni(1, 1, 1, 1, 1, 1, 1)).
        lot(lf224, warszawa, rzeszow, 1850, 1930, dni(1, 1, 1, 1, 1, 1, 1)).
        lot(m232, warszawa, berlin, 1400, 1525, dni(1, 0, 1, 1, 0, 0, 1)).
        lot(a231, warszawa, monachium, 1420, 1600, dni(0, 1, 1, 0, 1, 1, 1)).
        lot(l324, warszawa, londyn, 1330, 1600, dni(1, 1, 1, 1, 1, 1, 1)).
        lot(a2324, krakow, warszawa, 700, 745, dni(1, 1, 1, 1, 1, 1, 1)).
        lot(lf224, rzeszow, warszawa, 850, 940, dni(1, 1, 1, 1, 1, 1, 1)).
        lot(m232, berlin, warszawa, 1600, 1725, dni(1, 0, 1, 1, 0, 0, 1)).
        lot(a231, monachium, warszawa, 1720, 1850, dni(0, 1, 1, 0, 1, 1, 1)).
        lot(l324, londyn, warszawa, 1720, 1940, dni(1, 1, 1, 1, 1, 1, 1)).
        przeloty_wtorek(A, B):- lot(_,A,B,_,_,dni(_,1,_,_,_,_,_)).
    """

    query = """
        przeloty_wtorek(rzeszow, X).
    """

    db = KnowledgeDatabase(db_payload)
    solution = db.find_solutions(query)
    print('solution', solution)


if __name__ == '__main__':
    main()
