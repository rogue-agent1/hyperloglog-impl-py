"""HyperLogLog — cardinality estimation with O(1) space."""
import hashlib, math

class HyperLogLog:
    def __init__(self, p=14):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = 0.7213 / (1 + 1.079 / self.m)
    def add(self, item):
        h = int(hashlib.sha256(str(item).encode()).hexdigest(), 16)
        idx = h & (self.m - 1)
        w = h >> self.p
        self.registers[idx] = max(self.registers[idx], self._rho(w))
    def _rho(self, w):
        if w == 0: return 64 - self.p
        return (w & -w).bit_length()
    def count(self):
        Z = sum(2.0**(-r) for r in self.registers)
        E = self.alpha * self.m * self.m / Z
        if E <= 2.5 * self.m:
            V = self.registers.count(0)
            if V > 0: E = self.m * math.log(self.m / V)
        return int(E)

if __name__ == "__main__":
    hll = HyperLogLog(14)
    n = 100000
    for i in range(n): hll.add(f"item-{i}")
    est = hll.count()
    error = abs(est - n) / n
    print(f"True: {n}, Estimated: {est}, Error: {error:.4f}")
    assert error < 0.05
    print("All tests passed!")
