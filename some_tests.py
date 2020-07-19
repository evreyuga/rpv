def create_function(a, b, c):
    def new_f(v):
        return f"{a}{v}{b}{v}{c}"

    return new_f


x1, x2, x3 = 1, 2, 3

f = create_function(x1, x2, x3)
x1 = 4
print(f("*"))

def multipliers():
    def f(v):
        def f1(x):
            return x * v
        return f1
    return [f(i) for i in range(4)]

print([m(2) for m in multipliers()])

