// Problem setter's teaching-note solution: count distinct sufficiently distant destinations.
// Codex (GPT-6): choose doubling rounds from n and count destinations without sorting.

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

	std::vector<int> Buffer(n + 1);
	for (int Steps = 1; Steps < n; Steps *= 2)
	{
		for (int i = 1; i <= n; ++i)
		{
			Buffer[i] = Next[Next[i]];
		}
		Next.swap(Buffer);
	}
	std::vector<bool> Reached(n + 1, false);
	for (int i = 1; i <= n; ++i)
	{
		if (!Reached[Next[i]])
		{
			Reached[Next[i]] = true;
			++Answer;
		}
	}
	std::cout << Answer << '\n';
}
