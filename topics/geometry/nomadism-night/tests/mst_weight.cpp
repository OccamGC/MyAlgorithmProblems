#include "../mst.hpp"

#include <iostream>

// Diagnostic helper: accepts one or more ordinary inputs until EOF.
// Prints M and the sum of squared edge lengths for each tree.
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	while (std::cin >> n)
	{
		if (n < 1 || n > 400000)
		{
			return 2;
		}
		std::vector<FPoint> Points(n);
		for (int i = 0; i < n; ++i)
		{
			std::cin >> Points[i].x >> Points[i].y;
			Points[i].Id = i;
		}
		const FTree Tree = BuildMinimumSpanningTree(Points);
		std::int64_t Squares = 0;
		for (auto [u, v] : Tree.Edges)
		{
			const std::int64_t dx = Points[u].x - Points[v].x;
			const std::int64_t dy = Points[u].y - Points[v].y;
			Squares += dx * dx + dy * dy;
		}
		std::cout << Tree.Weight << ' ' << Squares << '\n';
	}
	return 0;
}
