from .util import *


def unify(left_side, rh, left_side_domain=None, rh_domain=None):
    if rh_domain is None:
        rh_domain = {}
    if left_side_domain is None:
        left_side_domain = {}

    nterms = len(rh.terms)
    if unifiable_check(nterms, rh, left_side) == False:
        return False

    for i in range(nterms):
        rh_arg = rh.terms[i]
        left_side_arg = left_side.terms[i]

        if left_side_arg == "_":
            continue

        rh_val = rh_val_get(rh_arg, left_side_arg, rh_domain)

        if rh_val:
            if left_side_eval(rh_val, left_side_arg, left_side_domain) == False:
                return False

    return True
