from .unify import unify
from ppil.prolog_elements.goal import Goal
from .util import prob_parser
from ppil.prolog_elements.fact import Fact


def parent_inherits(rl, rulef, currentgoal, Q):
    for f in range(len(rulef)):
        if len(rl.terms) != len(rulef[f].lh.terms):
            continue
        father = Goal(rulef[f], currentgoal)
        uni = unify(rulef[f].lh, rl,
                    father.domain,
                    currentgoal.domain)
        if uni:
            Q.push(father)


def child_assigned(rl, rulef, currentgoal, Q):
    if len(currentgoal.domain) == 0 or all(i not in currentgoal.domain for i in rl.terms):
        for f in range(len(rulef)):
            if len(rl.terms) != len(rulef[f].lh.terms):
                continue
            child = Goal(rulef[f], currentgoal)
            Q.push(child)
    else:
        key = currentgoal.domain.get(rl.terms[rl.index])
        if not key or rulef[0].rhs:
            first, last = (0, len(rulef))
        else:
            first, last = fact_binary_search(rulef, key)
        for f in range(first, last):
            if len(rl.terms) != len(rulef[f].lh.terms):
                continue
            child = Goal(rulef[f], currentgoal)
            uni = unify(rulef[f].lh, rl,
                        child.domain,
                        currentgoal.domain)
            if uni:
                Q.push(child)


def child_to_parent(child, Q):
    parent = child.parent.__copy__()
    unify(parent.fact.rhs[parent.ind],
          child.fact.lh,
          parent.domain,
          child.domain)
    parent.ind += 1
    Q.push(parent)


def prob_calc(currentgoal, rl, Q):
    key, value = prob_parser(currentgoal.domain, rl.to_string(), rl.terms)
    print('key', key)
    print('value', value)
    value = eval(value)
    if value:
        value = currentgoal.domain.get(key)
        if value is None:
            value = "Yes"
    elif not value:
        value = "No"
    currentgoal.domain[key] = value
    prob_child = Goal(Fact(rl.to_string()),
                      parent=currentgoal,
                      domain=currentgoal.domain)
    Q.push(prob_child)


def fact_binary_search(facts, key):
    right = 0
    length = len(facts)
    while right < length:
        middle = (right + length) // 2
        f = facts[middle]
        if key < f.lh.terms[f.lh.index]:
            length = middle
        else:
            right = middle + 1
    left = 0
    length = right - 1
    while left < length:
        middle = (left + length) // 2
        f = facts[middle]
        if key > f.lh.terms[f.lh.index]:
            left = middle + 1
        else:
            length = middle

    if left == right == 0:
        left, right = (0, len(facts))

    return left, right


def filter_eq(rule, currentgoal, Q):
    currentgoal.domain = {k: v for k, v in currentgoal.domain.items() if
                          currentgoal.domain[rule.terms[0]] != currentgoal.domain[rule.terms[1]]}

    prob_child = Goal(Fact(rule.to_string()),
                      parent=currentgoal,
                      domain=currentgoal.domain)
    Q.push(prob_child)
