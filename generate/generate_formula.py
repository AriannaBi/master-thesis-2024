import maude
import os.path
import numpy as np

maude.init(advise=True)
maude.load(os.path.join(os.path.dirname(__file__), 'maude/generate_formula.maude'))


m_generate = maude.getModule('gen_formula')
# print('Using', m_generate, 'module')
m_ap = maude.getModule('insert_ap')


t = m_generate.parseTerm('M')
pattern = m_generate.parseTerm('M')

with open('formulas.txt', 'w', newline='') as file:
    i = 0
    for sol, subs, path, nrew in t.search(type=maude.ANY_STEPS, target=pattern, depth=3):
        # if M is not in the solution, print it
        if (str(sol).find('M') == -1):
            i += 1
            # print(sol) 
            file.write(str(sol) + '\n')


print("Written file formulas.txt, Totale: ", nrew, "    Completed: ", i)

