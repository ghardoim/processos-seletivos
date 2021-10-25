## Does a list contain a triangular triplet?
### Introduction
Consider a zero-indexed list, A, that consists of N positive integers. A triplet (P, Q, R) is triangular on A if it is possible to build a triangle with sides of lengths A[P], A[Q], and A[R].

In other words, a triplet (P, Q, R) is triangular if:
```
0 ≤ P < Q < R < N
       and
A[P] + A[Q] > A[R]
A[Q] + A[R] > A[P]
A[R] + A[P] > A[Q]
```
## Task
### Write a function:

`def solution(a: List[int]) -> bool` that, given a zero-indexed list A consisting of N positive integers, returns True if A contains at least one triangular triplet and otherwise, returns False.

Example
- Given a list A such that the function should return True.
    - A[0] = 10; A[1] = 2; A[2] = 5; A[3] = 1; A[4] = 8; A[5] = 20;
    

-   While given a list A such that the function should return False.
    - A[0] = 10; A[1] = 50; A[2] = 5; A[3] = 1;
