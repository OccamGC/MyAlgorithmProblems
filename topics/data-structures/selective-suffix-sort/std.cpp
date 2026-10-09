// Problem setter's active inversion counts and two segment-tree layers.
// Inactive-pivot repair, proof and portable implementation: GPT-6.
#include <algorithm>
#include <iostream>
#include <limits>
#include <vector>

constexpr int Infinity = 1000000007;
struct FGroupNode
{
	int Left = 0;
	int Right = 0;
	int Minimum = Infinity;
	int Active = 0;
	int Lazy = 0;
};

class FSorter
{
private:
	int n;
	std::vector<int> Rank;
	std::vector<int> PositionInGroup;
	std::vector<int> MinimumRank;
	std::vector<int> Roots;
	std::vector<std::vector<int>> Positions;
	std::vector<FGroupNode> Group;
	long long Answer = 0;

	int BuildGroup(int l, int r, const std::vector<int>& Members, const std::vector<int>& Count)
	{
		int u = static_cast<int>(Group.size());
		Group.emplace_back();
		if (l == r)
		{
			if (Count[Members[l]] > 0)
			{
				Group[u].Minimum = Count[Members[l]];
				Group[u].Active = 1;
			}
		}
		else
		{
			int Middle = (l + r) / 2;
			int Left = BuildGroup(l, Middle, Members, Count);
			int Right = BuildGroup(Middle + 1, r, Members, Count);
			Group[u].Left = Left;
			Group[u].Right = Right;
			PullGroup(u);
		}
		return u;
	}
	void PullGroup(int u)
	{
		const FGroupNode& Left = Group[Group[u].Left];
		const FGroupNode& Right = Group[Group[u].Right];
		Group[u].Minimum = std::min(Left.Minimum, Right.Minimum);
		Group[u].Active = Left.Active + Right.Active;
	}
	void Apply(int u, int Delta)
	{
		if (Group[u].Active > 0)
		{
			Group[u].Minimum -= Delta;
			Group[u].Lazy += Delta;
		}
	}
	void Push(int u)
	{
		if (Group[u].Lazy != 0)
		{
			Apply(Group[u].Left, Group[u].Lazy);
			Apply(Group[u].Right, Group[u].Lazy);
			Group[u].Lazy = 0;
		}
	}
	void SetGlobal(int u, int l, int r, int Position, int Value)
	{
		if (l == r)
		{
			MinimumRank[u] = Value;
			return;
		}
		int Middle = (l + r) / 2;
		if (Position <= Middle)
		{
			SetGlobal(2 * u, l, Middle, Position, Value);
		}
		else
		{
			SetGlobal(2 * u + 1, Middle + 1, r, Position, Value);
		}
		MinimumRank[u] = std::min(MinimumRank[2 * u], MinimumRank[2 * u + 1]);
	}
	int ReadCount(int u, int l, int r, int Position)
	{
		if (Group[u].Active == 0)
		{
			return 0;
		}
		if (l == r)
		{
			return Group[u].Minimum;
		}
		Push(u);
		int Middle = (l + r) / 2;
		return Position <= Middle ? ReadCount(Group[u].Left, l, Middle, Position)
			: ReadCount(Group[u].Right, Middle + 1, r, Position);
	}
	void EraseGroup(int u, int l, int r, int Position)
	{
		if (l == r)
		{
			Answer -= Group[u].Minimum;
			Group[u].Minimum = Infinity;
			Group[u].Active = 0;
			Group[u].Lazy = 0;
			return;
		}
		Push(u);
		int Middle = (l + r) / 2;
		if (Position <= Middle)
		{
			EraseGroup(Group[u].Left, l, Middle, Position);
		}
		else
		{
			EraseGroup(Group[u].Right, Middle + 1, r, Position);
		}
		PullGroup(u);
	}
	void Clear(int Position)
	{
		int Value = Rank[Position];
		EraseGroup(Roots[Value], 0, static_cast<int>(Positions[Value].size()) - 1, PositionInGroup[Position]);
		SetGlobal(1, 0, n - 1, Position, Infinity);
	}
	void ClearSmaller(int u, int l, int r, int Start, int Value)
	{
		if (r < Start || MinimumRank[u] >= Value)
		{
			return;
		}
		if (l == r)
		{
			Clear(l);
			return;
		}
		int Middle = (l + r) / 2;
		ClearSmaller(2 * u, l, Middle, Start, Value);
		ClearSmaller(2 * u + 1, Middle + 1, r, Start, Value);
		MinimumRank[u] = std::min(MinimumRank[2 * u], MinimumRank[2 * u + 1]);
	}
	void Decrease(int u, int l, int r, int Start, int Value)
	{
		if (r < Start || Group[u].Active == 0)
		{
			return;
		}
		if (Start <= l && Group[u].Minimum > 1)
		{
			Answer -= Group[u].Active;
			Apply(u, 1);
			return;
		}
		if (l == r)
		{
			--Answer;
			Group[u].Minimum = Infinity;
			Group[u].Active = 0;
			Group[u].Lazy = 0;
			SetGlobal(1, 0, n - 1, Positions[Value][l], Infinity);
			return;
		}
		Push(u);
		int Middle = (l + r) / 2;
		Decrease(Group[u].Left, l, Middle, Start, Value);
		Decrease(Group[u].Right, Middle + 1, r, Start, Value);
		PullGroup(u);
	}
public:
	explicit FSorter(const std::vector<int>& a) : n(static_cast<int>(a.size())), Rank(n),
		PositionInGroup(n), MinimumRank(4 * n, Infinity)
	{
		std::vector<int> Values = a;
		std::sort(Values.begin(), Values.end());
		Values.erase(std::unique(Values.begin(), Values.end()), Values.end());
		int Unique = static_cast<int>(Values.size());
		Positions.resize(Unique);
		Roots.resize(Unique);
		std::vector<int> Fenwick(Unique + 1);
		std::vector<int> Count(n);
		for (int i = n - 1; i >= 0; --i)
		{
			Rank[i] = static_cast<int>(std::lower_bound(Values.begin(), Values.end(), a[i]) - Values.begin());
			for (int j = Rank[i]; j > 0; j -= j & -j)
			{
				Count[i] += Fenwick[j];
			}
			for (int j = Rank[i] + 1; j <= Unique; j += j & -j)
			{
				++Fenwick[j];
			}
			Answer += Count[i];
			if (Count[i] > 0)
			{
				SetGlobal(1, 0, n - 1, i, Rank[i]);
			}
		}
		for (int i = 0; i < n; ++i)
		{
			PositionInGroup[i] = static_cast<int>(Positions[Rank[i]].size());
			Positions[Rank[i]].push_back(i);
		}
		Group.reserve(2 * n + 1);
		Group.emplace_back();
		for (int Value = 0; Value < Unique; ++Value)
		{
			Roots[Value] = BuildGroup(0, static_cast<int>(Positions[Value].size()) - 1, Positions[Value], Count);
		}
	}
	long long GetAnswer() const
	{
		return Answer;
	}
	void Sort(int k)
	{
		int Value = Rank[k];
		int Last = static_cast<int>(Positions[Value].size()) - 1;
		if (ReadCount(Roots[Value], 0, Last, PositionInGroup[k]) == 0)
		{
			return;
		}
		Clear(k);
		ClearSmaller(1, 0, n - 1, k + 1, Value);
		Decrease(Roots[Value], 0, Last, PositionInGroup[k] + 1, Value);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> a(n);
	for (int& Value : a)
	{
		std::cin >> Value;
	}
	FSorter Sorter(a);
	std::cout << Sorter.GetAnswer() << '\n';
	for (int i = 0; i < m; ++i)
	{
		int Raw;
		std::cin >> Raw;
		int k = Raw - 1;
		if (Raw < 0)
		{
			long long Decoded = (Sorter.GetAnswer() + Raw) % n;
			k = static_cast<int>((Decoded + n) % n);
		}
		Sorter.Sort(k);
		std::cout << Sorter.GetAnswer() << '\n';
	}
}

