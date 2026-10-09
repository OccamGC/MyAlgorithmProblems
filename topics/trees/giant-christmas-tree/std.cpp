// Codex (GPT-6): first-removal times via ancestor skipping, then reverse-time diameter unions.
// The setter's centroid-based deletion idea is discussed separately in the solution.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

struct FEdge
{
	int Destination;
	int State;
};

class FTree
{
public:
	std::vector<std::vector<FEdge>> Edges;
	std::vector<int> Parent;
	std::vector<int> Depth;
	std::vector<int> Lit;
	std::vector<int> Order;
	std::vector<std::vector<int>> Up;
	explicit FTree(int n) : Edges(n + 1), Parent(n + 1), Depth(n + 1), Lit(n + 1)
	{
		int Levels = 1;
		while ((1 << Levels) <= n)
		{
			++Levels;
		}
		Up.assign(Levels, std::vector<int>(n + 1));
	}
	void Build()
	{
		Order.push_back(1);
		for (int Index = 0; Index < static_cast<int>(Order.size()); ++Index)
		{
			int u = Order[Index];
			for (FEdge Edge : Edges[u])
			{
				int v = Edge.Destination;
				if (v == Parent[u])
				{
					continue;
				}
				Parent[v] = u;
				Depth[v] = Depth[u] + 1;
				Lit[v] = Edge.State;
				Up[0][v] = u;
				for (int Level = 1; Level < static_cast<int>(Up.size()); ++Level)
				{
					Up[Level][v] = Up[Level - 1][Up[Level - 1][v]];
				}
				Order.push_back(v);
			}
		}
	}
	int Ancestor(int u, int v) const
	{
		if (Depth[u] < Depth[v])
		{
			std::swap(u, v);
		}
		int Difference = Depth[u] - Depth[v];
		for (int Level = 0; Level < static_cast<int>(Up.size()); ++Level)
		{
			if (Difference & (1 << Level))
			{
				u = Up[Level][u];
			}
		}
		if (u == v)
		{
			return u;
		}
		for (int Level = static_cast<int>(Up.size()) - 1; Level >= 0; --Level)
		{
			if (Up[Level][u] != Up[Level][v])
			{
				u = Up[Level][u];
				v = Up[Level][v];
			}
		}
		return Parent[u];
	}
	int Distance(int u, int v) const
	{
		return Depth[u] + Depth[v] - 2 * Depth[Ancestor(u, v)];
	}
};

class FDisjointSet
{
public:
	std::vector<int> Parent;
	explicit FDisjointSet(int n) : Parent(n + 1)
	{
		std::iota(Parent.begin(), Parent.end(), 0);
	}
	int Find(int u)
	{
		int Root = u;
		while (Parent[Root] != Root)
		{
			Root = Parent[Root];
		}
		while (u != Root)
		{
			int Next = Parent[u];
			Parent[u] = Root;
			u = Next;
		}
		return Root;
	}
};

class FDiameters
{
private:
	FDisjointSet Sets;
	std::vector<int> Size;
	std::vector<int> First;
	std::vector<int> Second;
	std::vector<int> Length;
	const FTree& Tree;
public:
	int Maximum = 0;
	FDiameters(int n, const FTree& InTree) : Sets(n), Size(n + 1, 1), First(n + 1), Second(n + 1), Length(n + 1), Tree(InTree)
	{
		std::iota(First.begin(), First.end(), 0);
		std::iota(Second.begin(), Second.end(), 0);
	}
	void Join(int u, int v)
	{
		u = Sets.Find(u);
		v = Sets.Find(v);
		if (u == v)
		{
			return;
		}
		int Best = Length[u];
		int a = First[u];
		int b = Second[u];
		if (Length[v] > Best)
		{
			Best = Length[v];
			a = First[v];
			b = Second[v];
		}
		for (int x : {First[u], Second[u]})
		{
			for (int y : {First[v], Second[v]})
			{
				int Distance = Tree.Distance(x, y);
				if (Distance > Best)
				{
					Best = Distance;
					a = x;
					b = y;
				}
			}
		}
		if (Size[u] < Size[v])
		{
			std::swap(u, v);
		}
		Sets.Parent[v] = u;
		Size[u] += Size[v];
		First[u] = a;
		Second[u] = b;
		Length[u] = Best;
		Maximum = std::max(Maximum, Best);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	FTree Tree(N);
	for (int i = 1; i < N; ++i)
	{
		int u;
		int v;
		int s;
		std::cin >> u >> v >> s;
		Tree.Edges[u].push_back(FEdge{v, s});
		Tree.Edges[v].push_back(FEdge{u, s});
	}
	Tree.Build();
	FDisjointSet Skip(N);
	for (int u : Tree.Order)
	{
		if (u != 1 && !Tree.Lit[u])
		{
			Skip.Parent[u] = Skip.Find(Tree.Parent[u]);
		}
	}
	std::vector<int> RemovedAt(N + 1);
	std::vector<std::vector<int>> Removed(M + 1);
	for (int i = 1; i <= M; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		int Common = Tree.Ancestor(u, v);
		for (int Start : {u, v})
		{
			int Current = Skip.Find(Start);
			while (Tree.Depth[Current] > Tree.Depth[Common])
			{
				RemovedAt[Current] = i;
				Removed[i].push_back(Current);
				Skip.Parent[Current] = Skip.Find(Tree.Parent[Current]);
				Current = Skip.Find(Current);
			}
		}
	}
	FDiameters Components(N, Tree);
	for (int u = 2; u <= N; ++u)
	{
		if (Tree.Lit[u] && RemovedAt[u] == 0)
		{
			Components.Join(u, Tree.Parent[u]);
		}
	}
	std::vector<int> Answers(M + 1);
	for (int i = M; i >= 1; --i)
	{
		Answers[i] = Components.Maximum;
		for (int u : Removed[i])
		{
			Components.Join(u, Tree.Parent[u]);
		}
	}
	for (int i = 1; i <= M; ++i)
	{
		std::cout << Answers[i] << '\n';
	}
}
