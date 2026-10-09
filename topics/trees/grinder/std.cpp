// Original degree-three expansion and balanced edge decomposition.
// Contribution: Codex (GPT-6): explicit traversals, 64-bit sums, and zero-length boundaries.
#include <algorithm>
#include <deque>
#include <iostream>
#include <limits>
#include <vector>

using FInt = long long;
constexpr FInt Missing = std::numeric_limits<FInt>::lowest() / 4;
constexpr int NoPath = -1061109568;

struct FEdge
{
	int To;
	int Next;
	int Weight;
	int OriginalChild;
};

struct FVisit
{
	int Vertex;
	int ParentIndex;
	int ParentEdge;
	int Depth;
	FInt Sum;
	FInt Best = Missing;
};

class FSolver
{
public:
	int n;
	int L;
	int R;
	std::vector<int> Value;
	std::vector<int> Head;
	std::vector<FEdge> Edges;
	std::vector<char> Removed;
	std::vector<FInt> EdgeAnswer;

	void Link(int u, int v, int Weight, int OriginalChild)
	{
		Edges.push_back({v, Head[u], Weight, OriginalChild});
		Head[u] = static_cast<int>(Edges.size()) - 1;
		Edges.push_back({u, Head[v], Weight, OriginalChild});
		Head[v] = static_cast<int>(Edges.size()) - 1;
	}

	std::vector<FVisit> Collect(int Start)
	{
		std::vector<FVisit> Visits{{Start, -1, -1, 0, 0}};
		for (std::size_t i = 0; i < Visits.size(); ++i)
		{
			const FVisit Visit = Visits[i];
			for (int e = Head[Visit.Vertex]; e != -1; e = Edges[e].Next)
			{
				const FEdge& Edge = Edges[e];
				if (Removed[e / 2] || (Visit.ParentEdge >= 0 && e == (Visit.ParentEdge ^ 1)))
				{
					continue;
				}
				const int Depth = Visit.Depth + (Edge.OriginalChild >= 0);
				if (Depth <= R)
				{
					Visits.push_back({Edge.To, static_cast<int>(i), e, Depth, Visit.Sum + Edge.Weight});
				}
			}
		}
		return Visits;
	}

	void PairSides(std::vector<FVisit>& From, const std::vector<FVisit>& To, const FEdge& Cut)
	{
		int MaxTo = 0;
		int MaxFrom = 0;
		for (const FVisit& Visit : To)
		{
			MaxTo = std::max(MaxTo, Visit.Depth);
		}
		for (const FVisit& Visit : From)
		{
			MaxFrom = std::max(MaxFrom, Visit.Depth);
		}
		std::vector<FInt> Maximum(MaxTo + 1, Missing);
		for (const FVisit& Visit : To)
		{
			if (Visit.Vertex < n)
			{
				Maximum[Visit.Depth] = std::max(Maximum[Visit.Depth], Visit.Sum + Value[Visit.Vertex]);
			}
		}
		// Counting by depth preserves linear work even with zero-length dummy edges.
		std::vector<int> First(MaxFrom + 1, -1);
		std::vector<int> NextVisit(From.size(), -1);
		for (int i = 0; i < static_cast<int>(From.size()); ++i)
		{
			NextVisit[i] = First[From[i].Depth];
			First[From[i].Depth] = i;
		}
		std::vector<int> Queue(MaxTo + 1);
		int Begin = 0;
		int End = 0;
		int Next = MaxTo;
		const int CutLength = Cut.OriginalChild >= 0;
		for (int Depth = 0; Depth <= MaxFrom; ++Depth)
		{
			const int Low = std::max(0, L - CutLength - Depth);
			const int High = R - CutLength - Depth;
			while (Next >= Low)
			{
				while (Begin < End && Maximum[Queue[End - 1]] <= Maximum[Next])
				{
					--End;
				}
				Queue[End++] = Next--;
			}
			while (Begin < End && Queue[Begin] > High)
			{
				++Begin;
			}
			if (Begin == End || Maximum[Queue[Begin]] == Missing)
			{
				continue;
			}
			for (int i = First[Depth]; i != -1; i = NextVisit[i])
			{
				FVisit& Visit = From[i];
				if (Visit.Vertex < n)
				{
					Visit.Best = Visit.Sum + Value[Visit.Vertex] + Cut.Weight + Maximum[Queue[Begin]];
				}
			}
		}
	}

	void Propagate(std::vector<FVisit>& Visits, int CutChild)
	{
		for (int i = static_cast<int>(Visits.size()) - 1; i >= 0; --i)
		{
			const FVisit& Visit = Visits[i];
			if (Visit.ParentIndex >= 0)
			{
				const int Child = Edges[Visit.ParentEdge].OriginalChild;
				if (Child >= 0)
				{
					EdgeAnswer[Child] = std::max(EdgeAnswer[Child], Visit.Best);
				}
				FVisit& Up = Visits[Visit.ParentIndex];
				Up.Best = std::max(Up.Best, Visit.Best);
			}
			else if (CutChild >= 0)
			{
				EdgeAnswer[CutChild] = std::max(EdgeAnswer[CutChild], Visit.Best);
			}
		}
	}

