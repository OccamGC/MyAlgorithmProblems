// Problem setter's centroid decomposition and maximum-weight closure.
// Iterative traversals/flow, 64-bit capacities and pruning proof: GPT-6.
#include <algorithm>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

struct FEdge
{
	int To;
	long long Capacity;
};
class FFlow
{
private:
	std::vector<std::vector<int>> Graph;
	std::vector<FEdge> Edges;
	std::vector<int> Level;
	std::vector<int> Current;
	struct FFrame
	{
		int Vertex;
		long long Limit;
		long long Sent;
		int Incoming;
	};
	bool BuildLevels(int Source, int Sink)
	{
		std::fill(Level.begin(), Level.end(), -1);
		std::queue<int> Queue;
		Level[Source] = 0;
		Queue.push(Source);
		while (!Queue.empty())
		{
			int u = Queue.front();
			Queue.pop();
			for (int e : Graph[u])
			{
				int v = Edges[e].To;
				if (Edges[e].Capacity > 0 && Level[v] < 0)
				{
					Level[v] = Level[u] + 1;
					Queue.push(v);
				}
			}
		}
		return Level[Sink] >= 0;
	}
	long long BlockingFlow(int Source, int Sink, long long Limit)
	{
		std::vector<FFrame> Stack{{Source, Limit, 0, -1}};
		Stack.reserve(Graph.size());
		while (!Stack.empty())
		{
			FFrame& Frame = Stack.back();
			int u = Frame.Vertex;
			if (u == Sink || Frame.Sent == Frame.Limit || Current[u] == static_cast<int>(Graph[u].size()))
			{
				long long Sent = u == Sink ? Frame.Limit : Frame.Sent;
				int Incoming = Frame.Incoming;
				Stack.pop_back();
				if (Stack.empty())
				{
					return Sent;
				}
				Edges[Incoming].Capacity -= Sent;
				Edges[Incoming ^ 1].Capacity += Sent;
				FFrame& Parent = Stack.back();
				Parent.Sent += Sent;
				if (Parent.Sent < Parent.Limit)
				{
					++Current[Parent.Vertex];
				}
				continue;
			}
			int e = Graph[u][Current[u]];
			int v = Edges[e].To;
			if (Edges[e].Capacity > 0 && Level[v] == Level[u] + 1)
			{
				long long Available = std::min(Frame.Limit - Frame.Sent, Edges[e].Capacity);
				Stack.push_back({v, Available, 0, e});
			}
			else
			{
				++Current[u];
			}
		}
		return 0;
	}
public:
	explicit FFlow(int n) : Graph(n), Level(n), Current(n)
	{
	}
	void Add(int u, int v, long long Capacity)
	{
		int Index = static_cast<int>(Edges.size());
		Graph[u].push_back(Index);
		Graph[v].push_back(Index + 1);
		Edges.push_back({v, Capacity});
		Edges.push_back({u, 0});
	}
	long long Maximum(int Source, int Sink, long long Limit)
	{
		long long Result = 0;
		while (BuildLevels(Source, Sink))
		{
			std::fill(Current.begin(), Current.end(), 0);
			Result += BlockingFlow(Source, Sink, Limit);
		}
		return Result;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<long long> Weight(n + 1);
	for (int u = 1; u <= n; ++u)
	{
		std::cin >> Weight[u];
	}
	std::vector<std::vector<std::vector<int>>> Trees(m, std::vector<std::vector<int>>(n + 1));
	for (int j = 0; j < m; ++j)
	{
		for (int i = 1; i < n; ++i)
		{
			int u;
			int v;
			std::cin >> u >> v;
			Trees[j][u].push_back(v);
			Trees[j][v].push_back(u);
		}
	}
	std::vector<bool> Removed(n + 1);
	std::vector<int> Membership(n + 1);
	std::vector<int> Size(n + 1);
	std::vector<int> FirstParent(n + 1);
	std::vector<int> Local(n + 1);
	std::vector<bool> Valid(n + 1);
	std::vector<std::vector<int>> Parent(m, std::vector<int>(n + 1));
	std::vector<int> Tasks{1};
	int Stamp = 0;
	long long Answer = 0;
	while (!Tasks.empty())
	{
		int Start = Tasks.back();
		Tasks.pop_back();
		++Stamp;
		std::vector<int> Component{Start};
		FirstParent[Start] = 0;
		for (std::size_t i = 0; i < Component.size(); ++i)
		{
			int u = Component[i];
			Membership[u] = Stamp;
			Size[u] = 1;
			Valid[u] = true;
			for (int v : Trees[0][u])
			{
				if (!Removed[v] && v != FirstParent[u])
				{
					FirstParent[v] = u;
					Component.push_back(v);
				}
			}
		}
		int Count = static_cast<int>(Component.size());
		int Center = Start;
		for (int i = Count - 1; i >= 0; --i)
		{
			int u = Component[i];
			int Largest = 0;
			for (int v : Trees[0][u])
			{
				if (!Removed[v] && FirstParent[v] == u)
				{
					Size[u] += Size[v];
					Largest = std::max(Largest, Size[v]);
				}
			}
			Largest = std::max(Largest, Count - Size[u]);
			if (2 * Largest <= Count)
			{
				Center = u;
			}
		}
		for (int j = 0; j < m; ++j)
		{
			for (int u : Component)
			{
				Parent[j][u] = -1;
			}
			Parent[j][Center] = 0;
			std::vector<int> Queue{Center};
			for (std::size_t i = 0; i < Queue.size(); ++i)
			{
				int u = Queue[i];
				for (int v : Trees[j][u])
				{
					if (Membership[v] == Stamp && Parent[j][v] == -1)
					{
						Parent[j][v] = u;
						Queue.push_back(v);
					}
				}
			}
		}
		std::vector<int> Deleted;
		for (int u : Component)
		{
			for (int j = 0; j < m; ++j)
			{
				if (Parent[j][u] == -1)
				{
					Valid[u] = false;
					Deleted.push_back(u);
					break;
				}
			}
		}
		for (std::size_t i = 0; i < Deleted.size(); ++i)
		{
			int u = Deleted[i];
			for (int j = 0; j < m; ++j)
			{
				for (int v : Trees[j][u])
				{
					if (Membership[v] == Stamp && Valid[v] && Parent[j][v] == u)
					{
						Valid[v] = false;
						Deleted.push_back(v);
					}
				}
			}
		}
		int Remaining = 0;
		long long Positive = 0;
		for (int u : Component)
		{
			if (Valid[u])
			{
				Local[u] = Remaining++;
				Positive += std::max(Weight[u], 0LL);
			}
		}
		if (Positive > Answer)
		{
			int Source = Remaining;
			int Sink = Remaining + 1;
			FFlow Flow(Remaining + 2);
			for (int u : Component)
			{
				if (!Valid[u])
				{
					continue;
				}
				if (Weight[u] > 0)
				{
					Flow.Add(Source, Local[u], Weight[u]);
				}
				else if (Weight[u] < 0)
				{
					Flow.Add(Local[u], Sink, -Weight[u]);
				}
				for (int j = 0; j < m; ++j)
				{
					int v = Parent[j][u];
					if (v > 0)
					{
						Flow.Add(Local[u], Local[v], Positive + 1);
					}
				}
			}
			Answer = std::max(Answer, Positive - Flow.Maximum(Source, Sink, Positive + 1));
		}
		Removed[Center] = true;
		for (int v : Trees[0][Center])
		{
			if (!Removed[v])
			{
				Tasks.push_back(v);
			}
		}
	}
	std::cout << Answer << '\n';
}

