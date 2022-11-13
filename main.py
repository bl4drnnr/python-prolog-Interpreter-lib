import ppil


def main():
    db_playload1 = [
        "osoba(michal, aleh, larysa, m, 19)",
        "osoba(aleh, wlodzimierz, ania, m, 56)",
        "osoba(larysa, andrzej, ola, f, 45)",
        "osoba(maciej, andrzej, ola, m, 48)",
        "osoba(andrzej, person1, person2, m, 82)",
        "osoba(ola, person3, person4, f, 75)",
        "osoba(wlodzimierz, person5, person6, m, 81)",
        "osoba(ania, person7, person8, f, 77)",
        "matka(X, Y) :- osoba(X, _, _, _, _), osoba(Y, _, W, _, L), W = X",
        # "ojciec(X, Y):-osoba(X, _, _, _, E), osoba(Y, W, _, _, L), W = X, M1 is L + 14, E >= M1",
        # "brat(X, Y):-osoba(X,B,C,D,_), osoba(Y,P,M,_,_), B=P, C=M, D = m, X\=Y",
        # "siostra(X, Y):-osoba(X,Q,W,E,_), osoba(Y,A,B,_,_), Q=A, W=B, E = f, X\=Y",
        # "babcia(X, Y):-(((matka(A, Y), matka(X, B)); (matka(X, A), ojciec(B, Y))), A = B)",
        # "dziadek(X, Y):-(((ojciec(A, Y), ojciec(X, B)); (ojciec(X, A), matka(B, Y))), A = B)"
    ]

    ancestors_db = ppil.KnowledgeDatabase("my db")
    ancestors_db(db_playload1)

    assert ancestors_db.query(ppil.Expression("osoba(michal, aleh, larysa, m, 19)")) == ["Yes"]

    # answer = {"What": "michal"}
    # query = ancestors_db.query(ppil.Expression("matka(larysa, What)"))
    # print('query', query)
    # assert answer in query


if __name__ == '__main__':
    main()
