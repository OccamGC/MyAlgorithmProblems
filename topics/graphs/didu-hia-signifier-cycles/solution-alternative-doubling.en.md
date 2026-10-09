# Didu Hia's Signifier Cycles: Destinations Far Enough Ahead

Problem setter's solution: double the outgoing-edge map and count distinct destinations. Codex (GPT-6): choose rounds from the input size and replace sorting with vertex marks. [alternative-doubling.cpp](alternative-doubling.cpp) is a backup to [path tracking](solution.en.md) and passes all formal inputs.

Let $f(v)=d_v$ . Initially store $f(v)$ with a step count of one. While that count is less than $n$ , use a separate buffer to compute each destination's destination, swap arrays and double the step count. The final array represents $f^q(v)$ , where $q$ is a power of two at least $n$ . Count its distinct destination vertices.

After at least $n$ steps, any starting vertex has entered a cycle, so every destination lies on one. On each cycle, $f^q$ is a cyclic permutation; every cycle vertex is the destination of exactly one starting vertex on that cycle. Thus the image is exactly the set of all cycle vertices, and counting distinct destinations is correct.

Every round must read the old array throughout, using a separate buffer instead of overwriting entries in place. There are $O(\log(n+1))$ rounds, taking $O(n\log(n+1)+1)$ time and $O(n+1)$ space. ID-indexed Boolean marks count distinct destinations in linear time afterward. When $n=0$ , both loops are empty and the result is zero.

Doubling illustrates cycle detection through the image of a mapping and also extends to distant-successor queries. For counting cycle vertices alone, the linear algorithms have a better time bound.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
