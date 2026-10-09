#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

constexpr long long Mod = 1000000007;

struct FNode
{
	long long Stock = 0;
	long long Production = 0;
	long long Value = 0;
	long long ProductionValue = 0;
	long long Time = 0;
	bool bClear = false;
};

class FSegmentTree
{
public:
	explicit FSegmentTree(const std::vector<std::pair<int, int>>& InKeys)
		: Keys(InKeys), Nodes(4 * InKeys.size())
	{
	}

	void Produce(int u, long long t)
	{
		auto& Node = Nodes[u];
		Node.Stock += Node.Production * t;
		Node.Value = (Node.Value + Node.ProductionValue * (t % Mod)) % Mod;
		Node.Time += t;
	}

	void Clear(int u)
	{
		Nodes[u].Stock = 0;
		Nodes[u].Value = 0;
		Nodes[u].Time = 0;
		Nodes[u].bClear = true;
	}

	void Push(int u)
	{
		if (Nodes[u].bClear)
		{
			Clear(2 * u);
			Clear(2 * u + 1);
			Nodes[u].bClear = false;
		}
		if (Nodes[u].Time != 0)
		{
			Produce(2 * u, Nodes[u].Time);
			Produce(2 * u + 1, Nodes[u].Time);
			Nodes[u].Time = 0;
		}
	}

	void Pull(int u)
	{
		Nodes[u].Stock = Nodes[2 * u].Stock + Nodes[2 * u + 1].Stock;
		Nodes[u].Production = Nodes[2 * u].Production + Nodes[2 * u + 1].Production;
		Nodes[u].Value = (Nodes[2 * u].Value + Nodes[2 * u + 1].Value) % Mod;
		Nodes[u].ProductionValue = (Nodes[2 * u].ProductionValue + Nodes[2 * u + 1].ProductionValue) % Mod;
	}

	// A negative Stock argument preserves the current stock at this leaf.
	long long Set(int u, int l, int r, int Position, long long Stock, long long Production)
	{
		if (l == r)
		{
			const long long Previous = Nodes[u].Stock;
			Nodes[u] = FNode{};
			Nodes[u].Stock = Stock < 0 ? Previous : Stock;
			Nodes[u].Production = Production;
			Nodes[u].Value = Nodes[u].Stock % Mod * Keys[l].first % Mod;
			Nodes[u].ProductionValue = Production * Keys[l].first % Mod;
			return Previous;
		}
		Push(u);
		const int Mid = (l + r) / 2;
		const long long Previous = Position <= Mid ? Set(2 * u, l, Mid, Position, Stock, Production) : Set(2 * u + 1, Mid + 1, r, Position, Stock, Production);
		Pull(u);
		return Previous;
	}

	long long Sell(int u, int l, int r, long long& k)
	{
		if (k == 0)
		{
			return 0;
		}
		if (Nodes[u].Stock <= k)
		{
			const long long Result = Nodes[u].Value;
			k -= Nodes[u].Stock;
			Clear(u);
			return Result;
		}
		if (l == r)
		{
			const long long Result = k % Mod * Keys[l].first % Mod;
			Nodes[u].Stock -= k;
			Nodes[u].Value = (Nodes[u].Value - Result + Mod) % Mod;
			k = 0;
			return Result;
		}
		Push(u);
		const int Mid = (l + r) / 2;
		long long Result = Sell(2 * u + 1, Mid + 1, r, k);
		Result = (Result + Sell(2 * u, l, Mid, k)) % Mod;
		Pull(u);
		return Result;
	}

private:
	const std::vector<std::pair<int, int>>& Keys;
	std::vector<FNode> Nodes;
};

struct FOperation
{
	int Type;
	int Id = 0;
	long long Value;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Price(n + 1);
	std::vector<int> Production(n + 1);
	std::vector<std::pair<int, int>> Keys;
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Price[i] >> Production[i];
		Keys.emplace_back(Price[i], i);
	}
	std::vector<FOperation> Operations(m);
	for (auto& Operation : Operations)
	{
		std::cin >> Operation.Type;
		if (Operation.Type >= 3)
		{
			std::cin >> Operation.Id;
		}
		std::cin >> Operation.Value;
		if (Operation.Type == 4)
		{
			Keys.emplace_back(static_cast<int>(Operation.Value), Operation.Id);
		}
	}
	std::sort(Keys.begin(), Keys.end());
	Keys.erase(std::unique(Keys.begin(), Keys.end()), Keys.end());
	const int Last = static_cast<int>(Keys.size()) - 1;
	auto Position = [&](int i)
	{
		return static_cast<int>(std::lower_bound(Keys.begin(), Keys.end(), std::pair<int, int>{Price[i], i}) - Keys.begin());
	};
	FSegmentTree Tree(Keys);
	for (int i = 1; i <= n; ++i)
	{
		Tree.Set(1, 0, Last, Position(i), 0, Production[i]);
	}
	for (const auto& Operation : Operations)
	{
		const int i = Operation.Id;
		if (Operation.Type == 1)
		{
			Tree.Produce(1, Operation.Value);
		}
		else if (Operation.Type == 2)
		{
			long long k = Operation.Value;
			std::cout << Tree.Sell(1, 0, Last, k) << '\n';
		}
		else if (Operation.Type == 3)
		{
			Production[i] = static_cast<int>(Operation.Value);
			Tree.Set(1, 0, Last, Position(i), -1, Production[i]);
		}
		else
		{
			const long long Stock = Tree.Set(1, 0, Last, Position(i), 0, 0);
			Price[i] = static_cast<int>(Operation.Value);
			Tree.Set(1, 0, Last, Position(i), Stock, Production[i]);
		}
	}
}
