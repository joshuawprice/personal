# Quick sort

Parition algorithm moves values to either side of a pivot, which can be chosen in a vartiety of ways, such as the first value in the array, a random value etc. (in the pseudocode we use the first value). Then does it again recursively until the array is of size 1, then we know everything is sorted.

Loop invariant of the partition algorithm: At the end of each iteration, the sub-array a\[m+1..i\] contains i values smaller than the pivot and the sub-array a[j..p] contains j values larger than the pivot.

Sorts in place. (No auxilary array required.)

Not stable with in-place sort.

## Complexity analysis

## Quick sort

1. Space complexity
    - 
2. Time complexity
    - Best case: $\mathcal{O}(n\log{n})$
    - Average case: $\mathcal{O}(n\log{n})$
    - Worst case: $\mathcal{O}(n^2)$

### Partition algorithm

1. Space complexity
    - $\mathcal{O}(1)$
2. Time complexity
    - $\mathcal{O}(n)$


## Pseudocode

### Quick sort

```
Algorithm quicksort(int[] array, int left, int right)

1: if (left < right) // Breaking condition
2:     int p = partition(array, left, right) // Divide step (difficult)
3:     quicksort(array, left, p - 1) // Conquer steps (easy)
4:     quicksort(array, p + 1, right)
```

### Partition algorithm

```
Algorithm Partition(a, int m, int p)

02 v := a[m]; i := m + 1; j := p
03 while (i < j) {

       // Starting from the left end, find the first element that is larger than or equal to the pivot (a[i] at the end of the loop)
04     while (a[i] < v and i < j) {
05         i := i + 1
06     }

       // Searching backward from the right end, find the first element that is smaller than the pivot (a[j] at the end of the loop)
07     while (a[j] >= v and j >= i) {
08         j := j - 1
09     }

       // Exchange (swap) these two elements so that they are in the right part of the array
10     if (i < j) {
11         t :=a[i]; a[i]:= a[j]; a[j] := t
12     }
13 }

   // Place the pivot at its final position (if not already there) and return this position
14 if ((m+1 < p and j > m) or (m+1 == p and a[j] < v)) {
15     a[m] := a[j]; a[j] := v;
16 }
17 return j