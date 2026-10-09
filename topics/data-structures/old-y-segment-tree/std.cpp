// Codex (GPT-6): previous-strictly-greater chains and binary lifting for online decoded queries.
#include <cstdint>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	int Levels = 1;
	while ((1 << Levels) <= N)
	{
		++Levels;
	}
	std::vector<int> Values(N + 1);
	std::vector<int> Stack;
	std::vector<std::vector<int>> Up(Levels, std::vector<int>(N + 1));
	for (int i = 1; i <= N; ++i)
	{
		std::cin >> Values[i];
		while (!Stack.empty() && Values[Stack.back()] <= Values[i])
		{
			Stack.pop_back();
		}
		Up[0][i] = Stack.empty() ? 0 : Stack.back();
		for (int Level = 1; Level < Levels; ++Level)
		{
			Up[Level][i] = Up[Level - 1][Up[Level - 1][i]];
		}
		Stack.push_back(i);
	}
	std::uint32_t Last = 0;
	while (M--)
	{
		std::uint32_t u;
		std::uint32_t v;
		std::cin >> u >> v;
		int Left = static_cast<int>((u ^ Last) % N) + 1;
		int Right = static_cast<int>((v ^ Last) % N) + 1;
		if (Left > Right)
		{
			std::swap(Left, Right);
		}
		int Answer = 1;
		for (int Level = Levels - 1; Level >= 0; --Level)
		{
			if (Up[Level][Right] >= Left)
			{
				Right = Up[Level][Right];
				Answer += 1 << Level;
			}
		}
		Last = Answer;
		std::cout << Answer << '\n';
	}
}
