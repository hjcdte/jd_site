from functools import reduce
l = range(1,5)

a = [{'name':'tom','age':'16'},{'name':'lilei','age':'18'}]

# print([[],] + a)
if({'name':'lilei','age':'18'} in a):
    print(1)

run_function = lambda x, y: x if y in x else x + [y]
uniqueList = reduce(run_function, [[], ] + a)

print(uniqueList)