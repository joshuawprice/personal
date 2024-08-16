# Exam answers

:::note

Question 12 does not have an answer worth full marks.

:::

## Part A: Algorithmic (50 marks)

### Section 1: Mystery Sorting (25 marks)

1. There exist problems where ordering the data can make the problem easier to solve.

2. 
	```
	array = [7,8,2,4,9,1,3,5,6]
	n = 6  
	
	FIRST ITERATION  
	temp = 7
	array[start] = array[n] = 1
	array[6] = 7
	start = 2 n = 5  
	array = [1,8,2,4,9,7,3,5,6]  
	
	SECOND ITERATION  
	temp = 8
	array[2] = array[5] = 9
	array[5] = 8
	start = 3
	n = 4  
	array = 1,9,2,4,8,7,3,5,6  
	
	THIRD ITERATION  
	temp = 2
	array[3] = array[4] = 4
	array[4] = 2
	start = 4
	n = 3  
	array = 1,9,4,2,8,7,3,5,6
	```

3. To reverse the order of the first `n` values in the array.

4. 
    | Prompts                             | Submitted Answers |
    | ----------------------------------- | ----------------- |
    | Space complexity (as a word)        | Constant          |
    | Time complexity (as bit-O notation) | $\mathcal{O}(n)$  |
5. $\mathcal{O}(k)$

6. `i = n`

7. `j = 1`

8. `max = j`

9. `max`

10. The part of the array on the right of the index `i` is already sorted and all values are greater than `array[max]`

11. - Insertion Sort (best case)
	- Quick Sort (best case)
	- Merge Sort
12. **1.5/2 marks**

    At iteration `n-i`, the sorted list contains the n-i largest numbers in the correct order

13. In-place = no copy of the original array or part of it is done; Stable = two equal values are sorted in the same order as in the original array

14. The purpose of divide and conquer algorithms is to divide a problem into many sub-problems and solve each of those before combining them to find the solution to the original problem.

	The key difference between quick sort and merge sort in this regard, is that the first step of the merge sort (which is to take an array and split it into two halves recursively, until only arrays of size 1 are left) is very easy, and the final step of merge sort (putting the sorted arrays back together while keeping the newly combined arrays sorted) is the hard part.
	
	Quick sort has the opposite approach, where the easy part is at the end, since arrays are sorted in a way such that you only need to concatenate the smaller arrays to ensure that the combined one will be sorted correctly. To do this, you need to ensure that one of the split arrays contains the lowest values in the array, and the other the highest. This is much more difficult than merge sort's approach, which simply splits the arrays into halves.

### Section 2: Palindrome Detection and Generation (25 marks)

15. 
    ```
    Algorithm isPalindrome(word, n) {
		i = 1
		while (i <= n/2 and word[i] == word[n-i+1]) do {
			i = i + 1
		}
		return i > n/2
	```

16. 
	| Prompts                   | Submitted Answers |
	| ------------------------- | ----------------- |
	| Space (in big-O notation) | $\mathcal{O}(1)$   |
	| Time (as a word)          | Linear                  |

17. Yes, any algorithm can be designed either recursively or iteratively

18. `isPalindrome(word, i+1, n-1)`

19. 
	| Prompts             | Submitted Answers                |
	| ------------------- | -------------------------------- |
	| recurrence relation | $T(n) = T(n-1) + \mathcal{O}(1)$ |
	| complexity          | $\mathcal{O}(n)$                              |

20. Yes, because you might need to use some parameters to store results

21. Input a sentence instead of a word into the word parameter, we should also rename the word parameter to sentence. Then in the while loop, make sure that it matches the same if only the case is different, and skip over the punctuation by having extra while loops for both sides of the string.

22. Yes

23. It's still just going to be looping over the same data (the string, once), just with a few extra statements.

24. The algorithm would not have a constant space complexity, as the algorithm would be creating an array to store the sentence in. So the space complexity would to $\mathcal{O}(n)$ where $n$ is the length of the sentence. 


## Part B: Artificial Intelligence (40 marks)

25. A solution is a sequence of actions which go from the initial state to the goal state. If a search strategy is complete, then it is guaranteed to find a solution. An optimal solution is one with the lowest path cost of all solutions.
26. 
	1. Initial State: An empty ingredients list
	2. The actions available to the agent are to add an ingredient to the ingredients list, or remove an ingredient currently in the ingredients list
	3. The transition model is the new ingredient list, formed from the previous ingredient list and the new ingredient, or minus the one that was removed
	4. The goal test is whether or not the ingredient list matches any recipes in the recipe database
	5. The path cost function is the sum of time taken by each ingredient on the ingredient list (if you have broccoli with time 1 and spinach with time 2 the path cost is 3)

27. 
    | Prompts       | Submitted Answers                                                                                                                                                                           |
    | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Admissibility | The heuristic function never overestimates the cost to reach the goal.                                                                                                                      |
    | Monotonicity  | The estimated cost of reaching the goal from a node is never greater than the cost of getting from the node to a successor plus the estimated cost of reaching the goal from the successor. |

28. 
    - An evaluation function
    - A heuristic function

29. 
	- Iterative deepening depth-first search
	- Uniform-cost search
	- Depth-first search

30. None of the other choices

31. 
	| Prompts                  | Submitted Answers                         |
	| ------------------------ | ----------------------------------------- |
	| Greedy best-first search | $f(n) = h(n)$                             |
	| Uniform-cost search      | $f(n) = g(n)$                             |
	| Best-first search        | $f(n) = \text{any non-negative function}$ |
	| A* search                | $f(n) = h(n) + g(n)$                                          |
32. The choice of heuristic function

33. 
	| Prompts       | Submitted Answers                                                                                                   |
	| ------------- | ------------------------------------------------------------------------------------------------------------------- |
	| Admissibility | The heuristic for a node never overestimates the cost of reaching a goal from that node.                            |
	| Monotonicity  | The heuristic for a node is not greater than the cost of reaching a successor plus the heuristic for the successor. |

34. None of the above

35. True

36. N1

37. Large portions of the search space can be removed by removing states where the variable combinations violate the constraints.
38. 
	- A specification of the states in which the action is applicable
	- The effects of the action on the state
	- The action name
	- A list of variables

## Part C: Machine Learning & Deep Learning (10 marks)

39. The machine learns using labelled data

40. Some labelled data is combined with unlabelled data to give a larger training set

41. 0.8

42. 0.4

43. 
	- Neural networks learn from training data
	- Neural networks learn by iteratively adapting their weights
