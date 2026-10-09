#ifndef NOMADISM_DAY_MST_HPP
#define NOMADISM_DAY_MST_HPP

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <numeric>
#include <stdexcept>
#include <utility>
#include <vector>

struct FPoint
{
	int x;
	int y;
	int Id;
};

inline std::int64_t SquaredDistance(const FPoint& a, const FPoint& b)
{
	const std::int64_t dx = a.x - b.x;
	const std::int64_t dy = a.y - b.y;
	return dx * dx + dy * dy;
}

inline std::int64_t Distance(const FPoint& a, const FPoint& b)
{
	const std::int64_t Square = SquaredDistance(a, b);
	std::int64_t Root = static_cast<std::int64_t>(std::sqrt(static_cast<double>(Square)));
	// Correct the estimate with integer comparisons, including perfect squares.
	while (Root * Root < Square)
	{
		++Root;
	}
	while (Root > 0 && (Root - 1) * (Root - 1) >= Square)
	{
		--Root;
	}
	return Root;
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

// Guibas-Stolfi divide-and-conquer with an indexed quad-edge structure.
// Each live undirected edge owns four consecutive records; deleted slots
// are recycled so that storage remains O(n), including during merging.
class FDelaunay
{
	struct FQuadEdge
	{
		int Origin;
		int Next;
	};

	const std::vector<FPoint>& Points;
	std::vector<FQuadEdge> Edges;
	std::vector<int> FreeEdges;

	static int Rotate(int e)
	{
		return (e & ~3) | ((e + 1) & 3);
	}

	static int InverseRotate(int e)
	{
		return (e & ~3) | ((e + 3) & 3);
	}

	static int Reverse(int e)
	{
		return e ^ 2;
	}

	int Destination(int e) const
	{
		return Edges[Reverse(e)].Origin;
	}

	int OriginPrevious(int e) const
	{
		return Rotate(Edges[Rotate(e)].Next);
	}

	int LeftNext(int e) const
	{
		return Rotate(Edges[InverseRotate(e)].Next);
	}

	int MakeEdge(int u, int v)
	{
		int Base;
		if (FreeEdges.empty())
		{
			Base = static_cast<int>(Edges.size());
			Edges.resize(Base + 4);
		}
		else
		{
			Base = FreeEdges.back();
			FreeEdges.pop_back();
		}
		Edges[Base] = {u, Base};
		Edges[Base + 1] = {-1, Base + 3};
		Edges[Base + 2] = {v, Base + 2};
		Edges[Base + 3] = {-1, Base + 1};
		return Base;
	}

	void Splice(int a, int b)
	{
		const int Alpha = Rotate(Edges[a].Next);
		const int Beta = Rotate(Edges[b].Next);
		std::swap(Edges[a].Next, Edges[b].Next);
		std::swap(Edges[Alpha].Next, Edges[Beta].Next);
	}

	int Connect(int a, int b)
	{
		const int e = MakeEdge(Destination(a), Edges[b].Origin);
		Splice(e, LeftNext(a));
		Splice(Reverse(e), b);
		return e;
	}

	void DeleteEdge(int e)
	{
		Splice(e, OriginPrevious(e));
		Splice(Reverse(e), OriginPrevious(Reverse(e)));
		const int Base = e & ~3;
		Edges[Base].Origin = -1;
		FreeEdges.push_back(Base);
	}

	std::int64_t Cross(int a, int b, int c) const
	{
		const std::int64_t ax = Points[b].x - Points[a].x;
		const std::int64_t ay = Points[b].y - Points[a].y;
		const std::int64_t bx = Points[c].x - Points[a].x;
		const std::int64_t by = Points[c].y - Points[a].y;
		return ax * by - ay * bx;
	}

	bool LeftOf(int p, int e) const
	{
		return Cross(Edges[e].Origin, Destination(e), p) > 0;
	}

	bool RightOf(int p, int e) const
	{
		return Cross(Edges[e].Origin, Destination(e), p) < 0;
	}

	bool InCircle(int a, int b, int c, int d) const
	{
		const std::int64_t ax = Points[a].x - Points[d].x;
		const std::int64_t ay = Points[a].y - Points[d].y;
		const std::int64_t bx = Points[b].x - Points[d].x;
		const std::int64_t by = Points[b].y - Points[d].y;
		const std::int64_t cx = Points[c].x - Points[d].x;
		const std::int64_t cy = Points[c].y - Points[d].y;
		// With |coordinate| <= 10000, the absolute sum is <= 1.92e18.
		// Strict comparison leaves cocircular edges in place deterministically.
		return (ax * ax + ay * ay) * (bx * cy - by * cx)
			- (bx * bx + by * by) * (ax * cy - ay * cx)
			+ (cx * cx + cy * cy) * (ax * by - ay * bx) > 0;
	}

	std::pair<int, int> Build(int Left, int Right)
	{
		if (Right - Left == 2)
		{
			const int a = MakeEdge(Left, Left + 1);
			return {a, Reverse(a)};
		}
		if (Right - Left == 3)
		{
			const int a = MakeEdge(Left, Left + 1);
			const int b = MakeEdge(Left + 1, Left + 2);
			Splice(Reverse(a), b);
			const std::int64_t Turn = Cross(Left, Left + 1, Left + 2);
			if (Turn == 0)
			{
				return {a, Reverse(b)};
			}
			const int c = Connect(b, a);
			if (Turn > 0)
			{
				return {a, Reverse(b)};
			}
			return {Reverse(c), c};
		}

		const int Middle = (Left + Right) / 2;
		auto [LeftOuter, LeftInner] = Build(Left, Middle);
		auto [RightInner, RightOuter] = Build(Middle, Right);
		while (true)
		{
			if (LeftOf(Edges[RightInner].Origin, LeftInner))
			{
				LeftInner = LeftNext(LeftInner);
			}
			else if (RightOf(Edges[LeftInner].Origin, RightInner))
			{
				RightInner = Edges[Reverse(RightInner)].Next;
			}
			else
			{
				break;
			}
		}
		int Base = Connect(Reverse(RightInner), LeftInner);
		if (Edges[LeftInner].Origin == Edges[LeftOuter].Origin)
		{
			LeftOuter = Reverse(Base);
		}
		if (Edges[RightInner].Origin == Edges[RightOuter].Origin)
		{
			RightOuter = Base;
		}

		while (true)
		{
			int LeftCandidate = Edges[Reverse(Base)].Next;
			if (RightOf(Destination(LeftCandidate), Base))
			{
				while (InCircle(Destination(Base), Edges[Base].Origin,
					Destination(LeftCandidate), Destination(Edges[LeftCandidate].Next)))
				{
					const int Next = Edges[LeftCandidate].Next;
					DeleteEdge(LeftCandidate);
					LeftCandidate = Next;
				}
			}
			int RightCandidate = OriginPrevious(Base);
			if (RightOf(Destination(RightCandidate), Base))
			{
				while (InCircle(Destination(Base), Edges[Base].Origin,
					Destination(RightCandidate), Destination(OriginPrevious(RightCandidate))))
				{
					const int Previous = OriginPrevious(RightCandidate);
					DeleteEdge(RightCandidate);
					RightCandidate = Previous;
				}
			}
			const bool bLeftValid = RightOf(Destination(LeftCandidate), Base);
			const bool bRightValid = RightOf(Destination(RightCandidate), Base);
			if (!bLeftValid && !bRightValid)
			{
				break;
			}
			if (!bLeftValid || (bRightValid && InCircle(Destination(LeftCandidate),
				Edges[LeftCandidate].Origin, Edges[RightCandidate].Origin, Destination(RightCandidate))))
			{
				Base = Connect(RightCandidate, Reverse(Base));
			}
			else
			{
				Base = Connect(Reverse(Base), Reverse(LeftCandidate));
			}
		}
		return {LeftOuter, RightOuter};
	}

public:
	explicit FDelaunay(const std::vector<FPoint>& InPoints) : Points(InPoints)
	{
		Edges.reserve(12 * Points.size());
	}

	std::vector<std::pair<int, int>> Run()
	{
		std::vector<std::pair<int, int>> Result;
		if (Points.size() < 2)
		{
			return Result;
		}
		Build(0, static_cast<int>(Points.size()));
		Result.reserve(3 * Points.size());
		for (int e = 0; e < static_cast<int>(Edges.size()); e += 4)
		{
			if (Edges[e].Origin >= 0)
			{
				Result.emplace_back(Edges[e].Origin, Destination(e));
			}
		}
		return Result;
	}
};

inline FTree BuildMinimumSpanningTree(const std::vector<FPoint>& Input)
{
	std::vector<FPoint> Sorted = Input;
	std::sort(Sorted.begin(), Sorted.end(), [](const FPoint& a, const FPoint& b)
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
	for (const FPoint& Point : Sorted)
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
	// Destroy the quad-edge pool before sorting and building the MST.
	auto Candidates = FDelaunay(Unique).Run();
	struct FEdge
	{
		std::int64_t Square;
		int u;
		int v;
	};
	std::vector<FEdge> Weighted;
	Weighted.reserve(Candidates.size());
	for (auto [u, v] : Candidates)
	{
		Weighted.push_back({SquaredDistance(Unique[u], Unique[v]), u, v});
	}
	std::sort(Weighted.begin(), Weighted.end(), [](const FEdge& a, const FEdge& b)
	{
		if (a.Square != b.Square)
		{
			return a.Square < b.Square;
		}
		return std::pair<int, int>(a.u, a.v) < std::pair<int, int>(b.u, b.v);
	});
	FDisjointSet Components(static_cast<int>(Unique.size()));
	for (const FEdge& Edge : Weighted)
	{
		if (Components.Unite(Edge.u, Edge.v))
		{
			Tree.Edges.emplace_back(Unique[Edge.u].Id, Unique[Edge.v].Id);
			Tree.Weight += Distance(Unique[Edge.u], Unique[Edge.v]);
		}
	}
	if (Tree.Edges.size() + 1 != Input.size())
	{
		throw std::runtime_error("Disconnected Delaunay graph");
	}
	return Tree;
}

#endif
