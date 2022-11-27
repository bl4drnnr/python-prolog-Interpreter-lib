# Table of Contents

1. [Python PROLOG Interpreter Library](#python-prolog-interpreter-library)
2. [Installation and usage](#installation-and-example-of-usage)
   1. [Installation](#installation)
   2. [Example of library usage](#example-of-library-usage)
   3. [Example of API usage](#example-of-api-usage)
3. [Introduction to Prolog](#introduction-to-prolog)
   1. [Data types](#data-types)
   2. [Rules and facts](#rules-and-facts)
4. [Documentation](#documentation)
   1. [Usage of library](#usage-of-library)
   2. [Usage of API](#usage-of-api)
5. [References and contact](#references-and-contact)
6. [Licence](#license)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

---

## Python PROLOG Interpreter Library

**PPIL** - is a simple `Python` witten library, that allows to use `Prolog` syntax within `Python`.

Application is built from 3 different parts:
- **Interactive CLI**
- **Classical terminal-based application**
- `Python` library with interpreter and API instance

Right now, you are reading about `Python` library, if you want to find out more about _CLI's_, ses [this](https://github.com/bl4drnnr/python-prolog-interpreter-cli) repository.


---

## Installation and example of usage

### Installation

In order to install library, open up terminal in project folder and type:

```
pip install ppil
```

### Example of library usage

Here is example of usage and, at the same time, the way how you can test the program:

```python
from ppil import KnowledgeDatabase

ancestors_payload = """
   person(michael, john, ann, m, 19).
   person(john, jeff, jenny, m, 56).
   person(ann, andrew, ewa, f, 45).
   person(jordan, andrew, ewa, m, 48).
   person(andrew, person1, person2, m, 82).
   person(ewa, person3, person4, f, 75).
   person(jeff, person5, person6, m, 81).
   person(jenny, person7, person8, f, 77).
   mom(X, Y) : -person(X, _, _, _, E), person(Y, _, W, _, L), W = X, M1 is L + 14, E >= M1.
   father(X, Y) :- person(X, _, _, _, E), person(Y, W, _, _, L), W = X, M1 is L + 14, E >= M1.
   brother(X, Y) :- person(X,B,C,D,_), person(Y,P,M,_,_), B = P, C = M, D = m, X \= Y.
   sister(X, Y) :- person(X, Q, W, E, _), person(Y, A, B, _, _), Q = A, W = B, E = f, X \= Y.
   grandmother(X, Y) :- (((mom(A, Y), mom(X, B)); (mom(X, A), father(B, Y))), A = B).
   grandad(X, Y) :- (((father(A, Y), father(X, B)); (father(X, A), mom(B, Y))), A = B).
"""

query = """
        osoba(ania, person7, person8, f, 77).
"""

ancestors_db = ppil.KnowledgeDatabase(ancestors_payload)
solution = ancestors_db.find_solutions(query)
```

### Example of API usage

You can create API instance, that can receive `JSON` (format will be described later) or `Prolog` and
send it back transform in other format. Also, it allows you to compile code and get result in both formats.

```python
from ppil import ApiInstance

api = ApiInstance()
api.run(debug=True)
```

More about how it works, you can find below, in [Documentation](#documentation) section.

---

## Introduction to Prolog

A little introduction to **_Prolog_**.

In Prolog, program logic is expressed in terms of relations, and a computation is initiated by running a query over these relations. 
Relations and queries are constructed using Prolog's single data type, the term. Relations are defined by clauses. Given a query, the Prolog engine attempts to find a resolution refutation of the negated query. 
If the negated query can be refuted, i.e., an instantiation for all free variables is found that makes the union of clauses and the singleton set consisting of the negated query false, it follows that the original query, with the found instantiation applied, is a logical consequence of the program. 
This makes Prolog (and other logic programming languages) particularly useful for database, symbolic mathematics, and language parsing applications. Because Prolog allows impure predicates, checking the truth value of certain special predicates may have some deliberate side effect, such as printing a value to the screen. 
Because of this, the programmer is permitted to use some amount of conventional imperative programming when the logical paradigm is inconvenient. It has a purely logical subset, called "pure Prolog", as well as a number of extralogical features.

### Data types

Prolog's single data type is the term. Terms are either atoms, numbers, variables or compound terms.

- An **atom** is a general-purpose name with no inherent meaning. Examples of atoms include `x`, `red`, `Taco`, and `some atom`.
- **Numbers** can be floats or integers. ISO standard compatible Prolog systems can check the Prolog flag "bounded". Most of the major Prolog systems support arbitrary length integer numbers.
- **Variables** are denoted by a string consisting of letters, numbers and underscore characters, and beginning with an upper-case letter or underscore. Variables closely resemble variables in logic in that they are placeholders for arbitrary terms.
- A **compound term** is composed of an atom called a "functor" and a number of "arguments", which are again terms. Compound terms are ordinarily written as a functor followed by a comma-separated list of argument terms, which is contained in parentheses. The number of arguments is called the term's arity. An atom can be regarded as a compound term with arity zero. An example of a compound term is `person_friends(zelda,[tom,jim])`.

Special cases of compound terms:

- A _List_ is an ordered collection of terms. It is denoted by square brackets with the terms separated by commas, or in the case of the empty list, by `[]`. For example, `[1,2,3]` or `[red,green,blue]`.
- _Strings_: A sequence of characters surrounded by quotes is equivalent to either a list of (numeric) character codes, a list of characters (atoms of length 1), or an atom depending on the value of the Prolog flag `double_quotes`. For example, `to be, or not to be`.

### Rules and facts

Prolog programs describe relations, defined by means of clauses. Pure Prolog is restricted to **_Horn clauses_**. There are two types of clauses: facts and rules. A rule is of the form

```
Head :- Body.
```

and is read as "Head is true if Body is true". 
A rule's body consists of calls to predicates, which are called the rule's **goals**. 
The built-in logical operator `,/2` (meaning an arity 2 operator with name `,`) denotes conjunction of goals, and `;/2` denotes disjunction. Conjunctions and disjunctions can only appear in the body, not in the head of a rule.

Clauses with empty bodies are called facts. An example of a fact is:

```
cat(tom).
```

which is equivalent to the rule:

```
cat(tom) :- true.
```

The built-in predicate `true/0` is always true.

Given the above fact, one can ask:

_is tom a cat?_

```
? - cat(tom).
Yes
```

_what things are cats?_

```
? - cat(X).
X = tom
```

Clauses with bodies are called **rules**. An example of a rule is:

```
animal(X) :- cat(X).
```

If we add that rule and ask _what things are animals_?

```
? - animal(X).
X = tom
```

Due to the relational nature of many built-in predicates, they can typically be used in several directions. For example, `length/2` can be used to determine the length of a list (`length(List, L)`, given a list `List`) as well as to generate a list skeleton of a given length
(`length(X, 5)`), and also to generate both list skeletons and their lengths together (`length(X, L)`). Similarly, `append/3` can be used both to append two lists (`append(ListA, ListB, X)` given lists `ListA` and `ListB`) as well as to split a given list into
parts (`append(X, Y, List)`, given a list `List`). For this reason, a comparatively small set of library predicates suffices for many Prolog programs.

As a general purpose language, Prolog also provides various built-in predicates to perform routine activities like input/output, using graphics and otherwise communicating with the operating system. 
These predicates are not given a relational meaning and are only useful for the side-effects they exhibit on the system. For example, the predicate `write/1` displays a term on the screen.


---

## Documentation

### Usage of library

To start use `Prolog`, first of all, you need to import it in your code:

```python
import ppil
```

Then, using library, create object of `KnowledgeDatabase` and pass a payload to it.

```python
from ppil import KnowledgeDatabase

database_payload = """
    is_tall(jack, yes).
    is_tall(eric, no).
    is_tall(johnny, yes).
    is_tall(mark, no).
"""

goal = """
        is_tall(Y, yes)
"""

database = ppil.KnowledgeDatabase(KnowledgeDatabase)
solution = database.find_solutions(goal)
```

Now, you are free to go, use `.find_solutions` method in order to manipulate your database (referring to example above):

```python
assert len(solutions.get("Y")) == 2

assert ("jack" in str(solution) for solution in solutions.get("Y"))
assert ("johnny" in str(solution) for solution in solutions.get("Y"))
```

More examples and test you will find in the `tests` folder.

### Usage of API

---

## References and contact

- Developer contact - [mikhail.bahdashych@protonmail.com](mailto:mikhail.bahdashych@protonmail.com)
- [Prolog on wiki](https://en.wikipedia.org/wiki/Prolog) - Official english page of Prolog programming language on Wikipedia
- [Prolog website](https://www.swi-prolog.org/) - Official site and documentation of Prolog
- [Prolog. Programming W. F. Clocksin C. S. Mellish](https://www.amazon.com/Programming-Prolog-Using-ISO-Standard/dp/3540006788/ref=sr_1_1?crid=3SI3X3IWULTLU&keywords=Programming+in+Prolog&qid=1666038671&qu=eyJxc2MiOiIwLjU4IiwicXNhIjoiMC42NSIsInFzcCI6IjAuNzIifQ%3D%3D&s=books&sprefix=%2Cstripbooks-intl-ship%2C234&sr=1-1) - Prolog guidebook

---

## License

Licensed by [MIT License](LICENSE).
