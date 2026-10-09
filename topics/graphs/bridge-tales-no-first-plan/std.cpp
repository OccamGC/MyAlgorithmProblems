#include <algorithm>
#include <array>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <utility>
#include <vector>

constexpr int MaxLog = 18;

struct FEdge
{
	int u;
	int v;
	int w;
	bool bInTree = false;
};

struct FTopTwo
{
	int First = -1;
	int Second = -1;

	void Add(int Value)
	{
		if (Value < 0 || Value == First || Value == Second)
		{
			return;
		}
		if (Value > First)
		{
			Second = First;
			First = Value;
		}
		else if (Value > Second)
		{
			Second = Value;
		}
	}

	void Merge(const FTopTwo& Other)
	{
		Add(Other.First);
		Add(Other.Second);
	}
};

struct FDisjointSet
{
	std::vector<int> Parent;
	std::vector<int> Size;

	explicit FDisjointSet(int n) : Parent(n + 1), Size(n + 1, 1)
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

	bool TryUnite(int a, int b)
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
		return true;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	int m;
	if (!(std::cin >> n >> m))
	{
		return 0;
	}
	std::vector<FEdge> Edges(m);
	for (FEdge& Edge : Edges)
	{
		std::cin >> Edge.u >> Edge.v >> Edge.w;
	}

	std::vector<int> Order(m);
	std::iota(Order.begin(), Order.end(), 0);
	std::sort(Order.begin(), Order.end(), [&](int a, int b)
	{
		return Edges[a].w < Edges[b].w;
	});

	FDisjointSet DisjointSet(n);
	std::vector<std::vector<std::pair<int, int>>> Tree(n + 1);
	long long Minimum = 0;
	for (int Id : Order)
	{
		FEdge& Edge = Edges[Id];
		if (!DisjointSet.TryUnite(Edge.u, Edge.v))
		{
			continue;
		}
		Edge.bInTree = true;
		Minimum += Edge.w;
		Tree[Edge.u].push_back({Edge.v, Edge.w});
		Tree[Edge.v].push_back({Edge.u, Edge.w});
	}

	std::vector<int> Depth(n + 1, -1);
	std::vector<std::array<int, MaxLog>> Up(n + 1);
	std::vector<std::array<FTopTwo, MaxLog>> Top(n + 1);
	std::queue<int> Bfs;
	Depth[1] = 0;
	for (int Level = 0; Level < MaxLog; ++Level)
	{
		Up[1][Level] = 1;
	}
	Bfs.push(1);
	while (!Bfs.empty())
	{
		int u = Bfs.front();
		Bfs.pop();
		for (auto [v, Weight] : Tree[u])
		{
			if (Depth[v] != -1)
			{
				continue;
			}
			Depth[v] = Depth[u] + 1;
			Up[v][0] = u;
			Top[v][0].Add(Weight);
			for (int Level = 1; Level < MaxLog; ++Level)
			{
				int Middle = Up[v][Level - 1];
				Up[v][Level] = Up[Middle][Level - 1];
				Top[v][Level] = Top[v][Level - 1];
				Top[v][Level].Merge(Top[Middle][Level - 1]);
			}
			Bfs.push(v);
		}
	}

	auto PathTop = [&](int a, int b)
	{
		FTopTwo Result;
		if (Depth[a] < Depth[b])
		{
			std::swap(a, b);
		}
		int Gap = Depth[a] - Depth[b];
		for (int Level = 0; Level < MaxLog; ++Level)
		{
			if ((Gap >> Level) & 1)
			{
				Result.Merge(Top[a][Level]);
				a = Up[a][Level];
			}
		}
		if (a == b)
		{
			return Result;
		}
		for (int Level = MaxLog - 1; Level >= 0; --Level)
		{
			if (Up[a][Level] != Up[b][Level])
			{
				Result.Merge(Top[a][Level]);
				Result.Merge(Top[b][Level]);
				a = Up[a][Level];
				b = Up[b][Level];
			}
		}
		Result.Merge(Top[a][0]);
		Result.Merge(Top[b][0]);
		return Result;
	};

	long long Answer = std::numeric_limits<long long>::max();
	for (const FEdge& Edge : Edges)
	{
		if (Edge.bInTree)
		{
			continue;
		}
		FTopTwo Path = PathTop(Edge.u, Edge.v);
		int Removed = Path.First < Edge.w ? Path.First : Path.Second;
		if (Removed >= 0 && Removed < Edge.w)
		{
			Answer = std::min(Answer, Minimum + Edge.w - Removed);
		}
	}
	std::cout << Answer << '\n';
}
