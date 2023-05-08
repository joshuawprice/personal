# Euclidean algorithm

The Euclidean algorithm is a recursive method to find the greatest common divisor (GCD) of two integers by repeatedly applying the modulo operation until the remainder becomes zero, at which point the GCD is the last non-zero remainder.


## Complexity analysis

1. Space complexity
    - Iterative: $\mathcal{O}(1)$
    - Recursive best case: $\mathcal{O}(1)$
    - Recursive worst case: $\mathcal{O}(\log{n})$
2. Time complexity
    - Best case: $\mathcal{O}(1)$
    - Worst case: $\mathcal{O}(\log{n})$


## Pseudocode

Iterative implementation:

```
Algorithm gcd(m, n)

1: rem = m % n
2: while rem > 0
3:     m = n
4:     n = rem
5:     rem = m % n
6: return n
```

Recursive implementation:

```
Algorithm gcd(m, n)

1: rem = m mod n
2: if rem == 0
3:     return n;
4: else
5:     return gcd(n, rem)
```


## Python

Iterative implementation:

```python
def it_gcd(m, n):
    if n > m:
        m, n = n, m

    while n != 0:
        m, n = n, m % n

    return m
```

Recursive implementation:

```python
def gcd(m, n):
    if n > m:
        m, n = n, m

    if n == 0:
        return m

    return gcd(n, m % n)
```


## Rust

Iterative implementation:

```rust
fn gcd(mut m: i32, mut n: i32) -> i32 {
    if n > m {
        (m, n) = (n, m);
    }

    while n != 0 {
        (m, n) = (n, m % n)
    }

    m
}
```

Recursive implementation:

```rust
fn gcd(mut m: i32, mut n: i32) -> i32 {
    // This algorithm only works if the m input is larger.
    if n > m {
        (m, n) = (n, m);
    }

    if n == 0 {
        return m;
    }

    gcd(n, m % n)
}
```


## C++

Recursive implementation:

```cpp
int gcd(int m, int n) {
    if (n > m) {
        int temp = m;
        m = n;
        n = temp;
    }

    if (n == 0) {
        return m;
    }

    return gcd(n, m % n);
}
```
