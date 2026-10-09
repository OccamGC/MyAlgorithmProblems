#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

class FParityDisjointSet
{
public:
	explicit FParityDisjointSet(int n)
		: Parent(n + 1), Size(n + 1, 1), Parity(n + 1, 0),
		  ColorCount(n + 1, {1, 0}), MaximumFirstColor(n)
	{
		std::iota(Parent.begin(), Parent.end(), 0);
	}

	bool AddConflict(int u, int v)
	{
		auto [RootU, ParityU] = Find(u);
		auto [RootV, ParityV] = Find(v);
		if (RootU == RootV)
		{
			return (ParityU ^ ParityV) == 1;
		}

		const int Offset = ParityU ^ ParityV ^ 1;
		if (Size[RootU] > Size[RootV])
		{
			std::swap(RootU, RootV);
		}
		MaximumFirstColor -= std::max(ColorCount[RootU][0], ColorCount[RootU][1]);
		MaximumFirstColor -= std::max(ColorCount[RootV][0], ColorCount[RootV][1]);
		ColorCount[RootV][0] += ColorCount[RootU][Offset];
		ColorCount[RootV][1] += ColorCount[RootU][Offset ^ 1];
		Parent[RootU] = RootV;
		Parity[RootU] = Offset;
		Size[RootV] += Size[RootU];
		MaximumFirstColor += std::max(ColorCount[RootV][0], ColorCount[RootV][1]);
		return true;
	}

	int GetMaximumFirstColor() const
	{
		return MaximumFirstColor;
	}

private:
	std::vector<int> Parent;
	std::vector<int> Size;
	std::vector<int> Parity;
	std::vector<std::array<int, 2>> ColorCount;
	int MaximumFirstColor;

	std::pair<int, int> Find(int x)
	{
		if (Parent[x] == x)
		{
			return {x, 0};
		}
		auto [Root, ParentParity] = Find(Parent[x]);
		Parity[x] ^= ParentParity;
		Parent[x] = Root;
		return {Root, Parity[x]};
	}
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
	FParityDisjointSet DisjointSet(n);
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		const bool bAccepted = DisjointSet.AddConflict(u, v);
		std::cout << (bAccepted ? 1 : 0) << ' '
			<< DisjointSet.GetMaximumFirstColor() << '\n';
	}
}
