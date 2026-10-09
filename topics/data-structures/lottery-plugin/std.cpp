#include <iostream>
#include <iterator>
#include <set>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	long long A;
	long long B;
	long long C;
	int n;
	int m;
	int q;
	int k;
	std::cin >> A >> B >> C >> n >> m >> q >> k;
	std::vector<int> Queries(q);
	std::vector<std::pair<int, int>> Changes(k);
	for (int& Position : Queries)
	{
		std::cin >> Position;
	}
	for (auto& Change : Changes)
	{
		std::cin >> Change.first >> Change.second;
	}
	std::set<std::pair<int, int>> Active;
	std::vector<int> Lucky(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		Lucky[i] = i;
		Active.emplace_hint(Active.end(), i, i);
	}
	int QueryIndex = 0;
	int ChangeIndex = 0;
	for (int i = 1; i <= m; ++i)
	{
		A = (A * B + C) % n + 1;
		const int t = static_cast<int>(A);
		if (QueryIndex < q && Queries[QueryIndex] == i)
		{
			++QueryIndex;
			auto Right = Active.upper_bound({t, n + 1});
			int Answer = 0;
			if (Right != Active.end())
			{
				Answer = Right->second;
			}
			if (Right != Active.begin())
			{
				auto Left = std::prev(Right);
				if (Right == Active.end() || t - Left->first <= Right->first - t)
				{
					Answer = Left->second;
				}
			}
			std::cout << Answer << '\n';
		}
		else if (ChangeIndex < k && Changes[ChangeIndex].first == i)
		{
			const int Person = Changes[ChangeIndex++].second;
			Active.erase({Lucky[Person], Person});
			Lucky[Person] = t;
			Active.emplace(t, Person);
		}
		else
		{
			Active.erase({Lucky[t], t});
		}
	}
}
