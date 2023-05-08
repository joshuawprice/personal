# Selection sort

Iterates finding the minimum (or maximum) element from the unsorted subarray and swapping it with the first unsorted element, thereby expanding the sorted subarray by one element at a time.

Loop invariant: the portion of the array considered so far is always sorted.

## Complexity analysis

1. Space complexity
    - $\mathcal{O}(1)$
2. Time complexity
    - $\mathcal{O}(n^2)$

## Pseudocode

```
Algorithm SelectionSort (a,n)

1: for i:= 1 to n-1 do {
2:     j := i;
3:     for k := i+1 to n do {
4:         if a[k] < a[j] then j := k;
5:     }
6:     t:=a[i]; a[i]:=a[j]; a[j]:=t;
7: }
```
