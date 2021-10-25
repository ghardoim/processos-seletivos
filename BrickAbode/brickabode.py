def solution(A):
    for p, P in enumerate(A):
        for q in range(p + 1, len(A)):
            for r in range(p + 2, len(A)):
                if (P + A[q] > A[r]) and (A[q] + A[r] > P) and (A[r] + P > A[q]):
                    return True
    return False

print(solution([10, 2, 5, 1, 8, 20]))
print(solution([10, 50, 5, 1]))