	void Solve(const std::vector<int>& OriginalParent)
	{
		const int Count = static_cast<int>(Head.size());
		Removed.assign(Edges.size() / 2, false);
		EdgeAnswer.assign(n, Missing);
		std::vector<int> ParentEdge(Count, -1);
		std::vector<int> Size(Count);
		std::vector<int> Order;
		std::vector<int> Tasks{0};
		while (!Tasks.empty())
		{
			const int Start = Tasks.back();
			Tasks.pop_back();
			Order.assign(1, Start);
			ParentEdge[Start] = -1;
			for (std::size_t i = 0; i < Order.size(); ++i)
			{
				const int u = Order[i];
				Size[u] = 1;
				for (int e = Head[u]; e != -1; e = Edges[e].Next)
				{
					if (!Removed[e / 2] && (ParentEdge[u] < 0 || e != (ParentEdge[u] ^ 1)))
					{
						ParentEdge[Edges[e].To] = e;
						Order.push_back(Edges[e].To);
					}
				}
			}
			const int Total = static_cast<int>(Order.size());
			if (Total <= 8)
			{
				for (int Endpoint : Order)
				{
					if (Endpoint >= n)
					{
						continue;
					}
					FVisit Visits[8]{};
					Visits[0] = {Endpoint, -1, -1, 0, 0};
					int CountVisits = 1;
					for (int i = 0; i < CountVisits; ++i)
					{
						const FVisit Visit = Visits[i];
						if (Visit.Vertex < n && L <= Visit.Depth && Visit.Depth <= R)
						{
							const FInt Result = Visit.Sum + Value[Endpoint] + Value[Visit.Vertex];
							for (int j = i; Visits[j].ParentIndex >= 0; j = Visits[j].ParentIndex)
							{
								const int Child = Edges[Visits[j].ParentEdge].OriginalChild;
								if (Child >= 0)
								{
									EdgeAnswer[Child] = std::max(EdgeAnswer[Child], Result);
								}
							}
						}
						for (int e = Head[Visit.Vertex]; e != -1; e = Edges[e].Next)
						{
							if (!Removed[e / 2] && (Visit.ParentEdge < 0 || e != (Visit.ParentEdge ^ 1)))
							{
								const FEdge& Edge = Edges[e];
								Visits[CountVisits++] = {Edge.To, i, e, Visit.Depth + (Edge.OriginalChild >= 0), Visit.Sum + Edge.Weight};
							}
						}
					}
				}
				continue;
			}
			int Cut = -1;
			int Balance = Total;
			for (int i = Total - 1; i >= 1; --i)
			{
				const int u = Order[i];
				const int e = ParentEdge[u];
				const int Largest = std::max(Size[u], Total - Size[u]);
				if (Largest < Balance)
				{
					Balance = Largest;
					Cut = e;
				}
				Size[Edges[e ^ 1].To] += Size[u];
			}
			Removed[Cut / 2] = true;
			const int a = Edges[Cut ^ 1].To;
			const int b = Edges[Cut].To;
			std::vector<FVisit> Left = Collect(a);
			std::vector<FVisit> Right = Collect(b);
			PairSides(Left, Right, Edges[Cut]);
			PairSides(Right, Left, Edges[Cut]);
			Propagate(Left, Edges[Cut].OriginalChild);
			Propagate(Right, Edges[Cut].OriginalChild);
			Tasks.push_back(a);
			Tasks.push_back(b);
		}
		std::vector<FInt> Answer(n, Missing);
		if (L == 0)
		{
			for (int u = 0; u < n; ++u)
			{
				Answer[u] = Value[u];
			}
		}
		for (int v = 1; v < n; ++v)
		{
			if (EdgeAnswer[v] != Missing)
			{
				Answer[v] = std::max(Answer[v], EdgeAnswer[v] / 2);
				Answer[OriginalParent[v]] = std::max(Answer[OriginalParent[v]], EdgeAnswer[v] / 2);
			}
		}
		for (FInt Result : Answer)
		{
			std::cout << (Result == Missing ? NoPath : Result) << '\n';
		}
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	FSolver Solver;
	std::cin >> Solver.n >> Solver.L >> Solver.R;
	const int n = Solver.n;
	Solver.Value.resize(n);
	for (int& v : Solver.Value)
	{
		std::cin >> v;
	}
	std::vector<int> Parent(n, -1);
	Solver.Head.assign(2 * n - 1, -1);
	Solver.Edges.reserve(4 * (n - 1));
	{
		std::vector<std::vector<int>> Graph(n);
		for (int i = 1; i < n; ++i)
		{
			int u;
			int v;
			std::cin >> u >> v;
			Graph[--u].push_back(--v);
			Graph[v].push_back(u);
		}
		std::vector<int> Order{0};
		for (int i = 0; i < n; ++i)
		{
			const int u = Order[i];
			int Last = u;
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Order.push_back(v);
					const int Dummy = n + v - 1;
					Solver.Link(Last, Dummy, 0, -1);
					Solver.Link(Dummy, v, Solver.Value[u] + Solver.Value[v], v);
					Last = Dummy;
				}
			}
		}
	}
	Solver.Solve(Parent);
}
