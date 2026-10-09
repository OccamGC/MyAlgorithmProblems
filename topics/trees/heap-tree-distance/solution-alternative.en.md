# Infinite Binary Tree Distances: Align Depths

Problem setter's solution from the teaching notes. Codex (GPT-6): integer depth computation and a complete proof. [alternative.cpp](alternative.cpp) supplements [larger-label ascent](solution.en.md) and passes all formal inputs.

Compute a vertex's depth by repeatedly dividing its label by two until reaching the root. First move the deeper endpoint up until depths match, adding the depth difference. Then move both endpoints to their parents in each round, adding two, until they coincide.

The lowest common ancestor is no deeper than either endpoint, so depth alignment cannot cross it. At equal depths, distinct endpoints have a strictly shallower lowest common ancestor, and both parent steps follow the shortest path. Their meeting point is exactly that ancestor; the accumulated steps are therefore correct.

Let $U$ be the largest label and $H=\lfloor\log_2U\rfloor$ . Depth computation and ascent each take $O(H+1)$ time. Extra space per query is $O(1)$ , and total time is $O(m(H+1))$ . All calculations use integers. Equal endpoints, ancestor–descendant pairs and the root need no special structural cases.

This method explicitly separates alignment from simultaneous ascent. Comparing labels directly avoids the depth pass. Both use constant storage in this problem.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
