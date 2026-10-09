#include <iostream>
#include <string>
#include <utility>
#include <vector>

struct FConstraint
{
	int a;
	int b;
	char Operation;
	std::string Result;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<FConstraint> Constraints(m);
	for (FConstraint& Constraint : Constraints)
	{
		std::cin >> Constraint.a >> Constraint.Operation >> Constraint.b >> Constraint.Result;
		--Constraint.a;
		--Constraint.b;
	}
	std::vector<std::string> Answer(n, std::string(k, '0'));
	for (int Bit = 0; Bit < k; ++Bit)
	{
		std::vector<std::vector<int>> Graph(2 * n);
		std::vector<std::vector<int>> Reverse(2 * n);
		auto Add = [&](int u, int v)
		{
			Graph[u].push_back(v);
			Reverse[v].push_back(u);
		};
		for (const FConstraint& Constraint : Constraints)
		{
			for (int s = 0; s <= 1; ++s)
			{
				for (int t = 0; t <= 1; ++t)
				{
					const int Result = Constraint.Operation == '^' ? (s ^ t) :
						(Constraint.Operation == '&' ? (s & t) : (s | t));
					if (Result != Constraint.Result[Bit] - '0')
					{
						Add(2 * Constraint.a + s, 2 * Constraint.b + (1 - t));
						Add(2 * Constraint.b + t, 2 * Constraint.a + (1 - s));
					}
				}
			}
		}
		std::vector<bool> Visited(2 * n);
		std::vector<int> Order;
		for (int Start = 0; Start < 2 * n; ++Start)
		{
			if (Visited[Start])
			{
				continue;
			}
			std::vector<std::pair<int, std::size_t>> Stack = {{Start, 0}};
			Visited[Start] = true;
			while (!Stack.empty())
			{
				const int u = Stack.back().first;
				std::size_t& Index = Stack.back().second;
				if (Index == Graph[u].size())
				{
					Order.push_back(u);
					Stack.pop_back();
				}
				else
				{
					const int v = Graph[u][Index++];
					if (!Visited[v])
					{
						Visited[v] = true;
						Stack.emplace_back(v, 0);
					}
				}
			}
		}
		std::vector<int> Component(2 * n, -1);
		int Count = 0;
		for (auto It = Order.rbegin(); It != Order.rend(); ++It)
		{
			if (Component[*It] != -1)
			{
				continue;
			}
			std::vector<int> Stack = {*It};
			Component[*It] = Count;
			while (!Stack.empty())
			{
				const int u = Stack.back();
				Stack.pop_back();
				for (int v : Reverse[u])
				{
					if (Component[v] == -1)
					{
						Component[v] = Count;
						Stack.push_back(v);
					}
				}
			}
			++Count;
		}
		for (int u = 0; u < n; ++u)
		{
			if (Component[2 * u] == Component[2 * u + 1])
			{
				std::cout << "No\n";
				return 0;
			}
			Answer[u][Bit] = Component[2 * u] < Component[2 * u + 1] ? '1' : '0';
		}
	}
	for (const std::string& Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
