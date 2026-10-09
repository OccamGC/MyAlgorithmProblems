#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<std::pair<int, int>> Buildings(k);
	std::vector<int> Boundaries = {0, m + 1};
	for (auto& Building : Buildings)
	{
		std::cin >> Building.first >> Building.second;
		Boundaries.push_back(Building.second);
	}
	std::sort(Buildings.begin(), Buildings.end());
	std::sort(Boundaries.begin(), Boundaries.end());
	Boundaries.erase(std::unique(Boundaries.begin(), Boundaries.end()), Boundaries.end());
	int Answer = 0;
	for (std::size_t i = 0; i + 1 < Boundaries.size(); ++i)
	{
		for (std::size_t j = i + 1; j < Boundaries.size(); ++j)
		{
			const int Width = Boundaries[j] - Boundaries[i] - 1;
			int Previous = 0;
			for (const auto& Building : Buildings)
			{
				if (Boundaries[i] < Building.second && Building.second < Boundaries[j])
				{
					Answer = std::max(Answer, std::min(Width, Building.first - Previous - 1));
					Previous = Building.first;
				}
			}
			Answer = std::max(Answer, std::min(Width, n - Previous));
		}
	}
	std::cout << Answer << '\n';
}
