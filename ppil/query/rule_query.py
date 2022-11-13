def get_answer(answer):
    if len(answer) == 0:
        answer.append("No")
        return answer

    elif len(answer) > 1:
        if any(ans != "Yes" for ans in answer):
            answer = [i for i in answer if i != "Yes"]
        elif all(ans == "Yes" for ans in answer):
            return get_answer([])

    return answer


def rule_query(knowledge_database, expr):
    database = knowledge_database.db
    predicate = database[expr.predicate]

    # print('predicate', predicate)
    # print('--------------------')
    # for i in predicate['facts']:
    #     print('terms', i.terms)
    #     print('fact', i.fact)
    #     print('left_side', i.left_side.to_string())
    #
    #     for t in i.right_side:
    #         print(t.to_string())
