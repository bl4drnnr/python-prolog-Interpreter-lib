import pcre
ARGUMENTS_REGEX = r"(?=(\(((?:(?-2)|[^()]+)+)\)))\("
DETIRM = [',', ';']
a = 'lot(a2324,warszawa,1800,1845(1,1,1,1,5,1,1),dni(1,1,1,1,1,1,1))'

data = pcre.findall(ARGUMENTS_REGEX, a)
filtered_data = [i[1] for i in data]
all_predicates = filtered_data[0]
res = {}

for i in filtered_data[1:]:
    index = a.find(i)
    predicates_list = a[:index].split('(')[:-1][-1]

    found_predicate = ''
    for sym in predicates_list[::-1]:
        if sym in DETIRM:
            break
        found_predicate += sym

    res[found_predicate[::-1]] = i

predicate = ''
for i in all_predicates:
    if i in DETIRM and '(' not in predicate and ')' not in predicate:
        if predicate not in res:
            res[predicate] = None
            predicate = ''
            continue
    if '(' in predicate and ')' in predicate:
        predicate = ''
    predicate += i

print(res)

