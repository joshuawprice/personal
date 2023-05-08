# Algorithms

## What is an algorithm?

An algorithm is a finite set of instructions that, if followed, accomplishes a particular task. In addition, all algorithms must satisfy the following criteria:
1. Input. Zero or more quantities are externally supplied.
2. Output. At least one quantity or result is produced.
3. Definiteness. Each instruction is clear and unambiguous.
4. Finiteness. If we trace out the instructions of an algorithm, then for all cases, the algorithm terminates after a finite number of steps.
 (Termination!)

We can also add “effectiveness”: every instruction must be basic enough and feasible. Ideally a person using only pencil and paper should be able to carry it out.

- Algorithms: always produce a correct result.
- Heuristics: may usually do a good job, but without providing any guarantee.

## Function growth

$$n! \gg 3^n \gg 2^n \gg n^3 \gg n^2 \gg n\log{n} \gg n \gg \log{n} \gg 1$$

<img src="/img/algorithms/big-o-functions.png" width="500px"/>

- The space complexity of an algorithm is the amount of memory it needs to run to completion.
- The time complexity of an algorithm is the amount of computer time it needs to run to completion.

## Space complexity

The space needed for the algorithms is seen to be the sum of the following components:
1. **A fixed space part** that does not depend on the characteristics of the algorithm inputs and outputs. This part includes instruction space (i.e. the space of the code, space for static variables and constants, etc.)
2. **A variable space part** consists of the size of the variables which depend on a particular problem instance being solved: the space needed by allocated and referenced variables, and the recursive stack space.

When analyzing the **space complexity** of an algorithm, we concentrate solely on estimating the variable part.

Any time memory is allocated dynamically, whether through manual allocation or by adding levels to the stack there is the possibility the space complexity of the algorithm will increase.

When given a choice between best or worst time complexity, usually the worst is more useful.

## Time complexity

