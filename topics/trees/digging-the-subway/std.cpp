// Codex (GPT-6): exact connected-subtree DP by leaf counts and marked status.
// The setter's greedy has a counterexample; the authorized redesign sets n <= 1000.
#include <algorithm>
#include <cstdio>
#include <vector>
struct FEdge
{
	int v;
	int w;
};
struct FState
{
	int Leaves;
	int Unmarked;
	int HasMark;
	int Degree;
	int Value;
};
int main()
{
	int n;
	int k;
	std::scanf("%d%d", &n, &k);
	std::vector<int> Marked(n);
	for (int i = 0; i < k; ++i)
	{
		int u;
		std::scanf("%d", &u);
		Marked[u - 1] = 1;
	}
	std::vector<std::vector<FEdge>> Graph(n);
	int Total = 0;
	for (int i = 1; i < n; ++i)
	{
		int u;
		int v;
		int w;
		std::scanf("%d%d%d", &u, &v, &w);
		--u;
		--v;
		Graph[u].push_back({v, w});
		Graph[v].push_back({u, w});
		Total += w;
	}
	std::vector<int> Parent(n, -1);
	std::vector<int> Order(1, 0);
	for (std::size_t i = 0; i < Order.size(); ++i)
	{
		int u = Order[i];
		for (FEdge e : Graph[u])
		{
			if (e.v != Parent[u])
			{
				Parent[e.v] = u;
				Order.push_back(e.v);
			}
		}
	}
	int Width = n + 1;
	std::vector<int> Value(Width * Width * 6);
	std::vector<int> Seen(Value.size());
	int Epoch = 0;
	std::vector<int> Keys;
	std::vector<std::vector<FState>> States(n);
	std::vector<int> Answer(n + 1);
	auto Key = [&](int Leaves, int Unmarked, int HasMark, int Degree)
	{
		return ((Leaves * Width + Unmarked) * 2 + HasMark) * 3 + Degree;
	};
	auto Add = [&](int Id, int Score)
	{
		if (Seen[Id] != Epoch)
		{
			Seen[Id] = Epoch;
			Value[Id] = Score;
			Keys.push_back(Id);
		}
		else
		{
			Value[Id] = std::max(Value[Id], Score);
		}
	};
	auto Unpack = [&](int Id)
	{
		int Score = Value[Id];
		int Degree = Id % 3;
		Id /= 3;
		int HasMark = Id % 2;
		Id /= 2;
		return FState{Id / Width, Id % Width, HasMark, Degree, Score};
	};
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		int u = *It;
		std::vector<FState> Current(1, {0, 0, Marked[u], 0, 0});
		for (FEdge e : Graph[u])
		{
			if (e.v == Parent[u])
			{
				continue;
			}
			++Epoch;
			Keys.clear();
			for (FState a : Current)
			{
				Add(Key(a.Leaves, a.Unmarked, a.HasMark, a.Degree), a.Value);
				for (FState b : States[e.v])
				{
					Add(Key(a.Leaves + b.Leaves, a.Unmarked + b.Unmarked,
						a.HasMark | b.HasMark, std::min(2, a.Degree + 1)), a.Value + b.Value + e.w);
				}
			}
			Current.clear();
			for (int Id : Keys)
			{
				Current.push_back(Unpack(Id));
			}
			std::vector<FState>().swap(States[e.v]);
		}
		++Epoch;
		Keys.clear();
		for (FState a : Current)
		{
			if (a.HasMark && a.Degree > 0)
			{
				int Leaves = a.Leaves + (a.Degree == 1);
				int Unmarked = a.Unmarked + (a.Degree == 1 && !Marked[u]);
				int Cost = std::max(Unmarked, (Leaves + 1) / 2);
				Answer[Cost] = std::max(Answer[Cost], a.Value);
			}
			if (a.Degree == 0)
			{
				++a.Leaves;
				a.Unmarked += !Marked[u];
			}
			Add(Key(a.Leaves, a.Unmarked, a.HasMark, 0), a.Value);
		}
		for (int Id : Keys)
		{
			States[u].push_back(Unpack(Id));
		}
	}
	int Need = 1;
	for (int i = 1; i <= n; ++i)
	{
		Answer[i] = std::max(Answer[i], Answer[i - 1]);
		if (Answer[i] == Total)
		{
			Need = i;
			break;
		}
	}
	std::printf("%d\n", Need);
	for (int i = 1; i <= Need; ++i)
	{
		std::printf("%d\n", Answer[i]);
	}
}
