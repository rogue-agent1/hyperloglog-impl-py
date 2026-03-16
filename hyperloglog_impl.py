#!/usr/bin/env python3
"""HyperLogLog — cardinality estimation with O(1) space."""
import hashlib,math
class HyperLogLog:
    def __init__(self,p=14):
        self.p=p;self.m=1<<p;self.registers=[0]*self.m
        self.alpha={4:0.532,5:0.697,6:0.709}.get(p,0.7213/(1+1.079/self.m))
    def _hash(self,item):
        return int(hashlib.sha256(str(item).encode()).hexdigest(),16)
    def add(self,item):
        h=self._hash(item);idx=h&(self.m-1);w=h>>self.p
        self.registers[idx]=max(self.registers[idx],self._rho(w))
    def _rho(self,w):
        if w==0: return 64-self.p
        return (w&-w).bit_length()
    def count(self):
        Z=sum(2**-r for r in self.registers)
        E=self.alpha*self.m*self.m/Z
        if E<=2.5*self.m:
            V=self.registers.count(0)
            if V>0: E=self.m*math.log(self.m/V)
        return int(E)
def main():
    hll=HyperLogLog()
    for i in range(10000): hll.add(i)
    print(f"Estimated cardinality: {hll.count()} (actual: 10000)")
if __name__=="__main__":main()
