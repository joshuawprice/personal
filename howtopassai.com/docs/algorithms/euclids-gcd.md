# Euclidean algorithm

## Complexity analysis

Iterative space complexity: $\mathcal{O}(1)$

Recursive best case space complexity: $\mathcal{O}(1)$

Recursive worst case space complexity: $\mathcal{O}(\log{n})$


## Pseudocode

Iterative implementation:

```
Algorithm gcd(m, n) {
    rem = m mod n;
    while(rem > 0) {
	    m = n;
		n = rem;
		rem = m mod n;
	}
	return n;
}
```

Recursive implementation:

```
Algorithm gcd(m, n) {
	rem = m mod n;
	if (rem = 0) {
		return n;
	else {
		return gcd(n, rem)
	}
}
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
