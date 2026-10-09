// Problem setter's nonpositive-edge contraction and Kruskal solution.
// Codex (GPT-6): iterative union by size and C++17 implementation.
// Include all nonpositive edges, then connect their components.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

struct Edge
{
	int a, b, Weight;
};

class DisjointSet
{
public:
	std::vector<int> Parent, Size;
	int Components;
	explicit DisjointSet(int n) : Parent(n + 1), Size(n + 1, 1), Components(n)
	{
		std::iota(Parent.begin(), Parent.end(), 0);
	}
	int Find(int x)
	{
		while (Parent[x] != x)
		{
			Parent[x] = Parent[Parent[x]];
			x = Parent[x];
		}
		return x;
	}
	bool Unite(int a, int b)
	{
		a = Find(a);
		b = Find(b);
		if (a == b)
		{
			return false;
		}
		if (Size[a] < Size[b])
		{
			std::swap(a, b);
		}
		Parent[b] = a;
		Size[a] += Size[b];
		--Components;
		return true;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n, m;
	std::cin >> n >> m;
	DisjointSet Sets(n);
	std::vector<Edge> Edges;
	Edges.reserve(m);
	long long Answer = 0;
	for (int i = 0; i < m; ++i)
	{
		Edge Current;
		std::cin >> Current.a >> Current.b >> Current.Weight;
		if (Current.Weight <= 0)
		{
			Answer += Current.Weight;
			Sets.Unite(Current.a, Current.b);
		}
		else
		{
			Edges.push_back(Current);
		}
	}
	std::sort(Edges.begin(), Edges.end(), [](const Edge& Left, const Edge& Right)
	{
		return Left.Weight < Right.Weight;
	});
	for (const Edge& Current : Edges)
	{
		if (Sets.Unite(Current.a, Current.b))
		{
			Answer += Current.Weight;
		}
	}
	if (Sets.Components == 1)
	{
		std::cout << Answer << '\n';
	}
	else
	{
		std::cout << "bad idea\n";
	}
}
