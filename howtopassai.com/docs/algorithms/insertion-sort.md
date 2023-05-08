# Insertion sort

Iterates through the array, taking each element, comparing it to elements in the sorted subarray to its left, and inserting it in its correct position.

## Pseudocode

```
Algorithm InsertionSort(a,n)
1: for i:= 2 to n do {
2:     j := i;
3:     while j > 1 and a[j] < a[j-1] {
4:         t := a[j]; a[j] := a[j-1]; a[j-1] := t; // interchange a[j] and a[j-1]
5:         j := j-1;
6:     }
7: }
```