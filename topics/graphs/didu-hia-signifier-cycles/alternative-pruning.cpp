// Codex (GPT-6): apply zero-indegree pruning to count the surviving cycle vertices.

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

	std::vector<int> Indegree(n + 1, 0);
	for (int i = 1; i <= n; ++i)
	{
		++Indegree[Next[i]];
	}
	std::vector<int> Queue;
	for (int i = 1; i <= n; ++i)
	{
		if (Indegree[i] == 0)
		{
			Queue.push_back(i);
		}
	}
	for (std::size_t Head = 0; Head < Queue.size(); ++Head)
	{
		const int Vertex = Next[Queue[Head]];
		if (--Indegree[Vertex] == 0)
		{
			Queue.push_back(Vertex);
		}
	}
	Answer = n - static_cast<int>(Queue.size());
	std::cout << Answer << '\n';
}
