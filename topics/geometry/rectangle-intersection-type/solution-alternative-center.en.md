# Intersection Types: Center Distances

Problem setter's center-distance intersection method. Codex (GPT-6): a 64-bit C++17 implementation and positive-length conditions for degenerate intersection classification.

Program: [alternative-center.cpp](alternative-center.cpp). This parallel option supports the full data; see the [top-edge method](solution.en.md).

## One-dimensional result

For closed intervals $[l_A,r_A]$ and $[l_B,r_B]$ , let their lengths be $w_A=r_A-l_A$ and $w_B=r_B-l_B$ . Define twice the distance between their centers as

$$c=|l_A+r_A-l_B-r_B|$$

They intersect exactly when $c\le w_A+w_B$ . If their centers are $s_A,s_B$ , the intervals reach each other exactly when $|s_A-s_B|\le(w_A+w_B)/2$ . Multiplying by two proves the formula. Equivalently, expanding the two sides of the absolute-value inequality yields $l_A\le r_B$ and $l_B\le r_A$ .

A nonempty intersection has positive length exactly when $w_A>0$ , $w_B>0$ , and $c<w_A+w_B$ . For two positive-length intervals, equality means endpoint contact, while strict inequality gives overlap of positive length. If either interval is a point, their intersection cannot have positive length, so the width checks are necessary. For example, $[0,4]$ and $[2,2]$ have the same center but intersect only at a point.

## Two-dimensional algorithm and complexity

Apply the result independently on the horizontal and vertical axes. If either intersection is empty, the shapes are disjoint; otherwise they intersect. For classification, add the two positive-length indicators: $0,1,2$ give `Point` , `Edge` , and `Area` respectively.

Both the doubled center distance and the sum of lengths may reach $4\cdot10^9$ , beyond signed 32-bit range; use 64-bit integers. Each pair takes $O(1)$ time and $O(1)$ extra space, or $O(T+1)$ total time. This expresses the same geometry through centers and lengths, with additional degeneracy checks but no floating-point center coordinates.
