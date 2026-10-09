// Problem setter's reversed paths and lexicographic neighbours.
// Exact canonical blocks, generation IDs and iterative deletion: GPT-6.
#include <algorithm>
#include <array>
#include <iostream>
#include <iterator>
#include <map>
#include <set>
#include <utility>
#include <vector>

constexpr int Levels = 17;
struct FNode
{
	int Value = 0;
	int Depth = 0;
	int External = 0;
	int ChildCount = 0;
	bool bAlive = true;
	std::array<int, Levels> Up{};
	std::array<int, Levels> Block{};
	std::vector<int> Children;
};

std::vector<FNode> Nodes(1);
std::array<std::map<std::pair<int, int>, int>, Levels> Canonical;

int CommonPrefix(int u, int v)
{
	int Result = 0;
	for (int k = Levels - 1; k >= 0; --k)
	{
		if (Nodes[u].Depth >= (1 << k) && Nodes[v].Depth >= (1 << k)
			&& Nodes[u].Block[k] == Nodes[v].Block[k])
		{
			Result += 1 << k;
			u = Nodes[u].Up[k];
			v = Nodes[v].Up[k];
		}
	}
	return Result;
}

int Ancestor(int u, int Distance)
{
	for (int k = 0; k < Levels; ++k)
	{
		if ((Distance >> k) & 1)
		{
			u = Nodes[u].Up[k];
		}
	}
	return u;
}

struct FCompare
{
	bool operator()(int u, int v) const
	{
		if (u == v)
		{
			return false;
		}
		int Length = CommonPrefix(u, v);
		int Shorter = std::min(Nodes[u].Depth, Nodes[v].Depth);
		if (Length == Shorter)
		{
			return Nodes[u].Depth != Nodes[v].Depth ? Nodes[u].Depth < Nodes[v].Depth : u < v;
		}
		return Nodes[Ancestor(u, Length)].Value < Nodes[Ancestor(v, Length)].Value;
	}
};

int AddNode(int Parent, int External, int Value)
{
	int Index = static_cast<int>(Nodes.size());
	Nodes.emplace_back();
	FNode& Node = Nodes.back();
	Node.Value = Value;
	Node.External = External;
	Node.Depth = Nodes[Parent].Depth + 1;
	Node.Up[0] = Parent;
	Node.Block[0] = Value + 1;
	for (int k = 1; k < Levels && (1 << k) <= Node.Depth; ++k)
	{
		int Middle = Node.Up[k - 1];
		Node.Up[k] = Nodes[Middle].Up[k - 1];
		std::pair<int, int> Key{Node.Block[k - 1], Nodes[Middle].Block[k - 1]};
		auto Result = Canonical[k].emplace(Key, static_cast<int>(Canonical[k].size()) + 1);
		Node.Block[k] = Result.first->second;
	}
	if (Parent != 0)
	{
		Nodes[Parent].Children.push_back(Index);
		++Nodes[Parent].ChildCount;
	}
	return Index;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	Nodes.reserve(n + 2);
	std::vector<int> Current(100001);
	std::set<int, FCompare> Leaves;
	Current[0] = AddNode(0, 0, 0);
	Leaves.insert(Current[0]);
	for (int i = 0; i < n; ++i)
	{
		int Type;
		int a;
		std::cin >> Type >> a;
		int u = Current[a];
		if (Type == 1)
		{
			int b;
			int c;
			std::cin >> b >> c;
			if (Nodes[u].ChildCount == 0)
			{
				Leaves.erase(u);
			}
			Current[b] = AddNode(u, b, c);
			Leaves.insert(Current[b]);
		}
		else if (Type == 2)
		{
			int Parent = Nodes[u].Up[0];
			std::vector<int> Stack{u};
			while (!Stack.empty())
			{
				int v = Stack.back();
				Stack.pop_back();
				if (!Nodes[v].bAlive)
				{
					continue;
				}
				if (Nodes[v].ChildCount == 0)
				{
					Leaves.erase(v);
				}
				for (int Child : Nodes[v].Children)
				{
					if (Nodes[Child].bAlive)
					{
						Stack.push_back(Child);
					}
				}
				Nodes[v].bAlive = false;
				Current[Nodes[v].External] = 0;
			}
			if (Parent != 0 && --Nodes[Parent].ChildCount == 0)
			{
				Leaves.insert(Parent);
			}
		}
		else
		{
			auto Position = Leaves.find(u);
			int Maximum = 0;
			if (Position != Leaves.begin())
			{
				Maximum = CommonPrefix(u, *std::prev(Position));
			}
			auto Next = std::next(Position);
			if (Next != Leaves.end())
			{
				Maximum = std::max(Maximum, CommonPrefix(u, *Next));
			}
			std::cout << Nodes[u].Depth - Maximum << '\n';
		}
	}
}
