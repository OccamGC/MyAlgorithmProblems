# Factorio: Circuit Board Test — Safe Direct Evaluation

This follows the accompanying editorial's method of rejecting nonpositive or oversized inputs before evaluating the predicates. Codex (GPT-6) supplies an exact integer implementation in [alternative.cpp](alternative.cpp). It is a backup to [interval simplification](solution.en.md), preserving the predicate structure.

## Establish a safe range first

If $x\le0$ , predicate $p(x)$ is false. Reject immediately. For positive integers, $15^3=3375>3000$ , so $x\ge15$ makes $q(x)$ false and can also be rejected.

Only $1\le x\le14$ remains. Its square is at most $196$ and its cube at most $2744$ . Compute them safely in signed 64-bit arithmetic and check

$$x^3<3000\land x^2\ge10\land(x^2>2000\lor x^2<700)$$

## Correctness and complexity

Every early rejection violates a necessary predicate. Every remaining input is evaluated exactly against the defining conditions. The result is therefore precisely $P(x)$ .

Read inputs as signed 64-bit integers, and perform the range test before any multiplication. Each test takes $O(1)$ time; total time is $O(T+1)$ with $O(1)$ auxiliary space. Direct evaluation uses a few more constant operations than interval testing but closely follows the predicates. See the [main measurements](solution.en.md#measured-results).
