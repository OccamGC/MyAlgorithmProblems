// Setter's method: bounded label relaxation with predecessor-cycle acceleration.
// Codex (GPT-6): detach reset/floor predecessors immediately, reschedule
// every accelerated vertex, and use 64-bit arithmetic and iterative scans.
#include "portal-graph.hpp"

int main()
{
	FGraph Graph;
	Graph.Read();
	if (Graph.Special())
	{
		return 0;
	}
	int Count = Graph.n + 2;
	std::vector<long long> Distance(Count, Infinity);
	std::vector<int> ParentEdge(Count, -1);
	std::vector<bool> Changed(Count, false);
	std::vector<int> Seen(Count);
	Distance[0] = 0;
	Changed[0] = true;
	while (true)
	{
		bool bProgress = false;
		for (int u = 0; u < Count; ++u)
		{
			if (!Changed[u])
			{
				continue;
			}
			Changed[u] = false;
			for (int Id : Graph.Outgoing[u])
			{
				const FEdge& e = Graph.Edges[Id];
				long long Floor = Graph.Portals[e.v].Opening;
				long long Value = e.bReset ? Floor : std::max(Floor, Distance[u] + e.Cost);
				if (Value < Distance[e.v])
				{
					Distance[e.v] = Value;
					ParentEdge[e.v] = Value == Floor ? -1 : Id;
					Changed[e.v] = true;
					bProgress = true;
				}
			}
		}
		if (!bProgress)
		{
			break;
		}
		std::fill(Seen.begin(), Seen.end(), 0);
		for (int Start = 0; Start < Count; ++Start)
		{
			int u = Start;
			while (u != -1 && Seen[u] == 0)
			{
				Seen[u] = Start + 1;
				u = ParentEdge[u] == -1 ? -1 : Graph.Edges[ParentEdge[u]].u;
			}
			if (u == -1 || Seen[u] != Start + 1)
			{
				continue;
			}
			std::vector<int> Cycle;
			int v = u;
			long long Shift = Infinity;
			do
			{
				Cycle.push_back(v);
				const FEdge& e = Graph.Edges[ParentEdge[v]];
				Shift = std::min(Shift, Distance[e.u] + e.Cost - Graph.Portals[v].Opening);
				v = e.u;
			}
			while (v != u);
			if (Shift > 0)
			{
				for (int Vertex : Cycle)
				{
					Distance[Vertex] -= Shift;
					Changed[Vertex] = true;
				}
			}
		}
	}
	std::printf("%lld\n", Distance[Graph.Target]);
}
