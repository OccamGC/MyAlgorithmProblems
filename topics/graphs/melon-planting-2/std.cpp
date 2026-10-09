// 解法改进：Codex（GPT-6）。简化集合判定，结合格雷码与增广路维护最大匹配。
// Solution improvement: Codex (GPT-6), combining established matching and Gray-code methods.
// Contribution for this problem: subset feasibility reduction and O(p * 2^p) incremental implementation.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

class FMatching
{
public:
	int p;
	int q;
	int Size = 0;
	int ActiveLeftCount = 0;
	int ActiveRightCount;
	std::vector<std::vector<int>> Edges;
	std::vector<std::vector<int>> Reverse;
	std::vector<int> LeftMatch;
	std::vector<int> RightMatch;
	std::vector<int> SeenLeft;
	std::vector<int> SeenRight;
	std::vector<bool> bLeftActive;
	std::vector<bool> bRightActive;
	int Stamp = 0;

	FMatching(int LeftCount, int RightCount, std::vector<std::vector<int>> Adjacency)
		: p(LeftCount), q(RightCount), ActiveRightCount(q), Edges(std::move(Adjacency)), Reverse(q),
		LeftMatch(p, -1), RightMatch(q, -1), SeenLeft(p), SeenRight(q),
		bLeftActive(p, false), bRightActive(q, true)
	{
		for (int u = 0; u < p; ++u)
		{
			for (int v : Edges[u])
			{
				Reverse[v].push_back(u);
			}
		}
	}

	bool FromLeft(int u)
	{
		if (SeenLeft[u] == Stamp)
		{
			return false;
		}
		SeenLeft[u] = Stamp;
		for (int v : Edges[u])
		{
			if (bRightActive[v] && (RightMatch[v] == -1 || FromLeft(RightMatch[v])))
			{
				LeftMatch[u] = v;
				RightMatch[v] = u;
				return true;
			}
		}
		return false;
	}

	bool FromRight(int v)
	{
		if (SeenRight[v] == Stamp)
		{
			return false;
		}
		SeenRight[v] = Stamp;
		for (int u : Reverse[v])
		{
			if (bLeftActive[u] && (LeftMatch[u] == -1 || FromRight(LeftMatch[u])))
			{
				LeftMatch[u] = v;
				RightMatch[v] = u;
				return true;
			}
		}
		return false;
	}

	void ChangeLeft(int u, bool bActive)
	{
		bLeftActive[u] = bActive;
		ActiveLeftCount += bActive ? 1 : -1;
		++Stamp;
		if (bActive)
		{
			if (Size < ActiveRightCount)
			{
				Size += FromLeft(u);
			}
		}
		else if (LeftMatch[u] != -1)
		{
			const int v = LeftMatch[u];
			LeftMatch[u] = RightMatch[v] = -1;
			--Size;
			if (Size < ActiveLeftCount)
			{
				Size += FromRight(v);
			}
		}
	}

	void ChangeRight(int v, bool bActive)
	{
		bRightActive[v] = bActive;
		ActiveRightCount += bActive ? 1 : -1;
		++Stamp;
		if (bActive)
		{
			if (Size < ActiveLeftCount)
			{
				Size += FromRight(v);
			}
		}
		else if (RightMatch[v] != -1)
		{
			const int u = RightMatch[v];
			LeftMatch[u] = RightMatch[v] = -1;
			--Size;
			if (Size < ActiveRightCount)
			{
				Size += FromLeft(u);
			}
		}
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int p;
	int q;
	std::cin >> p >> q;
	std::vector<std::vector<int>> Edges(p);
	std::vector<int> Used;
	for (auto& Row : Edges)
	{
		int Degree;
		std::cin >> Degree;
		Row.resize(Degree);
		for (int& v : Row)
		{
			std::cin >> v;
			Used.push_back(v);
		}
	}
	std::sort(Used.begin(), Used.end());
	Used.erase(std::unique(Used.begin(), Used.end()), Used.end());
	if (Used.empty())
	{
		std::cout << 0 << '\n';
		return 0;
	}
	q = static_cast<int>(Used.size());
	for (auto& Row : Edges)
	{
		for (int& v : Row)
		{
			v = static_cast<int>(std::lower_bound(Used.begin(), Used.end(), v) - Used.begin());
		}
	}
	FMatching State(p, q, std::move(Edges));
	std::vector<int> Required(q);
	for (int v = 0; v < q; ++v)
	{
		Required[v] = static_cast<int>(State.Reverse[v].size());
	}
	int RequiredCount = q;
	int SelectedCount = 0;
	int Answer = q == 0 ? 0 : p;
	std::uint32_t Previous = 0;
	for (std::uint32_t i = 1; i < (std::uint32_t{1} << p); ++i)
	{
		const std::uint32_t Mask = i ^ (i >> 1);
		std::uint32_t Difference = Mask ^ Previous;
		int u = 0;
		while ((Difference & 1) == 0)
		{
			Difference >>= 1;
			++u;
		}
		const bool bActive = (Mask >> u & 1) != 0;
		SelectedCount += bActive ? 1 : -1;
		State.ChangeLeft(u, bActive);
		for (int v : State.Edges[u])
		{
			Required[v] += bActive ? -1 : 1;
			const bool bNeeded = Required[v] != 0;
			if (bNeeded != State.bRightActive[v])
			{
				RequiredCount += bNeeded ? 1 : -1;
				State.ChangeRight(v, bNeeded);
			}
		}
		if (State.Size == RequiredCount)
		{
			Answer = std::min(Answer, SelectedCount);
		}
		Previous = Mask;
	}
	std::cout << Answer << '\n';
}
