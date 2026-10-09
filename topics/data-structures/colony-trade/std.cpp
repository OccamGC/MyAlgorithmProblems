// Original online price-ordered splay tree with clearing/production tags.
// Contribution: Codex (GPT-6): explicit ancestor propagation and 64-bit inventory.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

using FInt = long long;
constexpr FInt Mod = 1000000007;

struct FNode
{
	std::array<int, 2> Child{};
	int Parent = 0;
	FInt Price = 0;
	FInt Rate = 0;
	FInt Stock = 0;
	FInt TotalRate = 0;
	FInt TotalStock = 0;
	FInt Value = 0;
	FInt ProductionValue = 0;
	FInt Time = 0;
	bool bClear = false;
};

class FMarket
{
public:
	std::vector<FNode> Nodes;
	int Root = 0;
	explicit FMarket(int n) : Nodes(n + 1)
	{
	}

	void Pull(int u)
	{
		FNode& Node = Nodes[u];
		const FNode& Left = Nodes[Node.Child[0]];
		const FNode& Right = Nodes[Node.Child[1]];
		Node.TotalRate = Left.TotalRate + Node.Rate + Right.TotalRate;
		Node.TotalStock = Left.TotalStock + Node.Stock + Right.TotalStock;
		Node.Value = (Left.Value + Node.Stock % Mod * Node.Price % Mod + Right.Value) % Mod;
		Node.ProductionValue = (Left.ProductionValue + Node.Rate * Node.Price % Mod + Right.ProductionValue) % Mod;
	}

	void Clear(int u)
	{
		if (u != 0)
		{
			FNode& Node = Nodes[u];
			Node.Stock = Node.TotalStock = Node.Value = Node.Time = 0;
			Node.bClear = true;
		}
	}

	void Produce(int u, FInt Time)
	{
		if (u != 0)
		{
			FNode& Node = Nodes[u];
			Node.Stock += Node.Rate * Time;
			Node.TotalStock += Node.TotalRate * Time;
			Node.Value = (Node.Value + Node.ProductionValue * (Time % Mod)) % Mod;
			Node.Time += Time;
		}
	}

	void Push(int u)
	{
		FNode& Node = Nodes[u];
		if (Node.bClear)
		{
			Clear(Node.Child[0]);
			Clear(Node.Child[1]);
			Node.bClear = false;
		}
		if (Node.Time != 0)
		{
			Produce(Node.Child[0], Node.Time);
			Produce(Node.Child[1], Node.Time);
			Node.Time = 0;
		}
	}

	void Rotate(int u)
	{
		const int Parent = Nodes[u].Parent;
		const int Grandparent = Nodes[Parent].Parent;
		const int Side = Nodes[Parent].Child[1] == u;
		const int Middle = Nodes[u].Child[Side ^ 1];
		if (Grandparent != 0)
		{
			Nodes[Grandparent].Child[Nodes[Grandparent].Child[1] == Parent] = u;
		}
		Nodes[u].Parent = Grandparent;
		Nodes[Parent].Child[Side] = Middle;
		if (Middle != 0)
		{
			Nodes[Middle].Parent = Parent;
		}
		Nodes[u].Child[Side ^ 1] = Parent;
		Nodes[Parent].Parent = u;
		Pull(Parent);
		Pull(u);
	}

	void Splay(int u)
	{
		std::vector<int> Ancestors;
		for (int v = u; v != 0; v = Nodes[v].Parent)
		{
			Ancestors.push_back(v);
		}
		for (auto It = Ancestors.rbegin(); It != Ancestors.rend(); ++It)
		{
			Push(*It);
		}
		while (Nodes[u].Parent != 0)
		{
			const int Parent = Nodes[u].Parent;
			const int Grandparent = Nodes[Parent].Parent;
			if (Grandparent != 0)
			{
				const bool bAligned = (Nodes[Grandparent].Child[1] == Parent) == (Nodes[Parent].Child[1] == u);
				Rotate(bAligned ? Parent : u);
			}
			Rotate(u);
		}
		Root = u;
		Pull(u);
	}

