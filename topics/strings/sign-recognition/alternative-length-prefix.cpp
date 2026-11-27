// Precomputed length counts. C++17 implementation by Codex (GPT-6).
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
		// Stable radix sort of the pair (Rank, Second), including the -1 sentinel.
		const int MaxRank = *std::max_element(Rank.begin(), Rank.end());
		std::vector<int> Temp(Length);
		auto CountingPass = [&](auto Key)
		{
			std::vector<int> End(MaxRank + 2);
			for (int Position : Suffix)
			{
				++End[Key(Position) + 1];
			}
			std::partial_sum(End.begin(), End.end(), End.begin());
			for (auto It = Suffix.rbegin(); It != Suffix.rend(); ++It)
			{
				Temp[--End[Key(*It) + 1]] = *It;
			}
			Suffix.swap(Temp);
		};
		CountingPass(Second);
		CountingPass([&](int Position) { return Rank[Position]; });
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
	int Common = 0;
	for (int i = 1; i < Length; ++i)
	{
		Common = Owner[Suffix[i]] == Owner[Suffix[i - 1]] ? std::min(Common, Lcp[i]) : Lcp[i];
		Shared[Suffix[i]] = Common;
	}
	Common = 0;
	for (int i = Length - 2; i >= 0; --i)
	{
		Common = Owner[Suffix[i]] == Owner[Suffix[i + 1]] ? std::min(Common, Lcp[i + 1]) : Lcp[i + 1];
		Shared[Suffix[i]] = std::max(Shared[Suffix[i]], Common);
	}

	std::vector<long long> Prefix(Length + 2);
	for (int i = 0; i < Length; ++i)
	{
		if (Shared[i] < Remaining[i])
		{
			++Prefix[Shared[i] + 1];
			--Prefix[Remaining[i] + 1];
		}
	}
	// First integration gives counts by exact length; the second gives range sums.
	std::partial_sum(Prefix.begin(), Prefix.end(), Prefix.begin());
	std::partial_sum(Prefix.begin(), Prefix.end(), Prefix.begin());
	for (int i = 0; i < q; ++i)
	{
		long long l;
		long long r;
		std::cin >> l >> r;
		int Before = static_cast<int>(std::min<long long>(l - 1, Length));
		int Last = static_cast<int>(std::min<long long>(r, Length));
		std::cout << Prefix[Last] - Prefix[Before] << '\n';
	}
}
