// Codex (GPT-6): incremental shortest paths truncated at the specified threshold.
// Logical edges and directed arcs are counted separately for packet decryption.
#include <functional>
#include <queue>
#include <utility>
#include <vector>
#include "buffered-input.hpp"

struct FEdge
{
	int Destination;
	int Weight;
	int Next;
};
class FNetwork
{
public:
	int Limit;
	std::vector<int> Head;
	std::vector<int> Distance;
	std::vector<int> HeadTouched;
	std::vector<int> DistanceTouched;
	std::vector<FEdge> Edges;
	std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> Queue;
	FNetwork(int n, int Threshold) : Limit(Threshold), Head(n + 1, -1), Distance(n + 1, Threshold + 1)
	{
	}
	void Relax(int v, int Value)
	{
		if (Value < Distance[v])
		{
			if (Distance[v] == Limit + 1)
			{
				DistanceTouched.push_back(v);
			}
			Distance[v] = Value;
			Queue.push({Value, v});
		}
	}
	void Add(int u, int v, int Weight)
	{
		if (Head[u] == -1)
		{
			HeadTouched.push_back(u);
		}
		Edges.push_back({v, Weight, Head[u]});
		Head[u] = static_cast<int>(Edges.size()) - 1;
		Relax(v, Distance[u] + Weight);
	}
	void Propagate()
	{
		while (!Queue.empty())
		{
			auto Item = Queue.top();
			Queue.pop();
			int u = Item.second;
			if (Item.first != Distance[u])
			{
				continue;
			}
			for (int Edge = Head[u]; Edge != -1; Edge = Edges[Edge].Next)
			{
				Relax(Edges[Edge].Destination, Distance[u] + Edges[Edge].Weight);
			}
		}
	}
	void Clear()
	{
		for (int u : HeadTouched)
		{
			Head[u] = -1;
		}
		for (int u : DistanceTouched)
		{
			Distance[u] = Limit + 1;
		}
		HeadTouched.clear();
		DistanceTouched.clear();
		Edges.clear();
		Distance[1] = 0;
		DistanceTouched.push_back(1);
	}
};

int main()
{
	FInput Input;
	int n = Input.Read();
	int m = Input.Read();
	int k = Input.Read();
	int Threshold = Input.Read();
	FNetwork Network(n, Threshold);
	for (int i = 0; i < m; ++i)
	{
		int u = Input.Read();
		int v = Input.Read();
		int x = Input.Read();
		int y = Input.Read();
		Network.Add(u, v, x);
		if (y == 1)
		{
			Network.Add(v, u, x);
		}
	}
	Network.Relax(1, 0);
	Network.Propagate();
	int CurrentEdges = m;
	int Deleted = 0;
	for (int c = 1; c <= k; ++c)
	{
		int Key = 1LL * (Deleted + 3) * (c + 37) % 998244353;
		int u = Input.Read() ^ Key;
		int v = Input.Read() ^ Key;
		int x = Input.Read() ^ Key;
		int y = Input.Read() ^ Key;
		Network.Add(u, v, x);
		if (y == 1)
		{
			Network.Add(v, u, x);
		}
		++CurrentEdges;
		Network.Propagate();
		bool bClear = Network.Distance[n] <= Threshold;
		std::printf("%d%c", bClear ? 1 : 0, c == k ? '\n' : ' ');
		if (bClear)
		{
			Deleted += CurrentEdges;
			CurrentEdges = 0;
			Network.Clear();
		}
	}
}
