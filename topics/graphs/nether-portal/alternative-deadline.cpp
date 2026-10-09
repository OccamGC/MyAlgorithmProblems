// Codex (GPT-6): binary-search the deadline. Backward Bellman-Ford
// propagates latest departure times; an improving cycle permits arbitrary delay.
#include "portal-graph.hpp"

bool Feasible(const FGraph& Graph, long long Deadline)
{
	int Count = Graph.n + 2;
	std::vector<long long> Latest(Count, -Infinity);
	std::vector<int> Frontier(1, Graph.Target);
	std::vector<int> Next;
	std::vector<int> Enqueued(Count, -1);
	Latest[Graph.Target] = Deadline;
	for (int Round = 0; Round < Count; ++Round)
	{
		Next.clear();
		for (int v : Frontier)
		{
			for (int Id : Graph.Incoming[v])
			{
				const FEdge& e = Graph.Edges[Id];
				if (!Graph.Reachable[e.u])
				{
					continue;
				}
				if (e.bReset)
				{
					return true;
				}
				long long Value = Latest[v] - e.Cost;
				if (Value < Graph.Portals[e.u].Opening || Value <= Latest[e.u])
				{
					continue;
				}
				if (e.u == 0 && Value >= 0)
				{
					return true;
				}
				Latest[e.u] = Value;
				if (Enqueued[e.u] != Round)
				{
					Enqueued[e.u] = Round;
					Next.push_back(e.u);
				}
			}
		}
		if (Next.empty())
		{
			return false;
		}
		Frontier.swap(Next);
	}
	return true;
}
int main()
{
	FGraph Graph;
	Graph.Read();
	if (Graph.Special())
	{
		return 0;
	}
	long long Low = -20000;
	long long High = Graph.Upper[Graph.Target];
	while (Low < High)
	{
		long long Middle = Low + (High - Low) / 2;
		if (Feasible(Graph, Middle))
		{
			High = Middle;
		}
		else
		{
			Low = Middle + 1;
		}
	}
	std::printf("%lld\n", Low);
}
