// Bidirectional palindromic trees. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <array>
#include <iostream>
#include <string>
#include <vector>

struct FNode
{
	int Length = 0;
	int Link = 0;
	std::array<int, 2> Child{};
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int K;
	std::string Ring;
	std::cin >> n >> K >> Ring;
	K = std::min(K, n);
	std::vector<int> Ending(n * K);
	std::vector<int> Answer(n);
	for (int Pass = 0; Pass < 2; ++Pass)
	{
		if (Pass == 1)
		{
			std::reverse(Ring.begin(), Ring.end());
		}
		std::string Text = Ring + Ring;
		std::vector<FNode> Nodes(2);
		Nodes.reserve(2 * n + 2);
		Nodes[0].Length = -1;
		std::vector<int> Best;
		Best.reserve((2 * n + 2) * K);
		Best.resize(2 * K);
		int Last = 1;
		for (int i = 0; i < 2 * n - 1; ++i)
		{
			int Bit = Text[i] - '0';
			auto Extendable = [&](int v)
			{
				while (Nodes[v].Length + 2 > n || i - Nodes[v].Length - 1 < 0
					|| Text[i - Nodes[v].Length - 1] != Text[i])
				{
					v = Nodes[v].Link;
				}
				return v;
			};
			int Parent = Extendable(Last);
			if (Nodes[Parent].Child[Bit] == 0)
			{
				int v = static_cast<int>(Nodes.size());
				int Length = Nodes[Parent].Length + 2;
				int Link = Length == 1 ? 1 : Nodes[Extendable(Nodes[Parent].Link)].Child[Bit];
				Nodes.push_back({Length, Link, {}});
				Nodes[Parent].Child[Bit] = v;
				for (int j = 1; j <= K; ++j)
				{
					int Suffix = Best[Link * K + j - 1];
					Best.push_back(Length == Suffix + j ? Length : Suffix);
				}
			}
			Last = Nodes[Parent].Child[Bit];
			if (i >= n - 1)
			{
				int Position = Pass == 0 ? i % n : n - 1 - i % n;
				for (int j = 1; j <= K; ++j)
				{
					int& First = Ending[Position * K + j - 1];
					int Length = Best[Last * K + j - 1];
					if (Pass == 0)
					{
						First = Length;
					}
					else
					{
						Answer[Position] ^= j * std::max(First, Length);
					}
				}
			}
		}
	}
	for (int Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