	int Build(const std::vector<int>& Order, int Left, int Right, int Parent)
	{
		if (Left >= Right)
		{
			return 0;
		}
		const int Middle = (Left + Right) / 2;
		const int u = Order[Middle];
		Nodes[u].Parent = Parent;
		Nodes[u].Child[0] = Build(Order, Left, Middle, u);
		Nodes[u].Child[1] = Build(Order, Middle + 1, Right, u);
		Pull(u);
		return u;
	}

	void ChangePrice(int u, FInt Price)
	{
		Splay(u);
		const int Left = Nodes[u].Child[0];
		const int Right = Nodes[u].Child[1];
		if (Left != 0)
		{
			Nodes[Left].Parent = 0;
		}
		if (Right != 0)
		{
			Nodes[Right].Parent = 0;
		}
		if (Left == 0)
		{
			Root = Right;
		}
		else
		{
			Root = Left;
			int Last = Left;
			Push(Last);
			while (Nodes[Last].Child[1] != 0)
			{
				Last = Nodes[Last].Child[1];
				Push(Last);
			}
			Splay(Last);
			Nodes[Root].Child[1] = Right;
			if (Right != 0)
			{
				Nodes[Right].Parent = Root;
			}
			Pull(Root);
		}
		Nodes[u].Child = {};
		Nodes[u].Parent = 0;
		Nodes[u].Price = Price;
		Pull(u);
		if (Root == 0)
		{
			Root = u;
			return;
		}
		int v = Root;
		while (true)
		{
			Push(v);
			const int Side = std::pair<FInt, int>{Price, u} > std::pair<FInt, int>{Nodes[v].Price, v};
			if (Nodes[v].Child[Side] == 0)
			{
				Nodes[v].Child[Side] = u;
				Nodes[u].Parent = v;
				break;
			}
			v = Nodes[v].Child[Side];
		}
		Splay(u);
	}

	FInt Sell(FInt Demand)
	{
		if (Demand == 0)
		{
			return 0;
		}
		FInt Revenue = 0;
		int u = Root;
		while (true)
		{
			Push(u);
			FNode& Node = Nodes[u];
			if (Node.TotalStock <= Demand)
			{
				Revenue = (Revenue + Node.Value) % Mod;
				Clear(u);
				break;
			}
			const int Right = Node.Child[1];
			if (Right != 0 && Nodes[Right].TotalStock >= Demand)
			{
				u = Right;
				continue;
			}
			Demand -= Nodes[Right].TotalStock;
			Revenue = (Revenue + Nodes[Right].Value) % Mod;
			Clear(Right);
			const FInt Taken = std::min(Demand, Node.Stock);
			Revenue = (Revenue + Taken % Mod * Node.Price) % Mod;
			Node.Stock -= Taken;
			Demand -= Taken;
			if (Demand == 0)
			{
				break;
			}
			u = Node.Child[0];
		}
		Splay(u);
		return Revenue;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	FMarket Market(n);
	std::vector<int> Order(n);
	std::iota(Order.begin(), Order.end(), 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Market.Nodes[i].Price >> Market.Nodes[i].Rate;
	}
	std::sort(Order.begin(), Order.end(), [&](int a, int b)
	{
		return std::pair<FInt, int>{Market.Nodes[a].Price, a} < std::pair<FInt, int>{Market.Nodes[b].Price, b};
	});
	Market.Root = Market.Build(Order, 0, n, 0);
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		int Id = 0;
		FInt Value;
		std::cin >> Operation;
		if (Operation >= 3)
		{
			std::cin >> Id;
		}
		std::cin >> Value;
		if (Operation == 1)
		{
			Market.Produce(Market.Root, Value);
		}
		else if (Operation == 2)
		{
			std::cout << Market.Sell(Value) << '\n';
		}
		else if (Operation == 3)
		{
			Market.Splay(Id);
			Market.Nodes[Id].Rate = Value;
			Market.Pull(Id);
		}
		else
		{
			Market.ChangePrice(Id, Value);
		}
	}
}
