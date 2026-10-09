# Solution

Contributions: the problem setter's solution supplies binary search, deadline counting, and priority-queue simulation. Codex (GPT-6) completed the proof, fixed feasibility boundaries and aggregate overflow, implemented the solutions, and supplied monotone buckets and verification.

## Charging jobs for a fixed power

Discard devices with $a_i\ge mb_i$ : they need no charging, including every device with $b_i=0$ .

Fix power $X$ . Before device $i$ receives its $j$-th charge, its total acquired energy is $E=a_i+(j-1)X$ . If $E\ge mb_i$ , it needs no more charges. Otherwise the next charge has deadline

$$d=\left\lfloor E/b_i\right\rfloor.$$

By the end of minute $d$ , consumption would be $(d+1)b_i>E$ , while earlier minute ends are safe. Treat this charge as a one-minute job with deadline $d$ . Jobs may be performed early because battery capacity is unlimited.

## The deadline prefix condition

Let `Deadlines[d]` count jobs with deadline exactly $d$ . Feasibility is equivalent to the following for every $t=0,\ldots,m-1$ :

$$\sum_{d=0}^{t}\mathrm{Deadlines}[d]\le t+1.$$

Necessity follows from the number of available minutes. For sufficiency, execute jobs in nondecreasing deadline order. If a job at position $s$ has deadline $d<s$ , more than $d+1$ jobs have deadlines at most $d$ , contradicting the condition. A device's successive deadlines are nondecreasing; break ties in charging order to respect its internal dependencies.

Enumerate each device's required jobs. Reject as soon as their total exceeds $m$ , so at most $m+1$ jobs are generated per check. Then scan deadline prefixes. This bound also terminates an infeasible check with $X=0$ . One check costs $O(n+m)$ .

## Binary search and safe arithmetic

Set

$$H=\max_i\max(0,mb_i-a_i).$$

If any power is feasible, $H$ is feasible: charging each deficient device once before its first failure supplies enough energy for the entire exam. A larger power cannot postpone that first required charge. Test $H$ explicitly; print $-1$ if it fails, otherwise binary-search $[0,H]$ . Increasing power preserves feasibility.

The feasibility check is required even when the search bounds coincide. For example, two devices starting at zero, each draining one unit per minute over two minutes, both require the minute-zero slot and are impossible to support.

Use signed 64-bit arithmetic for individual energies. Here $H\le5\cdot10^{14}$ , and enumeration stops upon reaching the target energy. Do not sum all devices' deficits into a 64-bit variable: the aggregate may overflow.

## Complexity and alternatives

For $n$ devices, $m$ minutes, and the bound $H$ above, time is $O((n+m)(1+\log(H+1)))$ and space is $O(n+m)$ . [std.cpp](std.cpp) uses the preferred deadline histogram.

The setter also describes a min-heap simulation: each minute, charge the device with the earliest next deadline and update its heap entry. One check takes $O(n+m\log(n+1))$ . Swapping jobs into earliest-deadline order transforms any feasible schedule into this greedy schedule. The [monotone bucket alternative](solution-alternative.en.md) uses integer deadlines from $0$ through $m-1$ to reduce simulation to $O(n+m)$ . It retains explicit minute-by-minute device choices, making a schedule easy to recover, and produces correct results on the full data. Its slowest median, about 0.738 seconds, exceeds the 0.5-second limit, so it is a backup when explicit scheduling is useful.

## Measurements

Each formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.226576 seconds and peak memory is 19.33 MiB. Twice the median, rounded up to 0.5 seconds, gives a 0.5-second limit. The alternative's slowest median is 0.737621 seconds and peak memory is 25.43 MiB. See the [environment](../../../docs/评测环境与性能.md) and [individual measurements](../../../docs/benchmark-R34.json). Recalibrate in other environments.
