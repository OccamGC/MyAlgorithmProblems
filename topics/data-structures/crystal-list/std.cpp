// Original uniform-color segment tree; mixed nodes are charged amortized.
// Contribution: Codex (GPT-6): empty-input handling and 64-bit scores.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

class FColorTree
{
	std::vector<int> Color;
	const std::vector<int>& Energy;

public:
	FColorTree(int n, const std::vector<int>& InEnergy) : Color(4 * n + 4, 0), Energy(InEnergy)
	{
		if (n > 0)
		{
			Build(1, 1, n);
		}
	}

	void Build(int Node, int Left, int Right)
	{
		if (Left == Right)
		{
			std::cin >> Color[Node];
			return;
		}
		const int Middle = (Left + Right) / 2;
		Build(2 * Node, Left, Middle);
		Build(2 * Node + 1, Middle + 1, Right);
		Pull(Node);
	}

	void Pull(int Node)
	{
		Color[Node] = Color[2 * Node] == Color[2 * Node + 1] ? Color[2 * Node] : 0;
	}

	std::int64_t Replace(int Node, int Left, int Right, int l, int r, int NewColor)
	{
		if (l <= Left && Right <= r && Color[Node] != 0)
		{
			const std::int64_t Score = std::int64_t(Right - Left + 1) * std::abs(Energy[Color[Node]] - Energy[NewColor]);
			Color[Node] = NewColor;
			return Score;
		}
		if (Color[Node] != 0)
		{
			Color[2 * Node] = Color[2 * Node + 1] = Color[Node];
		}
		const int Middle = (Left + Right) / 2;
		std::int64_t Score = 0;
		if (l <= Middle)
		{
			Score += Replace(2 * Node, Left, Middle, l, r, NewColor);
		}
		if (r > Middle)
		{
			Score += Replace(2 * Node + 1, Middle + 1, Right, l, r, NewColor);
		}
		Pull(Node);
		return Score;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int k;
	int m;
	std::cin >> n >> k >> m;
	std::vector<int> Energy(k + 1);
	FColorTree Tree(n, Energy);
	for (int i = 1; i <= k; ++i)
	{
		std::cin >> Energy[i];
	}
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 1)
		{
			int c;
			int e;
			std::cin >> c >> e;
			Energy[c] = e;
		}
		else
		{
			int l;
			int r;
			int c;
			std::cin >> l >> r >> c;
			std::cout << Tree.Replace(1, 1, n, l, r, c) << '\n';
		}
	}
}
