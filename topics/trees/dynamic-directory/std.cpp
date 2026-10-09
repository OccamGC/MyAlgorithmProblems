// Link-cut tree with a separate weighted node for every edge.
// Codex (GPT-6): rewritten implementation, explicit edge reuse and iterative splay.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

struct FNode
{
	int Child[2] = {0, 0};
	int Parent = 0;
	bool bReverse = false;
	std::int64_t Value = 0;
	std::int64_t Sum = 0;
};

class FLinkCutTree
{
public:
	std::vector<FNode> Nodes;
	std::vector<int> Stack;

	explicit FLinkCutTree(int Count) : Nodes(Count + 1)
	{
		Stack.reserve(Count);
	}

	bool IsAuxiliaryRoot(int x) const
	{
		int p = Nodes[x].Parent;
		return Nodes[p].Child[0] != x && Nodes[p].Child[1] != x;
	}

	void Pull(int x)
	{
		Nodes[x].Sum = Nodes[Nodes[x].Child[0]].Sum + Nodes[x].Value
			+ Nodes[Nodes[x].Child[1]].Sum;
	}

	void Reverse(int x)
	{
		if (x != 0)
		{
			std::swap(Nodes[x].Child[0], Nodes[x].Child[1]);
			Nodes[x].bReverse = !Nodes[x].bReverse;
		}
	}

	void Push(int x)
	{
		if (Nodes[x].bReverse)
		{
			Reverse(Nodes[x].Child[0]);
			Reverse(Nodes[x].Child[1]);
			Nodes[x].bReverse = false;
		}
	}

	void Rotate(int x)
	{
		int p = Nodes[x].Parent;
		int g = Nodes[p].Parent;
		int Side = Nodes[p].Child[1] == x;
		int Middle = Nodes[x].Child[Side ^ 1];
		if (!IsAuxiliaryRoot(p))
		{
			Nodes[g].Child[Nodes[g].Child[1] == p] = x;
		}
		Nodes[x].Parent = g;
		Nodes[p].Child[Side] = Middle;
		if (Middle != 0)
		{
			Nodes[Middle].Parent = p;
		}
		Nodes[x].Child[Side ^ 1] = p;
		Nodes[p].Parent = x;
		Pull(p);
		Pull(x);
	}

	void Splay(int x)
	{
		Stack.clear();
		int v = x;
		Stack.push_back(v);
		while (!IsAuxiliaryRoot(v))
		{
			v = Nodes[v].Parent;
			Stack.push_back(v);
		}
		for (auto It = Stack.rbegin(); It != Stack.rend(); ++It)
		{
			Push(*It);
		}
		while (!IsAuxiliaryRoot(x))
		{
			int p = Nodes[x].Parent;
			int g = Nodes[p].Parent;
			if (!IsAuxiliaryRoot(p))
			{
				bool bAligned = (Nodes[p].Child[1] == x) == (Nodes[g].Child[1] == p);
				Rotate(bAligned ? p : x);
			}
			Rotate(x);
		}
	}

	int Access(int x)
	{
		int Last = 0;
		for (int v = x; v != 0; v = Nodes[v].Parent)
		{
			Splay(v);
			Nodes[v].Child[1] = Last;
			Pull(v);
			Last = v;
		}
		Splay(x);
		return Last;
	}

	void MakeRoot(int x)
	{
		Access(x);
		Reverse(x);
	}

	void Link(int a, int b)
	{
		MakeRoot(a);
		Nodes[a].Parent = b;
	}

	void Cut(int a, int b)
	{
		MakeRoot(a);
		Access(b);
		Nodes[b].Child[0] = 0;
		Nodes[a].Parent = 0;
		Pull(b);
	}

	int Lca(int a, int b)
	{
		Access(a);
		return Access(b);
	}

	int ParentEdge(int a)
	{
		Access(a);
		int v = Nodes[a].Child[0];
		Push(v);
		while (Nodes[v].Child[1] != 0)
		{
			v = Nodes[v].Child[1];
			Push(v);
		}
		Splay(v);
		return v;
	}

	void SetValue(int x, int Value)
	{
		Access(x);
		Nodes[x].Value = Value;
		Pull(x);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	FLinkCutTree Tree(2 * n);
	std::vector<std::pair<int, int>> Endpoints(2 * n + 1);
	std::map<std::pair<int, int>, int> Edges;
	auto Key = [](int a, int b)
	{
		return std::make_pair(std::min(a, b), std::max(a, b));
	};
	for (int i = 1; i < n; ++i)
	{
		int a;
		int b;
		int v;
		std::cin >> a >> b >> v;
		int Edge = n + i;
		Tree.SetValue(Edge, v);
		Tree.Link(a, Edge);
		Tree.Link(Edge, b);
		Endpoints[Edge] = Key(a, b);
		Edges[Key(a, b)] = Edge;
	}
	int Root = 1;
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 2)
		{
			std::cin >> Root;
		}
		else if (Operation == 4)
		{
			int k;
			int Common;
			std::cin >> k >> Common;
			Tree.MakeRoot(Root);
			for (int j = 1; j < k; ++j)
			{
				int a;
				std::cin >> a;
				Common = Tree.Lca(Common, a);
			}
			Tree.Access(Common);
			std::cout << Tree.Nodes[Common].Sum << '\n';
		}
		else
		{
			int a;
			int b;
			int v;
			std::cin >> a >> b >> v;
			if (Operation == 3)
			{
				auto It = Edges.find(Key(a, b));
				if (It != Edges.end())
				{
					Tree.SetValue(It->second, v);
				}
			}
			else
			{
				Tree.MakeRoot(Root);
				if (Tree.Lca(a, b) == a)
				{
					continue;
				}
				int Edge = Tree.ParentEdge(a);
				auto Old = Endpoints[Edge];
				Tree.Cut(Old.first, Edge);
				Tree.Cut(Old.second, Edge);
				Edges.erase(Old);
				Tree.SetValue(Edge, v);
				Tree.Link(a, Edge);
				Tree.Link(Edge, b);
				Endpoints[Edge] = Key(a, b);
				Edges[Key(a, b)] = Edge;
			}
		}
	}
}
