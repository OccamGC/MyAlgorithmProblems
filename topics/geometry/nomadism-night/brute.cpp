#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

// Dense complete-graph Prim oracle; intended only for small inputs.
// Unlike std.cpp, this diagnostic program prints M, not a tour.
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	while (std::cin >> n)
	{
		std::vector<std::pair<int, int>> Points(n);
		for (auto& [x, y] : Points)
		{
			std::cin >> x >> y;
		}
		std::vector<std::int64_t> Best(n, std::numeric_limits<std::int64_t>::max());
		std::vector<bool> Visited(n, false);
		Best[0] = 0;
		std::int64_t Total = 0;
		for (int Iteration = 0; Iteration < n; ++Iteration)
		{
			int u = -1;
			for (int i = 0; i < n; ++i)
			{
				if (!Visited[i] && (u == -1 || Best[i] < Best[u]))
				{
					u = i;
				}
			}
			Total += Best[u];
			Visited[u] = true;
			for (int v = 0; v < n; ++v)
			{
				if (Visited[v])
				{
					continue;
				}
				const std::int64_t dx = Points[u].first - Points[v].first;
				const std::int64_t dy = Points[u].second - Points[v].second;
				Best[v] = std::min(Best[v], std::abs(dx) + std::abs(dy));
			}
		}
		std::cout << Total << '\n';
	}
	return 0;
}
