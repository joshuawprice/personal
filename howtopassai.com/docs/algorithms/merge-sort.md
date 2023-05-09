# Merge sort

## Complexity analysis

### Merge sort

1. Space complexity
    - $\mathcal{O}(n)$
2. Time complexity
    - $\mathcal{O}(n\log{n})$

### Merge algorithm

1. Space complexity
    - If we allocate an array: $\mathcal{O}(n)$
    - If we don't allocate an array: $\mathcal{O}(1)$
2. Time complexity
    - $\mathcal{O}(n)$

## Pseudocode

### Merge sort

```
Algorithm MERGE-SORT(A, low, high)

1: if  low  <  high then               // Breaking condition.
2:     mid  := FLOOR[(low + high)/2]   // Divide step (array mid element)
3:     MERGE-SORT (A, low, mid)        // Solve first subproblem (sorting left half of A).
4:     MERGE-SORT (A,  mid  + 1, high) // Solve second subproblem (sorting right half of A).
5:     MERGE (A, low, mid, high)       // Conquer step (merging sorted halves)
```

### Merge algorithm

```
01: Algorithm MERGE(a, low, mid, high)
02:     k:= low; i:=low, j:=mid+1;

        // Fill array ‘b’ with minimum of first elements of each array until one is depleted.
03:     while ((k ≤ mid) and (j ≤ high)) do {
04:         if (a[k] ≤ a[j]) then {
05:             b[i] := a[k]; k := k+1;
06:         } else {
07:             b[i] := a[j]; j:= j+1; }
08:         i := i+1; }

        // Takes the remaining elements of the right array.
09:     if (k > mid) then {
10:         for h = j to high do {
11:             b[i] := a[h]; i :=i+1; }

        // Takes the remaining elements of the left array.
12:     } else {
13:         for h = k to mid do {
14:             b[i] := a[h]; i := i+1; } }

        // Copy the sorted and merged array ‘b’ back into final array ‘a’.
15:     for h := low to high do { a[h] := b[h]; }
```
