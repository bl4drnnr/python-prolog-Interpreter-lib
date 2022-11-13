from ppil.pq import SearchQueue
from ppil.search_util import *


def answer_handler(answer):
    if len(answer) == 0:
        answer.append("No")
        return answer

    elif len(answer) > 1:
        if any(ans != "Yes" for ans in answer):
            answer = [i for i in answer if i != "Yes"]
        elif all(ans == "Yes" for ans in answer):
            return answer_handler([])

    return answer


def rule_query(knowledge_database, expr):
    answer = []
    start = Goal(Fact("start(search):-from(random_point)"))
    start.fact.rhs = [expr]
    queue = SearchQueue()
    queue.push(start)

    while not queue.empty:
        current_goal = queue.pop()
        if current_goal.ind >= len(current_goal.fact.rhs):
            if current_goal.parent is None:
                if current_goal.domain:
                    answer.append(current_goal.domain)
                else:
                    answer.append("Yes")
                continue
            
            child_to_parent(current_goal, queue)
            continue
        
        rule = current_goal.fact.rhs[current_goal.ind]
        
        if rule.predicate == "":
            prob_calc(current_goal, rule, queue)
            continue
        
        if rule.predicate == "neq":
            filter_eq(rule, current_goal, queue)
            continue
            
        elif rule.predicate in knowledge_database.db:
            rule_f = knowledge_database.db[rule.predicate]["facts"]
            if current_goal.parent is None:
                parent_inherits(rule, rule_f, current_goal, queue)
            else:
                child_assigned(rule, rule_f, current_goal, queue)
    
    answer = answer_handler(answer)

    return answer
