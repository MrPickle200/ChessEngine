class A:
    def __init__(self):
        self.val = 5
def add(x : A):
    x.val = 6
    print(x.val)
    return x

a = A()
add(a)


