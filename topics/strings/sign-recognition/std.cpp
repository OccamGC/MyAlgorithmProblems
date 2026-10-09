#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int q;
	std::cin >> n >> q;
	std::vector<int> Text;
	std::vector<int> Owner;
	std::vector<int> Remaining;
	for (int i = 0; i < n; ++i)
	{
		std::string s;
		std::cin >> s;
		for (int j = 0; j < static_cast<int>(s.size()); ++j)
		{
			Text.push_back(s[j] - 'a' + n);
			Owner.push_back(i);
			Remaining.push_back(static_cast<int>(s.size()) - j);
		}
		Text.push_back(i);
		Owner.push_back(-1);
		Remaining.push_back(0);
	}
	const int Length = static_cast<int>(Text.size());
	std::vector<int> Suffix(Length);
	std::iota(Suffix.begin(), Suffix.end(), 0);
	std::vector<int> Rank = Text;
	std::vector<int> NextRank(Length);
	for (int Width = 1; Width < Length; Width *= 2)
	{
		auto Second = [&](int Position)
		{
			return Position + Width < Length ? Rank[Position + Width] : -1;
		};
		std::sort(Suffix.begin(), Suffix.end(), [&](int a, int b)
		{
			return Rank[a] != Rank[b] ? Rank[a] < Rank[b] : Second(a) < Second(b);
		});
		NextRank[Suffix[0]] = 0;
		for (int i = 1; i < Length; ++i)
		{
			const int a = Suffix[i - 1];
			const int b = Suffix[i];
			NextRank[b] = NextRank[a] + (Rank[a] != Rank[b] || Second(a) != Second(b));
		}
		Rank.swap(NextRank);
		if (Rank[Suffix.back()] == Length - 1)
		{
			break;
		}
	}
	std::vector<int> Lcp(Length);
	int Matched = 0;
	for (int i = 0; i < Length; ++i)
	{
		if (Rank[i] == 0)
		{
			Matched = 0;
			continue;
		}
		const int j = Suffix[Rank[i] - 1];
		while (i + Matched < Length && j + Matched < Length && Text[i + Matched] == Text[j + Matched])
		{
			++Matched;
		}
		Lcp[Rank[i]] = Matched;
		if (Matched > 0)
		{
			--Matched;
		}
	}
	std::vector<int> Shared(Length);
	for (int Id = 0; Id < n; ++Id)
	{
		int Common = 0;
		for (int i = 0; i < Length; ++i)
		{
			Common = i > 0 && Owner[Suffix[i - 1]] != Id ? Lcp[i] : std::min(Common, Lcp[i]);
			if (Owner[Suffix[i]] == Id)
			{
				Shared[Suffix[i]] = std::max(Shared[Suffix[i]], Common);
			}
		}
		Common = 0;
		for (int i = Length - 1; i >= 0; --i)
		{
			Common = i + 1 < Length && Owner[Suffix[i + 1]] != Id ? Lcp[i + 1] : std::min(Common, i + 1 < Length ? Lcp[i + 1] : 0);
			if (Owner[Suffix[i]] == Id)
			{
				Shared[Suffix[i]] = std::max(Shared[Suffix[i]], Common);
			}
		}
	}
	for (int i = 0; i < q; ++i)
	{
		long long l;
		long long r;
		std::cin >> l >> r;
		long long Answer = 0;
		for (int j = 0; j < Length; ++j)
		{
			const long long Low = std::max(l, static_cast<long long>(Shared[j]) + 1);
			const long long High = std::min(r, static_cast<long long>(Remaining[j]));
			Answer += std::max(0LL, High - Low + 1);
		}
		std::cout << Answer << '\n';
	}
}
