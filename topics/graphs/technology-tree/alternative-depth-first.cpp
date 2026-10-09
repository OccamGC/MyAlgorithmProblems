// Codex (GPT-6): apply three-state depth-first dynamic programming on dependencies.
// Explicit frames avoid recursion; gray edges detect dependency cycles.
#include <algorithm>
#include <iostream>
#include <vector>

struct FFrame
{
	int Vertex;
	int Edge;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Time(n);
	std::vector<int> Head(n, -1);
	std::vector<int> To;
	std::vector<int> Next;
	To.reserve(m);
	Next.reserve(m);
	for (int& Value : Time)
	{
		std::cin >> Value;
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
			To.push_back(v);
			Next.push_back(Head[u]);
			Head[u] = static_cast<int>(To.size()) - 1;
		}
	}
	std::vector<unsigned char> State(n, 0);
	std::vector<long long> Finish(n, 0);
	std::vector<FFrame> Stack;
	Stack.reserve(n);
	long long Answer = 0;
	for (int Start = 0; Start < n; ++Start)
	{
		if (Time[Start] == -1 || State[Start] != 0)
		{
			continue;
		}
		State[Start] = 1;
		Stack.push_back({Start, Head[Start]});
		while (!Stack.empty())
		{
			int u = Stack.back().Vertex;
			int Edge = Stack.back().Edge;
			if (Edge == -1)
			{
				Finish[u] += Time[u];
				Answer = std::max(Answer, Finish[u]);
				State[u] = 2;
				Stack.pop_back();
				continue;
			}
			int v = To[Edge];
			if (State[v] == 1)
			{
				std::cout << "bad idea\n";
				return 0;
			}
			if (State[v] == 0)
			{
				State[v] = 1;
				Stack.push_back({v, Head[v]});
			}
			else
			{
				Finish[u] = std::max(Finish[u], Finish[v]);
				Stack.back().Edge = Next[Edge];
			}
		}
	}
	std::cout << Answer << '\n';
}
