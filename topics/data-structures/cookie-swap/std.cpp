#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

using FInt64 = std::int64_t;

struct FSummary
{
	FInt64 Demand = 0; // Sum of d_i: receiving capacities.
	FInt64 Supply = 0; // Sum of s_i: providing capacities.
	FInt64 MaxPair = 0; // Maximum d_i + s_i for one participant.
};

static FSummary Merge(const FSummary& Left, const FSummary& Right)
{
	return {Left.Demand + Right.Demand, Left.Supply + Right.Supply,
		std::max(Left.MaxPair, Right.MaxPair)};
}

class FSegmentTree
{
public:
	explicit FSegmentTree(int n)
	{
		while (Base < n)
		{
			Base *= 2;
		}
		Nodes.resize(2 * Base);
	}

	void ReadLeaves(int n)
	{
		for (int i = 0; i < n; ++i)
		{
			FSummary& Leaf = Nodes[Base + i];
			std::cin >> Leaf.Demand >> Leaf.Supply;
			Leaf.MaxPair = Leaf.Demand + Leaf.Supply;
		}
		for (int i = Base - 1; i > 0; --i)
		{
			Nodes[i] = Merge(Nodes[2 * i], Nodes[2 * i + 1]);
		}
	}

	void Update(int x, int Type, FInt64 Value)
	{
		int Index = Base + x - 1;
		if (Type == 1)
		{
			Nodes[Index].Demand = Value;
		}
		else
		{
			Nodes[Index].Supply = Value;
		}
		Nodes[Index].MaxPair = Nodes[Index].Demand + Nodes[Index].Supply;
		for (Index /= 2; Index > 0; Index /= 2)
		{
			Nodes[Index] = Merge(Nodes[2 * Index], Nodes[2 * Index + 1]);
		}
	}

	FSummary Query(int l, int r) const
	{
		FSummary Result;
		for (l += Base - 1, r += Base; l < r; l /= 2, r /= 2)
		{
			if (l & 1)
			{
				Result = Merge(Result, Nodes[l++]);
			}
			if (r & 1)
			{
				Result = Merge(Result, Nodes[--r]);
			}
		}
		return Result;
	}

private:
	int Base = 1;
	std::vector<FSummary> Nodes;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	int m;
	if (!(std::cin >> n >> m))
	{
		return 0;
	}
	FSegmentTree Tree(n);
	Tree.ReadLeaves(n);
	for (int i = 0; i < m; ++i)
	{
		int Type;
		int x;
		int y;
		std::cin >> Type >> x >> y;
		if (Type == 3)
		{
			const FSummary Range = Tree.Query(x, y);
			std::cout << std::min({Range.Demand, Range.Supply,
				Range.Demand + Range.Supply - Range.MaxPair}) << '\n';
		}
		else
		{
			Tree.Update(x, Type, y);
		}
	}
}
