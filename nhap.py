class A:
    def __init__(self):
        self.val = 5
def add(x : A):
    x.val = 6

a = A()
add(a)
print(a.val) # OUTPUT = 6

