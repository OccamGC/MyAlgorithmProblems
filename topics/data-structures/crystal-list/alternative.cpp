// Codex (GPT-6): ordered-interval implementation and amortized analysis.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <iterator>
#include <map>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int k;
	int m;
	std::cin >> n >> k >> m;
	std::map<int, int> Segments;
	int Previous = -1;
	for (int i = 1; i <= n; ++i)
	{
		int Color;
		std::cin >> Color;
		if (Color != Previous)
		{
			Segments.emplace_hint(Segments.end(), i, Color);
		}
		Previous = Color;
	}
	Segments[n + 1] = 0;
	std::vector<int> Energy(k + 1);
	for (int i = 1; i <= k; ++i)
	{
		std::cin >> Energy[i];
	}
	auto Split = [&](int Position)
	{
		auto It = Segments.lower_bound(Position);
		if (It->first == Position)
		{
			return It;
		}
		return Segments.emplace_hint(It, Position, std::prev(It)->second);
	};
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 1)
		{
			int Color;
			int Value;
			std::cin >> Color >> Value;
			Energy[Color] = Value;
		}
		else
		{
			int l;
			int r;
			int Color;
			std::cin >> l >> r >> Color;
			auto End = Split(r + 1);
			auto Begin = Split(l);
			std::int64_t Answer = 0;
			for (auto It = Begin; It != End; ++It)
			{
				Answer += std::int64_t(std::next(It)->first - It->first)
					* std::abs(Energy[It->second] - Energy[Color]);
			}
			Segments.erase(Begin, End);
			Segments.emplace_hint(End, l, Color);
			std::cout << Answer << '\n';
		}
	}
}
