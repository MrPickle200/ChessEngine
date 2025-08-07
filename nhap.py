class A:
    def __init__(self, val : int):
        self.val = val
    def __eq__(self, other):
        return isinstance(other, A) and self.val == other.val
    
l = [A(3), A(4), A(5)]
print(A(3) in l)


