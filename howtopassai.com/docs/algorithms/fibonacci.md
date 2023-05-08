# Fibonacci sequence

## Complexity analysis

Iterative space complexity: $\mathcal{O}(1)$

Recursive space complexity: $\mathcal{O}(n)$


## Pseudocode

Iterative implementation:

```
Algorithm fib(int n) // Compute the n-th Fibonacci number.
1: int u := 0;
2: int v := 1;
3: for i = 2 to n do   
4:     t := u + v;
5:     u := v;
6:     v := t;
7: end do
8: return v;
```

Recursive implementation:

```
Algorithm recfib(int n) // Compute the n-th Fibonacci number.
1: if n <= 1
2:     return n;
3: else
4:     return recfib(n-1) + recfib(n-2);
```
