# Uniform-cost search (UCS)

- Like BFS, but instead of expanding the shallowest node, it expands the node n with the lowest path cost g(n).
- General graph-search algorithm in which the node with lowest path cost is chosen for expansion.
- This is done by storing the frontier as a priority queue ordered by g.

## Performance

- Complete: provided the cost of every step exceeds some small positive constant. It will get stuck if there is a path with an infinite sequence of zero-cost actions. 

- Optimal: uniform-cost search expands nodes in order of their optimal path cost. So, the first goal node selected for expansion will be the optimal solution. 

- Time and Space Complexity: let $C^∗$ be the cost of the optimal solution, and assume that every action costs at least $e$. Then the algorithm’s worst-case time and space complexity is $\mathcal{O}(b^{1+ \lfloor C^*/e\rfloor})$, which can be much greater than $b^d$. 

    When all step costs are equal, $b^{1+\lfloor C^*/e\rfloor}$ is just $b^{d+1}$.  
    
    When all step costs are the same, uniform-cost search is similar to BFS, but BFS stops as soon as it generates a goal, whereas uniform-cost search examines all the nodes at the goal’s depth to see if one has a lower cost. 
    
    Uniform-cost search does strictly more work by expanding nodes at depth d unnecessarily.
