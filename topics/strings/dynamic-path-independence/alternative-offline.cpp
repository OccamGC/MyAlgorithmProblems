// Reversed paths and lexicographic neighbours: problem setter.
// Offline exact doubling ranks and generation-aware replay: GPT-6.
#include <algorithm>
#include <array>
#include <iostream>
#include <iterator>
#include <numeric>
#include <set>
#include <utility>
#include <vector>

constexpr int Levels = 18;
struct FNode
{
	int Value = 0;
	int Depth = 0;
	int External = 0;
	int ChildCount = 0;
	bool bAlive = false;
	std::array<int, Levels> Up{};
	std::array<int, Levels> Rank{};
	std::vector<int> Children;
};
struct FOperation
{
	int Type;
	int Vertex;
	int Child;
};
std::vector<FNode> Nodes(1);

int AddNode(int Parent, int External, int Value)
{
	int Index = static_cast<int>(Nodes.size());
	Nodes.emplace_back();
	FNode& Node = Nodes.back();
	Node.Value = Value;
	Node.External = External;
	Node.bAlive = true;
	Node.Depth = Nodes[Parent].Depth + 1;
	Node.Up[0] = Parent;
	Node.Rank[0] = Value + 1;
	for (int k = 1; k < Levels; ++k)
	{
		Node.Up[k] = Nodes[Node.Up[k - 1]].Up[k - 1];
	}
	if (Parent != 0)
	{
		Nodes[Parent].Children.push_back(Index);
	}
	return Index;
}

int CommonPrefix(int u, int v)
{
	int Result = 0;
	for (int k = Levels - 1; k >= 0; --k)
	{
		if (Nodes[u].Depth >= (1 << k) && Nodes[v].Depth >= (1 << k)
			&& Nodes[u].Rank[k] == Nodes[v].Rank[k])
		{
			Result += 1 << k;
			u = Nodes[u].Up[k];
			v = Nodes[v].Up[k];
		}
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	Nodes.reserve(n + 2);
	std::vector<int> Current(100001);
	Current[0] = AddNode(0, 0, 0);
	std::vector<FOperation> Operations;
	Operations.reserve(n);
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
			int v = AddNode(u, b, c);
			Current[b] = v;
			Operations.push_back({Type, u, v});
		}
		else
		{
			Operations.push_back({Type, u, 0});
			if (Type == 2)
			{
				std::vector<int> Stack{u};
				while (!Stack.empty())
				{
					int v = Stack.back();
					Stack.pop_back();
					if (!Nodes[v].bAlive)
					{
						continue;
					}
					for (int Child : Nodes[v].Children)
					{
						Stack.push_back(Child);
					}
					Nodes[v].bAlive = false;
					Current[Nodes[v].External] = 0;
				}
			}
		}
	}
	int Count = static_cast<int>(Nodes.size()) - 1;
	std::vector<int> Order(Count);
	std::iota(Order.begin(), Order.end(), 1);
	for (int k = 1; k < Levels; ++k)
	{
		auto Key = [k](int u)
		{
			return std::make_pair(Nodes[u].Rank[k - 1], Nodes[Nodes[u].Up[k - 1]].Rank[k - 1]);
		};
		std::sort(Order.begin(), Order.end(), [&](int u, int v)
		{
			return Key(u) < Key(v);
		});
		int Rank = 0;
		std::pair<int, int> Previous{-1, -1};
		for (int u : Order)
		{
			auto CurrentKey = Key(u);
			if (CurrentKey != Previous)
			{
				++Rank;
				Previous = CurrentKey;
			}
			Nodes[u].Rank[k] = Rank;
		}
	}
	for (FNode& Node : Nodes)
	{
		Node.bAlive = false;
	}
	auto Key = [](int u)
	{
		return std::make_pair(Nodes[u].Rank[Levels - 1], u);
	};
	std::set<std::pair<int, int>> Leaves{Key(1)};
	Nodes[1].bAlive = true;
	for (const FOperation& Operation : Operations)
	{
		int u = Operation.Vertex;
		if (Operation.Type == 1)
		{
			if (Nodes[u].ChildCount++ == 0)
			{
				Leaves.erase(Key(u));
			}
			Nodes[Operation.Child].bAlive = true;
			Leaves.insert(Key(Operation.Child));
		}
		else if (Operation.Type == 2)
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
					Leaves.erase(Key(v));
				}
				for (int Child : Nodes[v].Children)
				{
					Stack.push_back(Child);
				}
				Nodes[v].bAlive = false;
			}
			if (Parent != 0 && --Nodes[Parent].ChildCount == 0)
			{
				Leaves.insert(Key(Parent));
			}
		}
		else
		{
			auto Position = Leaves.find(Key(u));
			int Maximum = 0;
			if (Position != Leaves.begin())
			{
				Maximum = CommonPrefix(u, std::prev(Position)->second);
			}
			auto Next = std::next(Position);
			if (Next != Leaves.end())
			{
				Maximum = std::max(Maximum, CommonPrefix(u, Next->second));
			}
			std::cout << Nodes[u].Depth - Maximum << '\n';
		}
	}
}

