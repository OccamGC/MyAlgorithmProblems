// Problem setter's solution: timestamp cycle counting and removal of 1/2-cycles.
// Codex (GPT-6): C++17 organization and linear-extension sufficiency proof.

#include <iostream>
#include <queue>
#include <vector>

bool CanComplete(const std::vector<int>& Next)
{
	const int n = static_cast<int>(Next.size());
	std::vector<int> Number(n, 0);
	int Timer = 0;
	int CycleVertices = 0;
	for (int Start = 0; Start < n; ++Start)
	{
		if (Number[Start] != 0)
		{
			continue;
		}
		const int Begin = Timer + 1;
		int Current = Start;
		while (Number[Current] == 0)
		{
			Number[Current] = ++Timer;
			Current = Next[Current];
		}
		if (Number[Current] >= Begin)
		{
			CycleVertices += Timer - Number[Current] + 1;
		}
	}
	for (int i = 0; i < n; ++i)
	{
		if (Next[Next[i]] == i)
		{
			--CycleVertices;
		}
	}
	return CycleVertices == 0;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		int N;
		std::cin >> N;
		std::vector<int> Next(N);
		for (int& Destination : Next)
		{
			std::cin >> Destination;
			--Destination;
		}
		std::cout << (CanComplete(Next) ? 'Y' : 'N') << '\n';
	}
}
