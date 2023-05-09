# Bubble sort

## Complexity analysis

1. Space complexity
    - $\mathcal{O}(1)$
2. Time complexity
    - $\mathcal{O}(n^2)$

## Pseudocode

```
Algorithm BubbleSort(a, n)

1: for i := n to 1 do
2:     for j := 1 to i - 1 do
3:         if a[j] > a[j + 1]
4:             t := a[j]; a[j] := a[j + 1]; a[j + 1] := t;
5: return a;
```
