def diffWaysToCompute(input):
    self.formula = input
    self.memo = {}
    return self._diffWaysToCompute(0, len(input))

def _diffWaysToCompute(self, lo, hi):
    if self.formula[lo:hi].isdigit():
        return [int(self.formula[lo:hi])]
    if((lo, hi) in self.memo):
        return self.memo.get((lo, hi))
    ret = []
    for i, char in enumerate(self.formula[lo:hi]):
        if char in ['+', '-', '*']:
            leftResult = self._diffWaysToCompute(lo, i + lo)
            rightResult = self._diffWaysToCompute(lo + i + 1, hi)
            ret.extend([eval(str(i) + char + str(j)) for i in leftResult for j in rightResult])
            self.memo[(lo, hi)] = ret
    return ret

a=input()
print(diffWaysToCompute(a))