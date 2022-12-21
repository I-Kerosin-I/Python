from itertools import product, permutations


def solver(d1, d2, d3, d4):
    for n in permutations(f'{d1}{d2}{d3}{d4}'):
        res = [
            f'{br[0]} {n[0]} {i[0]} {br[1]} {n[1]} {br[2]} {i[1]} {br[3]} {n[2]} {br[4]} {i[2]} {n[3]} {br[5]}' \
            for i in product('+-*/', repeat=3) for br in
            ('      ', '( )   ', '(   ) ', ' (  ) ', ' (   )', '   ( )')]
        try:
            print([i.replace(' ', '') for i in res if eval(i) == 10])
        except ZeroDivisionError:
            print('ZeroDivision')

solver(4,1,2,8)
