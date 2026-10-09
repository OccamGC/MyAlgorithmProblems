// Setter's portal-state graph; Codex (GPT-6): iterative reachability,
// 64-bit time bounds, and explicit reset edges in negative-time worlds.
#ifndef PORTAL_GRAPH_HPP
#define PORTAL_GRAPH_HPP
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <vector>

constexpr long long Infinity = 4000000000000000000LL;
struct FPortal
{
	int World;
	int x;
	int y;
	int DestinationWorld;
	int DestinationX;
	int DestinationY;
	long long Opening;
	int Delta;
};
struct FEdge
{
	int u;
	int v;
	int Cost;
	bool bReset;
};
struct FGraph
{
	int n;
	int m;
	int Target;
	std::vector<FPortal> Portals;
	std::vector<int> Step;
	std::vector<FEdge> Edges;
	std::vector<std::vector<int>> Outgoing;
	std::vector<std::vector<int>> Incoming;
	std::vector<bool> Reachable;
	std::vector<long long> Upper;
	void Read()
	{
		std::scanf("%d%d", &n, &m);
		Target = n + 1;
		Portals.resize(n + 2);
		Step.resize(m + 1);
		Outgoing.resize(n + 2);
		Incoming.resize(n + 2);
		std::vector<std::vector<int>> Sources(m + 1);
		for (int i : {0, Target})
		{
			FPortal& p = Portals[i];
			std::scanf("%d%d%d", &p.World, &p.x, &p.y);
			p.DestinationWorld = p.World;
			p.DestinationX = p.x;
			p.DestinationY = p.y;
			p.Opening = -Infinity;
			p.Delta = 0;
			Sources[p.World].push_back(i);
		}
		for (int w = 1; w <= m; ++w)
		{
			std::scanf("%d", &Step[w]);
		}
		for (int i = 1; i <= n; ++i)
		{
			FPortal& p = Portals[i];
			std::scanf("%d%d%d%d%d%d%lld%d", &p.World, &p.x, &p.y,
				&p.DestinationWorld, &p.DestinationX, &p.DestinationY, &p.Opening, &p.Delta);
			Sources[p.World].push_back(i);
		}
		for (int i = 0; i <= Target; ++i)
		{
			const FPortal& p = Portals[i];
			for (int j : Sources[p.DestinationWorld])
			{
				const FPortal& q = Portals[j];
				int Cost = p.Delta + Step[p.DestinationWorld]
					* (std::abs(p.DestinationX - q.x) + std::abs(p.DestinationY - q.y));
				int Id = static_cast<int>(Edges.size());
				Edges.push_back({i, j, Cost, Step[p.DestinationWorld] < 0});
				Outgoing[i].push_back(Id);
				Incoming[j].push_back(Id);
			}
		}
		Reachable.assign(n + 2, false);
		Upper.assign(n + 2, Infinity);
		std::vector<int> Queue(1, 0);
		Reachable[0] = true;
		Upper[0] = 0;
		for (std::size_t At = 0; At < Queue.size(); ++At)
		{
			int u = Queue[At];
			for (int Id : Outgoing[u])
			{
				const FEdge& e = Edges[Id];
				if (!Reachable[e.v])
				{
					Reachable[e.v] = true;
					Upper[e.v] = std::max(Portals[e.v].Opening, Upper[u] + e.Cost);
					Queue.push_back(e.v);
				}
			}
		}
	}
	bool Special() const
	{
		if (!Reachable[Target])
		{
			std::puts("YouNeedOpPermission");
			return true;
		}
		if (Step[Portals[Target].World] < 0)
		{
			std::puts("NegativeInfinity");
			return true;
		}
		return false;
	}
};
#endif
