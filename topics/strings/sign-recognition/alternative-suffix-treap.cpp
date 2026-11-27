// Suffix treap with integer ranks. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

struct FNode
{
	int Child[2]{};
	int Parent = 0;
	int Size = 1;
	unsigned Priority = 0;
};

// Node p+1 is the suffix starting at p. Zero denotes the empty suffix.
std::vector<int> BuildOrder(const std::vector<int>& Text)
{
	int n = static_cast<int>(Text.size());
	std::vector<FNode> Tree(n + 1);
	Tree[0].Size = 0;
	auto RankOf = [&](int u)
	{
		if (u > n)
		{
			return 0;
		}
		int Rank = 1 + Tree[Tree[u].Child[0]].Size;
		while (Tree[u].Parent)
		{
			int p = Tree[u].Parent;
			if (Tree[p].Child[1] == u)
			{
				Rank += 1 + Tree[Tree[p].Child[0]].Size;
			}
			u = p;
		}
		return Rank;
	};
	auto Pull = [&](int u)
	{
		Tree[u].Size = 1 + Tree[Tree[u].Child[0]].Size + Tree[Tree[u].Child[1]].Size;
	};
	int Root = 0;
	std::mt19937 Random(9173);
	for (int u = n; u > 0; --u)
	{
		Tree[u].Priority = Random();
		int TailRank = RankOf(u + 1);
		int Parent = 0;
		int Current = Root;
		int Side = 0;
		while (Current)
		{
			Parent = Current;
			Side = Text[u - 1] > Text[Current - 1] ||
				(Text[u - 1] == Text[Current - 1] && TailRank > RankOf(Current + 1));
			Current = Tree[Current].Child[Side];
		}
		Tree[u].Parent = Parent;
		if (Parent == 0)
		{
			Root = u;
			continue;
		}
		Tree[Parent].Child[Side] = u;
		for (int p = Parent; p; p = Tree[p].Parent)
		{
			++Tree[p].Size;
		}
		while (Parent && Tree[u].Priority > Tree[Parent].Priority)
		{
			Side = Tree[Parent].Child[1] == u;
			int Grand = Tree[Parent].Parent;
			int Middle = Tree[u].Child[Side ^ 1];
			if (Middle)
			{
				Tree[Middle].Parent = Parent;
			}
			Tree[Parent].Child[Side] = Middle;
			Tree[u].Child[Side ^ 1] = Parent;
			Tree[Parent].Parent = u;
			Tree[u].Parent = Grand;
			if (Grand)
			{
				Tree[Grand].Child[Tree[Grand].Child[1] == Parent] = u;
			}
			else
			{
				Root = u;
			}
			Pull(Parent);
			Pull(u);
			Parent = Grand;
		}
	}
	std::vector<int> Suffix;
	std::vector<int> Stack;
	int u = Root;
	while (u || !Stack.empty())
	{
		while (u)
		{
			Stack.push_back(u);
			u = Tree[u].Child[0];
		}
		u = Stack.back();
		Stack.pop_back();
		Suffix.push_back(u - 1);
		u = Tree[u].Child[1];
	}
	return Suffix;
}

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
	std::vector<int> Suffix = BuildOrder(Text);
	std::vector<int> Rank(Length);
	for (int i = 0; i < Length; ++i)
	{
		Rank[Suffix[i]] = i;
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
