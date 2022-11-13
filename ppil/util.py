import re

__all__ = ["is_number", "is_variable", "rh_val_get", "unifiable_check", "left_side_eval"]


def is_variable(term):
    if is_number(term):
        return False
    elif term <= "Z" or term == "_":
        return True
    else:
        return False
    

def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False        
        

def prob_parser(domain, rule_string, rule_terms):
    if "is" in rule_string:
        s = rule_string.split("is")
        key = s[0]
        value = s[1]
    else:
        key = list(domain.keys())[0]
        value = rule_string
    for i in rule_terms:
        if i in domain.keys():
            value = re.sub(i, str(domain[i]), value)
    value = re.sub(r"(and|or|in|not)", r" \g<0> ", value)
    return key, value


def rh_val_get(rh_arg, left_side_arg, rh_domain):
    if is_variable(rh_arg):
        rh_val = rh_domain.get(rh_arg)
    else: rh_val = rh_arg
    
    return rh_val
    

def unifiable_check(nterms, rh, left_side):
    if nterms != len(left_side.terms): 
        return False
    if rh.predicate != left_side.predicate: 
        return False
    

def left_side_eval(rh_val, left_side_arg, left_side_domain):
    if is_variable(left_side_arg):
        left_side_val = left_side_domain.get(left_side_arg)
        if not left_side_val: 
            left_side_domain[left_side_arg] = rh_val
        elif left_side_val != rh_val:
            return False          
    elif left_side_arg != rh_val: 
        return False

