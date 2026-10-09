# Three counterexamples to local accounting arguments

Each fixture is a valid induced four-neighbor forest. These examples refute stronger intermediate claims, not the conjectured cubic algorithm bound. Coordinates are zero-based row and column indices.

## 1. A new success need not enlarge the bounding box

The [nine-by-nine fixture](inputs/unchanged-bounding-box.in) has nineteen moves and forty-four candidate checks. Fix a target and translate each successful complete query prefix so that its current endpoint hits the target. A new successful copy need not enlarge the bounding box of the preceding copies. Thus a success cannot always be charged to a newly reached boundary position.

## 2. A new success need not enlarge the union of copies

In the [seventeen-by-seventeen fixture](inputs/unchanged-union.in), the entire first row is road. Only columns zero, two, four, six, eight, and ten are road in the second row; all remaining cells are obstacles. The target is $(1,8)$. The query first visits a horizontal backbone of nine cells, then visits second-row tooth tips in column order zero, four, two, eight, six.

The complete translated prefix at the fifth successful tooth tip is already contained in the union of the preceding four copies. That union still has twenty-three cells. Combining a bounding-box charge with a charge for previously uncovered road cells therefore need not increase the potential at every success. This fixture has thirty-nine moves and one hundred thirty-eight candidate checks.

## 3. One final-step direction can still contain a nondegenerate parallelogram

In the [eight-by-eight fixture](inputs/same-direction-parallelogram.in), fix target $(6,5)$. Four displacements that successfully hit this target upon first discovery occur in this order:

$$
(1,0),\quad(2,-2),\quad(2,0),\quad(1,2).
$$

All four final steps are downward, and

$$
(1,0)+(2,0)=(2,-2)+(1,2).
$$

These points form a nondegenerate parallelogram. Successful displacements from different times therefore cannot be grouped solely by final-step direction and then bounded with the static forbidden-pattern lemma. That lemma requires all relevant copies of one complete template to coexist; these successful events use different prefixes. The fixture has sixty-nine moves and ninety-seven candidate checks.

The [verifier](../verify_examples.py) checks these scan counts and directly verifies the copy containment and parallelogram events in the last two examples.
