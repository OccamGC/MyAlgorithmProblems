# Alien Factory: Signal Network

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The deployed limit is twice the largest per-input median runtime of the reference program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [reference measurements](../../../docs/评测环境与性能.md).

## Story

A factory controls its power equipment through a signal network. To avoid repeated switching near a charge threshold, an engineer combines binary signals and packages rotations, interval flips and readout into reusable devices. Simulate one of these signal registers.

## Formal Problem Statement

Maintain an unsigned $128$-bit binary integer $A$ , initially zero. Number its bits $0,1,\ldots,127$ from least significant to most significant; bit $i$ has weight $2^i$ .

| Operation | Meaning |
| --- | --- |
| `1 x` | Rotate the whole register right by $x$ bits. A negative value means a left rotation by its absolute value. |
| `2` | Print the nonnegative integer represented by the lowest $16$ bits, in uppercase hexadecimal. |
| `3 l r` | Flip every bit whose index belongs to the closed interval $[l,r]$ . |

A rotation preserves the bits shifted out at one end and places them at the other end. Let $k$ be the nonnegative remainder of $x$ modulo $128$ . New bit $i$ equals old bit $(i+k)\bmod128$ . A rotation with $k=0$ changes nothing.

![An eight-bit right rotation by three moves the lowest three bits to the highest positions](assets/rotation.svg)

The diagram illustrates a right rotation by $3$ in an $8$-bit register: `00011101` becomes `10100011` . The actual problem always uses $128$ bits.

## Input

The first line contains the number of operations $N$ . Each of the next $N$ lines contains one operation in the format above.

## Output

For every `2` operation, print one hexadecimal number using digits `0` through `9` and uppercase letters `A` through `F` . Omit the `0x` prefix and unnecessary leading zeros. Print `0` for zero. The other operations produce no output.

## Samples

### Sample 1

### Input

```text
12
2
3 0 3
2
1 1
2
1 -1
2
3 0 0
2
1 128
2
2
```

### Output

```text
0
F
7
F
E
E
E
```

### Sample 2

### Input

```text
8
3 0 127
2
3 63 64
1 64
2
1 0
3 0 15
2
```

### Output

```text
FFFF
FFFE
1
```

### Sample 3

### Input

```text
0
```

### Output

```text

```

## Sample explanations

Sample 1 first sets the lowest four bits, producing `F` . After one right rotation, the lowest sixteen bits give `7` , while one bit wraps to the highest position. The reverse rotation restores the state. Sample 2 crosses the boundary between bits $63$ and $64$ . Sample 3 contains no operations.

## Constraints and guarantees

For all inputs: $0\le N\le2\times10^6$ , $|x|\le10^9$ , and $0\le l\le r\le127$ .

| Score | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
