// Codex (GPT-6): minimum-cost flow for expense, and maximum remaining fuel per stop count.
#include <algorithm>
#include <functional>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

struct FStation
{
	int Position;
	long long Price;
	long long Stock;
};

struct FEdge
{
	int Destination;
	int Reverse;
	int Capacity;
	long long Cost;
};

class FMinCostFlow
{
private:
	std::vector<std::vector<FEdge>> Graph;
public:
	explicit FMinCostFlow(int Size) : Graph(Size)
	{
	}
	void Add(int u, int v, int Capacity, long long Cost)
	{
		int From = static_cast<int>(Graph[u].size());
		int To = static_cast<int>(Graph[v].size());
		Graph[u].push_back(FEdge{v, To, Capacity, Cost});
		Graph[v].push_back(FEdge{u, From, 0, -Cost});
	}
	long long Solve(int Source, int Sink, int Required)
	{
		int Size = static_cast<int>(Graph.size());
		constexpr long long Infinity = 4000000000000000000LL;
		std::vector<long long> Potential(Size);
		long long Answer = 0;
		while (Required > 0)
		{
			std::vector<long long> Distance(Size, Infinity);
			std::vector<int> PreviousVertex(Size);
			std::vector<int> PreviousEdge(Size);
			using FEntry = std::pair<long long, int>;
			std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Queue;
			Distance[Source] = 0;
			Queue.push({0, Source});
			while (!Queue.empty())
			{
				FEntry Entry = Queue.top();
				Queue.pop();
				int u = Entry.second;
				if (Entry.first != Distance[u])
				{
					continue;
				}
				for (int i = 0; i < static_cast<int>(Graph[u].size()); ++i)
				{
					const FEdge& Edge = Graph[u][i];
					int v = Edge.Destination;
					long long Candidate = Distance[u] + Edge.Cost + Potential[u] - Potential[v];
					if (Edge.Capacity > 0 && Candidate < Distance[v])
					{
						Distance[v] = Candidate;
						PreviousVertex[v] = u;
						PreviousEdge[v] = i;
						Queue.push({Candidate, v});
					}
				}
			}
			if (Distance[Sink] == Infinity)
			{
				return -1;
			}
			for (int u = 0; u < Size; ++u)
			{
				if (Distance[u] != Infinity)
				{
					Potential[u] += Distance[u];
				}
			}
			int Amount = Required;
			for (int v = Sink; v != Source; v = PreviousVertex[v])
			{
				Amount = std::min(Amount, Graph[PreviousVertex[v]][PreviousEdge[v]].Capacity);
			}
			for (int v = Sink; v != Source; v = PreviousVertex[v])
			{
				FEdge& Edge = Graph[PreviousVertex[v]][PreviousEdge[v]];
				Answer += Amount * Edge.Cost;
				Edge.Capacity -= Amount;
				Graph[v][Edge.Reverse].Capacity += Amount;
			}
			Required -= Amount;
		}
		return Answer;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int L;
	int R;
	std::cin >> N >> L >> R;
	int Capacity = R == -1 ? L : R;
	std::vector<FStation> Stations(N);
	for (FStation& Station : Stations)
	{
		std::cin >> Station.Position >> Station.Price >> Station.Stock;
	}
	std::sort(Stations.begin(), Stations.end(), [](const FStation& Left, const FStation& Right)
	{
		return Left.Position < Right.Position;
	});
	if (Stations.empty() || Stations.front().Position != 0)
	{
		Stations.insert(Stations.begin(), FStation{0, 0, 0});
	}
	Stations.push_back(FStation{L, 0, 0});
	int Count = static_cast<int>(Stations.size());
	int Source = Count;
	int Sink = Count + 1;
	FMinCostFlow Flow(Count + 2);
	for (int i = 0; i + 1 < Count; ++i)
	{
		int Distance = Stations[i + 1].Position - Stations[i].Position;
		if (Distance > Capacity)
		{
			std::cout << "-1\n-1\n";
			return 0;
		}
		Flow.Add(Source, i, static_cast<int>(std::min<long long>(Stations[i].Stock, Capacity)), Stations[i].Price);
		Flow.Add(i, Sink, Distance, 0);
		Flow.Add(i, i + 1, Capacity - Distance, 0);
	}
	long long Cost = Flow.Solve(Source, Sink, L);
	std::vector<int> Fuel(Count + 1, -1);
	Fuel[0] = 0;
	for (int i = 0; i + 1 < Count; ++i)
	{
		int Stock = static_cast<int>(std::min<long long>(Stations[i].Stock, Capacity));
		if (Stock > 0)
		{
			for (int Stops = i; Stops >= 0; --Stops)
			{
				if (Fuel[Stops] >= 0 && Fuel[Stops] < Capacity)
				{
					Fuel[Stops + 1] = std::max(Fuel[Stops + 1], std::min(Capacity, Fuel[Stops] + Stock));
				}
			}
		}
		int Distance = Stations[i + 1].Position - Stations[i].Position;
		for (int& Value : Fuel)
		{
			Value = Value >= Distance ? Value - Distance : -1;
		}
	}
	int Answer = -1;
	for (int Stops = 0; Stops <= Count; ++Stops)
	{
		if (Fuel[Stops] >= 0)
		{
			Answer = Stops;
			break;
		}
	}
	std::cout << Cost << '\n' << Answer << '\n';
}
