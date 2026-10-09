#include <algorithm>
#include <cmath>
#include <functional>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int BlockLimit;
	int e;
	long double RoundingOffset;
	std::cin >> n >> BlockLimit >> e >> RoundingOffset;
	std::vector<std::vector<int>> Graph(n);
	for (int i = 0; i < e; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Graph[u - 1].push_back(v - 1);
		Graph[v - 1].push_back(u - 1);
	}
	std::vector<long double> Damage(n);
	std::vector<long double> p(n);
	for (auto& Value : Damage)
	{
		std::cin >> Value;
	}
	for (auto& Value : p)
	{
		std::cin >> Value;
	}
	long double Answer = 0;
	std::vector<int> Parent(n);
	std::vector<int> Order;
	std::vector<long double> dp(n);
	std::vector<long double> Children;
	for (int Root = 0; Root < n; ++Root)
	{
		Order.clear();
		Order.push_back(Root);
		Parent[Root] = -1;
		for (std::size_t Index = 0; Index < Order.size(); ++Index)
		{
			int u = Order[Index];
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Order.push_back(v);
				}
			}
		}
		for (auto It = Order.rbegin(); It != Order.rend(); ++It)
		{
			int u = *It;
			Children.clear();
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					Children.push_back(dp[v]);
				}
			}
			std::sort(Children.begin(), Children.end(), std::greater<long double>());
			long double Sum = 0;
			long double Best = 0;
			for (std::size_t i = 0; i < Children.size(); ++i)
			{
				Sum += Children[i];
				long double Candidate = Sum * (p[u] + (1 - p[u]) / (i + 1));
				if (BlockLimit > 0 || i + 1 == Children.size())
				{
					Best = std::max(Best, Candidate);
				}
			}
			dp[u] = Damage[u] + Best;
		}
		Answer = std::max(Answer, dp[Root]);
	}
	std::cout << static_cast<long long>(std::floor(Answer + RoundingOffset + 0.5L)) << '\n';
}
