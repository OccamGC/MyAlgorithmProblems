// Problem setter's teaching-note solution: globally increasing visit timestamps.
// Codex (GPT-6): C++17 implementation and proof of the current-walk test.

#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Next(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Next[i];
	}
	int Answer = 0;

	std::vector<int> Stamp(n + 1, 0);
	int Clock = 1;
	for (int Start = 1; Start <= n; ++Start)
	{
		if (Stamp[Start] != 0)
		{
			continue;
		}
		const int Begin = Clock;
		int Vertex = Start;
		while (Stamp[Vertex] == 0)
		{
			Stamp[Vertex] = Clock++;
			Vertex = Next[Vertex];
		}
		if (Stamp[Vertex] >= Begin)
		{
			Answer += Clock - Stamp[Vertex];
		}
	}
	std::cout << Answer << '\n';
}
