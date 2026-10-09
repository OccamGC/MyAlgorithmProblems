#ifndef NOMADISM_NIGHT_MST_HPP
#define NOMADISM_NIGHT_MST_HPP

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <stdexcept>
#include <utility>
#include <vector>

struct FPoint
{
	int x;
	int y;
	int Id;
};

inline std::int64_t Distance(const FPoint& a, const FPoint& b)
{
	return std::abs(a.x - b.x) + std::abs(a.y - b.y);
}

struct FTree
{
	std::int64_t Weight = 0;
	std::vector<std::pair<int, int>> Edges;
};

struct FDisjointSet
{
	std::vector<int> Parent;

	explicit FDisjointSet(int n) : Parent(n, -1)
	{
	}

	int Find(int u)
	{
		int Root = u;
		while (Parent[Root] >= 0)
		{
			Root = Parent[Root];
		}
		while (u != Root)
		{
			const int Next = Parent[u];
			Parent[u] = Root;
			u = Next;
		}
		return Root;
	}

	bool Unite(int u, int v)
	{
		u = Find(u);
		v = Find(v);
		if (u == v)
		{
			return false;
		}
		if (Parent[u] > Parent[v])
		{
			std::swap(u, v);
		}
		Parent[u] += Parent[v];
		Parent[v] = u;
		return true;
	}
};

inline FTree BuildMinimumSpanningTree(const std::vector<FPoint>& Input)
{
	std::vector<FPoint> Points = Input;
	std::sort(Points.begin(), Points.end(), [](const FPoint& a, const FPoint& b)
	{
		if (a.x != b.x)
		{
			return a.x < b.x;
		}
		if (a.y != b.y)
		{
			return a.y < b.y;
		}
		return a.Id < b.Id;
	});
	FTree Tree;
	Tree.Edges.reserve(Input.size() - 1);
	std::vector<FPoint> Unique;
	Unique.reserve(Input.size());
	for (const FPoint& Point : Points)
	{
		if (!Unique.empty() && Unique.back().x == Point.x && Unique.back().y == Point.y)
		{
			Tree.Edges.emplace_back(Unique.back().Id, Point.Id);
		}
		else
		{
			Unique.push_back(Point);
		}
	}
	Points = Unique;
	struct FEdge
	{
		int Weight;
		int u;
		int v;
	};
	std::vector<FEdge> Candidates;
	Candidates.reserve(4 * Points.size());
	for (int Direction = 0; Direction < 4; ++Direction)
	{
		std::sort(Points.begin(), Points.end(), [](const FPoint& a, const FPoint& b)
		{
			return a.x != b.x ? a.x > b.x : a.y > b.y;
		});
		std::vector<int> Keys;
		Keys.reserve(Points.size());
		for (const FPoint& Point : Points)
		{
			Keys.push_back(Point.y - Point.x);
		}
		std::sort(Keys.begin(), Keys.end());
		Keys.erase(std::unique(Keys.begin(), Keys.end()), Keys.end());
		const int KeyCount = static_cast<int>(Keys.size());
		std::vector<int> Fenwick(KeyCount + 1, -1);
		auto Better = [&](int a, int b)
		{
			if (a == -1)
			{
				return b;
			}
			if (b == -1)
			{
				return a;
			}
			const int SumA = Points[a].x + Points[a].y;
			const int SumB = Points[b].x + Points[b].y;
			return SumA != SumB ? (SumA < SumB ? a : b)
				: (Points[a].Id < Points[b].Id ? a : b);
		};
		for (int i = 0; i < static_cast<int>(Points.size()); ++i)
		{
			const int Key = KeyCount - static_cast<int>(std::lower_bound(Keys.begin(),
				Keys.end(), Points[i].y - Points[i].x) - Keys.begin());
			int Best = -1;
			for (int Index = Key; Index > 0; Index -= Index & -Index)
			{
				Best = Better(Best, Fenwick[Index]);
			}
			if (Best != -1)
			{
				const int Weight = Points[Best].x + Points[Best].y - Points[i].x - Points[i].y;
				Candidates.push_back({Weight, Points[i].Id, Points[Best].Id});
			}
			for (int Index = Key; Index <= KeyCount; Index += Index & -Index)
			{
				Fenwick[Index] = Better(Fenwick[Index], i);
			}
		}
		for (FPoint& Point : Points)
		{
			if (Direction == 1)
			{
				Point.x = -Point.x;
			}
			else
			{
				std::swap(Point.x, Point.y);
			}
		}
	}
	std::sort(Candidates.begin(), Candidates.end(), [](const FEdge& a, const FEdge& b)
	{
		if (a.Weight != b.Weight)
		{
			return a.Weight < b.Weight;
		}
		return std::pair<int, int>(a.u, a.v) < std::pair<int, int>(b.u, b.v);
	});
	FDisjointSet Components(static_cast<int>(Input.size()));
	for (auto [u, v] : Tree.Edges)
	{
		Components.Unite(u, v);
	}
	for (const FEdge& Edge : Candidates)
	{
		if (Components.Unite(Edge.u, Edge.v))
		{
			Tree.Weight += Edge.Weight;
			Tree.Edges.emplace_back(Edge.u, Edge.v);
		}
	}
	if (Tree.Edges.size() + 1 != Input.size())
	{
		throw std::runtime_error("Disconnected Manhattan candidate graph");
	}
	return Tree;
}

#endif
