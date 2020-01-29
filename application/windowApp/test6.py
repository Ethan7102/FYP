def apply_f(fun):
	return fun(3, 2)

def sum(x, y):
	return x + y

def d(x,x2):
    return x-x2
sum_fun = sum
num = apply_f(sum)
print(num)
print(apply_f(d))