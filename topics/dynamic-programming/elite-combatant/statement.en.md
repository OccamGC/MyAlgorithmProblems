# Elite Combatant

- Indicative time limit: 1.0 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

Boris and an iron dog are surrounded again. The dog can infiltrate the command center and disable every unit of one type, or increase Boris's health. His AKM will have to handle everything else.

The reconnaissance report lists combat troops, harmless production units, and a few peculiar enemies whose attacks actually heal Boris. Every enemy must go, but the order is up for discussion. “Enemy fire support” can occasionally be taken literally.

Find the greatest amount of health Boris can have after completing the mission.

## Formal Problem Statement

There are $K$ enemy types and $N$ individual enemies. Each unit of type $i$ starts with health $h_i$ and has attack value $a_i$ . A negative attack value heals Boris. Boris starts with health $H$ and deals attack damage $A$ per hit.

Before combat, the iron dog performs exactly one of these actions:

1. Remove every unit of one type without using a turn.
2. Increase Boris's health by $\Delta H$ , the health bonus supplied in the input.

While enemies remain, every turn consists of:

1. Boris attacks one living enemy. Remove that enemy immediately if its health becomes nonpositive.
2. All surviving enemies attack simultaneously. Subtract the sum of their attack values from Boris's health; a negative sum heals him.

Once Boris starts attacking a type with $a_i>0$ , he may attack only that type until it is eliminated; attacks against other types cannot be inserted in between. He may choose freely among its individual units. When no type is locked, he may attack any living enemy. Attacking a type with $a_i\le0$ does not create a lock.

Boris cannot skip his attack, attack a removed enemy, or continue after all enemies are eliminated. His health has no upper bound, but must be strictly positive after every turn; zero is fatal. Enemy attacks are resolved together, with no ordering within that phase.

Maximize his final health over all legal choices. If the mission is impossible, output `leave!` .

## Input Format

The first line contains five integers $K,N,H,A,\Delta H$ in order: the type count, total enemy count, Boris's initial health, damage per attack, and optional health bonus.

The next $K$ lines each contain a type name and integers $h_i,a_i$ . Names are UTF-8 encoded, case-sensitive, distinct, and contain no whitespace.

The following $N$ lines each contain the type name of one enemy. Every name appears in the type table. Some declared types may have zero actual units.

## Output Format

Output the maximum final health as a decimal integer, or `leave!` if the mission is impossible.

A valid answer may exceed the range of 64-bit integers.

## Sample 1

### Input

```text
2 3 100 50 100
YuriRecruit 20 30
GIGuard 80 10
YuriRecruit
YuriRecruit
GIGuard
```

### Output

```text
140
```

### Explanation

Choose extra health, starting at $200$ . Eliminate the two `YuriRecruit` units and then `GIGuard` , finishing with $140$ .

## Sample 2

### Input

```text
1 5 100 30 500
WarMiner 100 10
WarMiner
WarMiner
WarMiner
WarMiner
WarMiner
```

### Output

```text
100
```

### Explanation

Remove the entire miner type. Combat ends without a turn.

## Sample 3

### Input

```text
3 5 100 100 500
Rocketeer 500 20
PrismTank 200 100
SEAL 50 100
Rocketeer
Rocketeer
PrismTank
SEAL
SEAL
```

### Output

```text
leave!
```

### Explanation

No choice keeps Boris alive until every enemy is eliminated.

## Sample 4

### Input

```text
1 2 1 1 0
Medic 2 -10
Medic
Medic
```

### Output

```text
51
```

### Explanation

Hit each enemy once without eliminating either, gaining $40$ health in total. Eliminate them one at a time for another $10$ , finishing at $51$ .

## Constraints and Guarantees

- $1\le K\le5000$ and $1\le N\le50000$ .
- $1\le H\le10^9$ , $1\le A\le10^5$ , and $0\le\Delta H\le10^9$ .
- $1\le h_i\le10^5$ and $-10^5\le a_i\le10^5$ . At most $20$ declared types have positive attack.
- Each name has $1$ to $100$ UTF-8 bytes and contains no whitespace, including spaces, tabs, or newlines.
- All input values other than names are integers. Healing has no upper cap.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
