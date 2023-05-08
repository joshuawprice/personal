# Selection sort

Iterates finding the minimum (or maximum) element from the unsorted subarray and swapping it with the first unsorted element, thereby expanding the sorted subarray by one element at a time.

## Pseudocode

```
1. Algorithm SelectionSort (a,n)
2. // Sort the array a[1:n] in increasing order, assuming the left part of the array a[1:i]contains the i smallest numbers at the end of iteration i
3. for i:= 1 to n-1 do {
4.     j := i;
5.     for k := i+1 to n do {
6.         if a[k] < a[j] then j := k;
7.     }
8.     t:=a[i]; a[i]:=a[j]; a[j]:= t;
9. }
```
