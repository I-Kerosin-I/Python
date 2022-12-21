from itertools import product


def solver(n1, n2, n3, n4):
    res = [
        f'{br[0]} {n1} {i[0]} {br[1]} {n2} {br[2]} {i[1]} {br[3]} {n3} {br[4]} {i[2]} {n4} {br[5]}' \
        for i in product('+-*/', repeat=3) for br in
        ('      ', '( )   ', '(   ) ', ' (  ) ', ' (   )', '   ( )')]
    print([i.replace(' ', '') for i in res if eval(i) == 10])


solver(1, 9, 5, 6)
