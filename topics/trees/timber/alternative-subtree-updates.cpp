// DFS-order segment tree. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

struct FPeak
{
	int Depth = 0;
	int Vertex = 0;
};

class FDepthTree
{
	int Base = 1;
	std::vector<FPeak> Peak;
	std::vector<int> Tag;
	void Pull(int u)
	{
		Peak[u] = Peak[2 * u].Depth >= Peak[2 * u + 1].Depth ? Peak[2 * u] : Peak[2 * u + 1];
		Peak[u].Depth += Tag[u];
	}
	void Subtract(int u, int l, int r, int a, int b)
	{
		if (a <= l && r <= b)
		{
			--Tag[u];
			--Peak[u].Depth;
			return;
		}
		int Mid = (l + r) / 2;
		if (a < Mid)
		{
			Subtract(2 * u, l, Mid, a, b);
		}
		if (Mid < b)
		{
			Subtract(2 * u + 1, Mid, r, a, b);
		}
		Pull(u);
	}
public:
	explicit FDepthTree(const std::vector<FPeak>& Values)
	{
		while (Base < static_cast<int>(Values.size()))
		{
			Base *= 2;
		}
		Peak.resize(2 * Base);
		Tag.resize(2 * Base);
		std::copy(Values.begin(), Values.end(), Peak.begin() + Base);
		for (int i = Base - 1; i > 0; --i)
		{
			Pull(i);
		}
	}
	FPeak Top() const
	{
		return Peak[1];
	}
	void Subtract(int a, int b)
	{
		Subtract(1, 0, Base, a, b);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::vector<int>> Graph(n + 1);
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	std::vector<int> Parent(n + 1, -1);
	std::vector<int> Entry(n + 1);
	std::vector<int> Size(n + 1, 1);
	std::vector<int> Depth(n + 1, 1);
	std::vector<char> Used(n + 1);
	Used[0] = true;
	std::vector<std::pair<int, bool>> Gains;
	for (int Root = 1; Root <= n; ++Root)
	{
		if (Parent[Root] != -1)
		{
			continue;
		}
		Parent[Root] = 0;
		std::vector<int> Stack{Root};
		std::vector<FPeak> Order;
		while (!Stack.empty())
		{
			int u = Stack.back();
			Stack.pop_back();
			Entry[u] = static_cast<int>(Order.size());
			Order.push_back({Depth[u], u});
			for (int v : Graph[u])
			{
				if (Parent[v] == -1)
				{
					Parent[v] = u;
					Depth[v] = Depth[u] + 1;
					Stack.push_back(v);
				}
			}
		}
		for (auto It = Order.rbegin(); It != Order.rend(); ++It)
		{
			Size[Parent[It->Vertex]] += Size[It->Vertex];
		}
		FDepthTree Tree(Order);
		while (Tree.Top().Depth > 0)
		{
			const FPeak Peak = Tree.Top();
			Gains.emplace_back(Peak.Depth, !Used[Root]);
			for (int u = Peak.Vertex; !Used[u]; u = Parent[u])
			{
				Used[u] = true;
				Tree.Subtract(Entry[u], Entry[u] + Size[u]);
			}
		}
	}
	std::sort(Gains.begin(), Gains.end(), [](const auto& Left, const auto& Right)
	{
		if (Left.first != Right.first)
		{
			return Left.first > Right.first;
		}
		return Left.second < Right.second;
	});
	std::cout << Gains.size() << '\n';
	int Cut = 0;
	int Trees = 0;
	for (const auto& Gain : Gains)
	{
		Cut += Gain.first;
		Trees += Gain.second;
		std::cout << Cut << ' ' << Trees << '\n';
	}
}
