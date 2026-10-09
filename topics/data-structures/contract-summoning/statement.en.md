# Contract Summoning

- Indicative time limit: **1.0 seconds** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual limit: measure the reference solution on the target system, take the largest median time over test files, multiply by 2, and round up to a multiple of 0.5 seconds.
- Memory limit: **1024 MB**.

## Story

In the world of DNF, the summoner and every NPC have three attributes: strength, intelligence and spirit. Each NPC checks the attributes of the character calling it. An NPC that answers a call can then summon others. How many NPC types can ultimately be reached?

## Formal Problem Statement

You are given the initial summoner's attributes $(F,I,S)$ and $n$ NPC types. Type $i$ has requirements $(f_i,g_i,h_i)$ and its own attributes $(F_i,I_i,S_i)$ .

An available character can summon type $i$ if its strength, intelligence and spirit are at least $f_i,g_i,h_i$ , respectively. **One character** must satisfy all three requirements simultaneously.

Initially only the summoner is available. Summoning consumes no character and changes no attributes. A summoned NPC may subsequently summon other NPCs. Find the maximum number of NPC types that can eventually be summoned, counting each type once and excluding the initial summoner.

## Input Format

The first line contains $n,F,I,S$ .

Each of the next $n$ lines contains $f_i,g_i,h_i,F_i,I_i,S_i$ : the first three values are requirements, and the last three are the NPC's own attributes.

## Output Format

Output one integer: the number of NPC types that can be summoned.

## Sample 1

### Input

```text
3 2 3 5
1 2 4 4 2 2
3 2 3 3 4 3
4 1 1 5 2 3
```

### Output

```text
3
```

## Sample 2

### Input

```text
3 1 1 1
1 1 1 5 1 1
1 1 1 1 5 5
5 5 5 9 9 9
```

### Output

```text
2
```

## Sample 3

### Input

```text
3 0 0 0
0 0 0 1 1 1
1 1 1 2 2 2
2 2 2 0 0 0
```

### Output

```text
3
```

## Sample Explanation

In sample 1, the initial summoner can summon NPC 1, which can then summon NPC 3. No available character simultaneously meets all three requirements of NPC 2, so the answer is $2$ .

![The summoning chain in sample 1 runs from the summoner through NPC 1 to NPC 3](assets/summoning-chain.svg)

Each NPC box lists its requirement triple followed by its attribute triple; the starting box lists only its attributes.

In sample 2, attributes from two different NPCs cannot be combined, so type 3 remains unavailable. In sample 3, all three types can be summoned along a chain.

## Constraints and Guarantees

For all test cases: $1\le n\le100000$ . Every requirement and attribute is an integer between $0$ and $10^9$ , inclusive. Different NPC types may have identical requirements or attributes.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
