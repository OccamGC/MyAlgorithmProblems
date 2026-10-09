#include <algorithm>
#include <iostream>
#include <numeric>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

class FBlossomMatching
{
private:

	int n;
	std::vector<std::vector<int>> Edges;
	std::vector<int> Match;
	std::vector<int> Parent;
	std::vector<int> Base;
	std::vector<bool> Used;
	std::vector<bool> Blossom;

	int FindBase(int u, int v)
	{
		std::vector<bool> Seen(n, false);
		while (true)
		{
			u = Base[u];
			Seen[u] = true;
			if (Match[u] == -1)
			{
				break;
			}
			u = Parent[Match[u]];
		}
		while (true)
		{
			v = Base[v];
			if (Seen[v])
			{
				return v;
			}
			v = Parent[Match[v]];
		}
	}

	void MarkPath(int u, int Root, int Child)
	{
		while (Base[u] != Root)
		{
			Blossom[Base[u]] = true;
			Blossom[Base[Match[u]]] = true;
			Parent[u] = Child;
			Child = Match[u];
			u = Parent[Match[u]];
		}
	}

	int FindPath(int Root)
	{
		std::fill(Used.begin(), Used.end(), false);
		std::fill(Parent.begin(), Parent.end(), -1);
		std::iota(Base.begin(), Base.end(), 0);
		std::queue<int> Queue;
		Queue.push(Root);
		Used[Root] = true;
		while (!Queue.empty())
		{
			int u = Queue.front();
			Queue.pop();
			for (int v : Edges[u])
			{
				if (Base[u] == Base[v] || Match[u] == v)
				{
					continue;
				}
				if (v == Root || (Match[v] != -1 && Parent[Match[v]] != -1))
				{
					int RootBase = FindBase(u, v);
					std::fill(Blossom.begin(), Blossom.end(), false);
					MarkPath(u, RootBase, v);
					MarkPath(v, RootBase, u);
					for (int i = 0; i < n; ++i)
					{
						if (Blossom[Base[i]])
						{
							Base[i] = RootBase;
							if (!Used[i])
							{
								Used[i] = true;
								Queue.push(i);
							}
						}
					}
				}
				else if (Parent[v] == -1)
				{
					Parent[v] = u;
					if (Match[v] == -1)
					{
						return v;
					}
					Used[Match[v]] = true;
					Queue.push(Match[v]);
				}
			}
		}
		return -1;
	}

public:

	explicit FBlossomMatching(int Size)
		: n(Size), Edges(n), Match(n, -1), Parent(n), Base(n), Used(n), Blossom(n)
	{
	}

	void AddEdge(int u, int v)
	{
		Edges[u].push_back(v);
		Edges[v].push_back(u);
	}

	int Solve()
	{
		int Answer = 0;
		for (int Root = 0; Root < n; ++Root)
		{
			if (Match[Root] != -1)
			{
				continue;
			}
			int v = FindPath(Root);
			if (v == -1)
			{
				continue;
			}
			++Answer;
			while (v != -1)
			{
				int u = Parent[v];
				int Next = Match[u];
				Match[u] = v;
				Match[v] = u;
				v = Next;
			}
		}
		return Answer;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	FBlossomMatching Solver(n);
	std::unordered_map<std::string, int> Id;
	for (int i = 0; i < m; ++i)
	{
		std::string a;
		std::string b;
		std::cin >> a >> b;
		if (Id.find(a) == Id.end())
		{
			int Next = static_cast<int>(Id.size());
			Id[a] = Next;
		}
		if (Id.find(b) == Id.end())
		{
			int Next = static_cast<int>(Id.size());
			Id[b] = Next;
		}
		Solver.AddEdge(Id[a], Id[b]);
	}
	std::cout << n - Solver.Solve() << '\n';
}
