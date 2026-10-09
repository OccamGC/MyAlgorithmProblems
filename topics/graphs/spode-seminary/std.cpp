// Problem setter's solution: residual reachability, augmentation, and latest feasible ranks.
// Codex (GPT-6): explicit traversals and portable C++17 implementation.
#include <algorithm>
#include <iostream>
#include <vector>

struct FEdge
{
	int To;
	int Capacity;
};

struct FNetwork
{
	std::vector<FEdge> Edges;
	std::vector<std::vector<int>> Adjacency;

	explicit FNetwork(int Size) : Adjacency(Size)
	{
	}

	void Add(int u, int v, int Capacity)
	{
		Adjacency[u].push_back(static_cast<int>(Edges.size()));
		Edges.push_back({v, Capacity});
		Adjacency[v].push_back(static_cast<int>(Edges.size()));
		Edges.push_back({u, 0});
	}

	void MarkReachable(int Sink, int Rank, std::vector<int>& Last)
	{
		std::vector<int> Queue{Sink};
		Last[Sink] = Rank;
		for (std::size_t i = 0; i < Queue.size(); ++i)
		{
			int u = Queue[i];
			for (int Index : Adjacency[u])
			{
				int v = Edges[Index].To;
				if (Edges[Index ^ 1].Capacity > 0 && Last[v] != Rank)
				{
					Last[v] = Rank;
					Queue.push_back(v);
				}
			}
		}
	}

	void Augment(int Source, int Sink)
	{
		std::vector<int> Previous(Adjacency.size(), -1);
		std::vector<int> Queue{Source};
		Previous[Source] = -2;
		for (std::size_t i = 0; i < Queue.size() && Previous[Sink] == -1; ++i)
		{
			int u = Queue[i];
			for (int Index : Adjacency[u])
			{
				int v = Edges[Index].To;
				if (Edges[Index].Capacity > 0 && Previous[v] == -1)
				{
					Previous[v] = Index;
					Queue.push_back(v);
				}
			}
		}
		for (int v = Sink; v != Source; )
		{
			int Index = Previous[v];
			--Edges[Index].Capacity;
			++Edges[Index ^ 1].Capacity;
			v = Edges[Index ^ 1].To;
		}
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int q;
	std::cin >> n >> m >> q;
	std::vector<int> Satisfaction(n + 1);
	std::vector<int> Capacity(m + 1);
	std::vector<std::vector<int>> Preference(n + 1, std::vector<int>(m + 1));
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Satisfaction[i];
	}
	for (int j = 1; j <= m; ++j)
	{
		std::cin >> Capacity[j];
	}
	for (int i = 1; i <= n; ++i)
	{
		for (int j = 1; j <= m; ++j)
		{
			std::cin >> Preference[i][j];
		}
	}
	while (q--)
	{
		int Sink = 0;
		FNetwork Network(n + m + 1);
		std::vector<int> Last(n + m + 1);
		std::vector<int> Answer(n + 1, -1);
		std::vector<int> Promotion(n + 1, -1);
		std::vector<int> Ranking(n + 1);
		for (int j = 1; j <= m; ++j)
		{
			Network.Add(n + j, Sink, Capacity[j]);
		}
		for (int i = 1; i <= n; ++i)
		{
			std::cin >> Ranking[i];
		}
		for (int Rank = 1; Rank <= n; ++Rank)
		{
			Network.MarkReachable(Sink, Rank, Last);
			int Student = Ranking[Rank];
			int Best = m + 1;
			int Latest = 0;
			for (int j = 1; j <= m; ++j)
			{
				int Tier = Preference[Student][j];
				if (Tier == -1)
				{
					continue;
				}
				if (Tier <= Satisfaction[Student])
				{
					Latest = std::max(Latest, Last[n + j]);
				}
				if (Last[n + j] == Rank)
				{
					Best = std::min(Best, Tier);
				}
			}
			if (Latest > 0)
			{
				Promotion[Student] = Rank - Latest;
			}
			if (Best <= m)
			{
				Answer[Student] = Best;
				for (int j = 1; j <= m; ++j)
				{
					if (Preference[Student][j] == Best && Last[n + j] == Rank)
					{
						Network.Add(Student, n + j, 1);
					}
				}
				Network.Augment(Student, Sink);
			}
		}
		for (int i = 1; i <= n; ++i)
		{
			std::cout << Answer[i] << (i == n ? '\n' : ' ');
		}
		for (int i = 1; i <= n; ++i)
		{
			std::cout << Promotion[i] << (i == n ? '\n' : ' ');
		}
	}
}
