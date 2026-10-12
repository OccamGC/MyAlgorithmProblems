"""Check the finite tree-extension examples; the general proofs are in the notes."""
import json

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def neighbors(point):
    x, y = point
    return {(x + dx, y + dy) for dx, dy in DIRECTIONS}


def radius(point):
    return abs(point[0]) + abs(point[1])


def shell(t):
    assert t >= 0
    return {(x, sign * (t - abs(x)))
            for x in range(-t, t + 1) for sign in (-1, 1)}


def cycle(t):
    assert t >= 2
    return shell(t) | {p for p in shell(t + 1) if p[0] * p[1] != 0}


def path(t):
    return cycle(t) - {(-1, -t), (0, -t), (1, -t)}


def induced_components(points):
    """Discover all actual grid edges, including unintended adjacencies."""
    adjacency = {p: neighbors(p) & points for p in points}
    unseen = set(points)
    components = []
    while unseen:
        root = unseen.pop()
        stack, component = [root], {root}
        while stack:
            for other in adjacency[stack.pop()]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    stack.append(other)
        edge_count = sum(len(adjacency[p]) for p in component) // 2
        components.append((component, edge_count))
    return adjacency, components


def check_paths(paths):
    roads = set().union(*paths)
    assert len(roads) == sum(map(len, paths)), "Overlapping components"
    adjacency, components = induced_components(roads)
    assert {frozenset(c) for c, _ in components} == {
        frozenset(p) for p in paths
    }, "Unexpected edges between intended components"
    for component, edges in components:
        assert edges == len(component) - 1, "Induced component contains a cycle"
        assert all(len(adjacency[p]) <= 2 for p in component), "Not a path"
    return roads


def check_staircase(t):
    ring = cycle(t)
    adjacency, components = induced_components(ring)
    assert len(ring) == 8 * t
    assert len(components) == 1
    assert all(len(adjacent) == 2 for adjacent in adjacency.values())
    points = path(t)
    check_paths([points])
    assert len(points) == 8 * t - 3
    assert all(max(abs(x), abs(y)) <= t for x, y in points)


def check_barrier(t, outer, inner):
    forbidden = shell(t - 1)
    assert len(forbidden) == 4 * t - 4
    assert not forbidden & (outer | inner)
    assert all(len(neighbors(p) & outer) >= 2 for p in forbidden)
    assert min(map(radius, outer)) == t
    assert max(map(radius, inner)) <= t - 2
    # Every grid step changes the integer radius by one, forcing all paths
    # from inner to outer through this shell, regardless of the board boundary.
    return forbidden


def check_small():
    rows = (".AAA.", ".A.AA", "..B.A", ".A.AA", ".AAA.")
    outer = {(r, c) for r, row in enumerate(rows)
             for c, char in enumerate(row) if char == "A"}
    inner = {(2, 2)}
    check_paths([outer, inner])
    assert len(outer) == 13
    forbidden = neighbors((2, 2))
    assert not forbidden & (outer | inner)
    for point in forbidden:
        assert len(neighbors(point) & outer) >= 2
        _, components = induced_components(outer | {point})
        assert len(components) == 1
        vertices, edges = components[0]
        assert edges >= len(vertices), "Added bridge failed to create a cycle"
    return {"side": 5, "component_sizes": [13, 1], "forbidden_cells": 4}


def check_two(k):
    n = 2 * k + 1
    outer, inner = path(k), path(k - 3)
    check_paths([outer, inner])
    assert (len(outer), len(inner)) == (4 * n - 7, 4 * n - 31)
    forbidden = check_barrier(k, outer, inner)
    bridges = {p for p in forbidden if neighbors(p) & inner}
    assert len(bridges) == 4 * k - 10 == 2 * n - 12
    missing = {(k - 1, 0), (1 - k, 0), (0, k - 1), (0, 1 - k),
               (-1, 2 - k), (1, 2 - k)}
    assert forbidden - bridges == missing
    return {"side": n, "component_sizes": [len(outer), len(inner)],
            "forbidden_cells": len(forbidden), "direct_bridges": len(bridges)}


def check_nested(s):
    n = 12 * s + 1
    radii = [6 * s - 3 * i for i in range(s + 1)]
    paths = [path(t) for t in radii]
    roads = check_paths(paths)
    assert all(max(abs(x), abs(y)) <= 6 * s for x, y in roads)
    assert len(paths) == s + 1
    assert [len(p) for p in paths] == [48 * s - 24 * i - 3 for i in range(s + 1)]
    assert (min(map(len, paths)), max(map(len, paths))) == (2 * n - 5, 4 * n - 7)
    assert len(roads) == (s + 1) * (36 * s - 3)
    all_forbidden = set()
    for i, t in enumerate(radii[:-1]):
        inner = set().union(*paths[i + 1:])
        forbidden = check_barrier(t, paths[i], inner)
        assert not forbidden & (roads | all_forbidden)
        all_forbidden.update(forbidden)
    assert len(all_forbidden) == 18 * s * s + 2 * s
    return {"s": s, "side": n, "trees": len(paths),
            "min_tree": min(map(len, paths)), "max_tree": max(map(len, paths)),
            "roads": len(roads), "forbidden_cells": len(all_forbidden)}


def main():
    two_parameters = (5, 6, 8, 12, 20, 32, 64)
    nested_parameters = (1, 2, 3, 5, 10, 20, 33)
    radii = {t for k in two_parameters for t in (k, k - 3)}
    radii.update(6 * s - 3 * i for s in nested_parameters for i in range(s + 1))
    for t in sorted(radii):
        check_staircase(t)
    report = {"small_example": check_small(),
              "two_paths": [check_two(k) for k in two_parameters],
              "nested_paths": [check_nested(s) for s in nested_parameters]}
    print(json.dumps(report, indent=2))
    print("PASS: all induced paths, counts, direct bridges, and separating shells.")


if __name__ == "__main__":
    main()
