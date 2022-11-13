from .util import *


def unify(lh, rh, lh_domain=None, rh_domain=None):
    if rh_domain is None:
        rh_domain = {}
    if lh_domain is None:
        lh_domain = {}

    nterms = len(rh.terms)
    if unifiable_check(nterms, rh, lh) == False:
        return False

    for i in range(nterms):
        rh_arg = rh.terms[i]
        lh_arg = lh.terms[i]

        if lh_arg == "_":
            continue

        rh_val = rh_val_get(rh_arg, lh_arg, rh_domain)

        if rh_val:
            if lh_eval(rh_val, lh_arg, lh_domain) == False:
                return False

    return True
