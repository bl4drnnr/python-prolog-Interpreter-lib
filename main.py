from src.ppil import KnowledgeDatabase


def main():
    # osoba(michal, aleh, larysa, m, 19).
    # osoba(aleh, wlodzimierz, ania, m, 56).
    # osoba(larysa, andrzej, ola, f, 45).
    # osoba(maciej, andrzej, ola, m, 48).
    # osoba(andrzej, person1, person2, m, 82).
    # osoba(ola, person3, person4, f, 75).
    # osoba(wlodzimierz, person5, person6, m, 81).
    # osoba(ania, person7, person8, f, 773).
    # tests(X, Y):- osoba(X, Y, A, B, C), osoba(X, Y, G, D, E).
    # matka(X, Y):- osoba(X, A, B, C, E), osoba(Y, D, W, P, L), W = X, M1 is L + 14, E >= M1.
    # ojciec(X, Y):- osoba(X, _, _, _, E), osoba(Y, W, _, _, L), W = X, M1 is L + 14, E >= M1.
    # brat(X, Y):- osoba(X, B, C, D, _), osoba(Y, P, M, _, _), B = P, C = M, D = m, X\=Y.
    # siostra(X, Y):- osoba(X, Q, W, E, _), osoba(Y, A, B, _, _), Q = A, W = B, E = f, X\=Y.
    # babcia(X, Y):- (((matka(A, Y), matka(X, B)); (matka(X, A), ojciec(B, Y))), A = B).
    # dziadek(X, Y):- (((ojciec(A, Y), ojciec(X, B)); (ojciec(X, A), matka(B, Y))), A = B.

    db_playload1 = """
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
        lot(a231, monachium, warszawa, 1720, 1850, dni(1, 1, 1, 0, 1, 1, 1)).
    """

    db = KnowledgeDatabase(db_playload1)
    solution = db.find_solutions(query)
    print('solution', solution)


if __name__ == '__main__':
    main()
