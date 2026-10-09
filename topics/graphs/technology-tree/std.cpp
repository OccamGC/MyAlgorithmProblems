// Problem setter's solution: remove completed technologies, topological longest paths.
// Codex (GPT-6): explicit queue and compact adjacency avoid deep call stacks.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Time(n);
	std::vector<int> Head(n, -1);
	std::vector<int> Indegree(n, 0);
	std::vector<int> To;
	std::vector<int> Next;
	To.reserve(m);
	Next.reserve(m);
	std::vector<long long> Finish(n, 0);
	int Remaining = 0;
	for (int& Value : Time)
	{
		std::cin >> Value;
		Remaining += Value != -1;
	}
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		--u;
		--v;
		if (Time[u] != -1 && Time[v] != -1)
		{
			To.push_back(u);
			Next.push_back(Head[v]);
			Head[v] = static_cast<int>(To.size()) - 1;
			++Indegree[u];
		}
	}
	std::vector<int> Queue;
	Queue.reserve(n);
	for (int u = 0; u < n; ++u)
	{
		if (Time[u] != -1 && Indegree[u] == 0)
		{
			Finish[u] = Time[u];
			Queue.push_back(u);
		}
	}
	long long Answer = 0;
	for (std::size_t Position = 0; Position < Queue.size(); ++Position)
	{
		int u = Queue[Position];
		Answer = std::max(Answer, Finish[u]);
		for (int Edge = Head[u]; Edge != -1; Edge = Next[Edge])
		{
			int v = To[Edge];
			Finish[v] = std::max(Finish[v], Finish[u] + Time[v]);
			if (--Indegree[v] == 0)
			{
				Queue.push_back(v);
			}
		}
	}
	if (static_cast<int>(Queue.size()) == Remaining)
	{
		std::cout << Answer << '\n';
	}
	else
	{
		std::cout << "bad idea\n";
	}
}
