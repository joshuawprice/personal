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


