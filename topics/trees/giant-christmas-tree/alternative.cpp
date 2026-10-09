// Problem setter's solution idea: centroid decomposition for diameter maintenance under deletions.
// Codex (GPT-6): local Euler-interval deletion, iterative construction and online path-query support.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>

struct FEdge
{
	int Destination;
	int State;
};

class FTree
{
public:
	std::vector<std::vector<FEdge>> Edges;
	std::vector<int> Parent;
	std::vector<int> Depth;
	std::vector<int> Lit;
	std::vector<int> Order;
	std::vector<std::vector<int>> Up;
	explicit FTree(int n) : Edges(n + 1), Parent(n + 1), Depth(n + 1), Lit(n + 1)
	{
		int Levels = 1;
		while ((1 << Levels) <= n)
		{
			++Levels;
		}
		Up.assign(Levels, std::vector<int>(n + 1));
	}
	void Build()
	{
		Order.push_back(1);
		for (int Index = 0; Index < static_cast<int>(Order.size()); ++Index)
		{
			int u = Order[Index];
			for (FEdge Edge : Edges[u])
			{
				int v = Edge.Destination;
				if (v == Parent[u])
				{
					continue;
				}
				Parent[v] = u;
				Depth[v] = Depth[u] + 1;
				Lit[v] = Edge.State;
				Up[0][v] = u;
				for (int Level = 1; Level < static_cast<int>(Up.size()); ++Level)
				{
					Up[Level][v] = Up[Level - 1][Up[Level - 1][v]];
				}
				Order.push_back(v);
			}
		}
	}
	int Ancestor(int u, int v) const
	{
		if (Depth[u] < Depth[v])
		{
			std::swap(u, v);
		}
		int Difference = Depth[u] - Depth[v];
		for (int Level = 0; Level < static_cast<int>(Up.size()); ++Level)
		{
			if (Difference & (1 << Level))
			{
				u = Up[Level][u];
			}
		}
		if (u == v)
		{
			return u;
		}
		for (int Level = static_cast<int>(Up.size()) - 1; Level >= 0; --Level)
		{
			if (Up[Level][u] != Up[Level][v])
			{
				u = Up[Level][u];
				v = Up[Level][v];
			}
		}
		return Parent[u];
	}
	int Distance(int u, int v) const
	{
		return Depth[u] + Depth[v] - 2 * Depth[Ancestor(u, v)];
	}
};

class FDisjointSet
{
public:
	std::vector<int> Parent;
	explicit FDisjointSet(int n) : Parent(n + 1)
	{
		std::iota(Parent.begin(), Parent.end(), 0);
	}
	int Find(int u)
	{
		int Root = u;
		while (Parent[Root] != Root)
		{
			Root = Parent[Root];
		}
		while (u != Root)
		{
			int Next = Parent[u];
			Parent[u] = Root;
			u = Next;
		}
		return Root;
	}
};


struct FRecord
{
	int Center;
	int Distance;
	int Branch;
	int Begin;
	int End;
};

struct FCenter
{
	std::vector<int> Order;
	std::set<int> Active;
	std::vector<std::set<std::pair<int, int>>> Branches;
	std::set<std::pair<int, int>> Maxima;
	int Diameter() const
	{
		auto Iterator = Maxima.rbegin();
		int Result = Iterator->first;
		++Iterator;
		if (Iterator != Maxima.rend())
		{
			Result += Iterator->first;
		}
		return Result;
	}
};

struct FVisit
{
	int Vertex;
	int Parent;
	int Distance;
	int Branch;
	bool bExit;
};

class FOnlineDiameters
{
private:
	const FTree& Tree;
	std::vector<FCenter> Centers;
	std::vector<std::vector<FRecord>> Records;
	std::vector<bool> Blocked;
	std::vector<int> TemporaryParent;
	std::vector<int> Size;
	std::set<std::pair<int, int>> Best;
	int FindCenter(int Start)
	{
		std::vector<int> Order{Start};
		TemporaryParent[Start] = 0;
		for (int Index = 0; Index < static_cast<int>(Order.size()); ++Index)
		{
			int u = Order[Index];
			for (FEdge Edge : Tree.Edges[u])
			{
				int v = Edge.Destination;
				if (!Blocked[v] && v != TemporaryParent[u])
				{
					TemporaryParent[v] = u;
					Order.push_back(v);
				}
			}
		}
		int Chosen = Start;
		int BestSize = static_cast<int>(Order.size());
		for (int Index = static_cast<int>(Order.size()) - 1; Index >= 0; --Index)
		{
			int u = Order[Index];
			Size[u] = 1;
			int Largest = 0;
			for (FEdge Edge : Tree.Edges[u])
			{
				int v = Edge.Destination;
				if (!Blocked[v] && v != TemporaryParent[u])
				{
					Size[u] += Size[v];
					Largest = std::max(Largest, Size[v]);
				}
			}
			Largest = std::max(Largest, static_cast<int>(Order.size()) - Size[u]);
			if (Largest < BestSize)
			{
				BestSize = Largest;
				Chosen = u;
			}
		}
		return Chosen;
	}
	void BuildCenter(int Center)
	{
		FCenter& Data = Centers[Center];
		Data.Branches.emplace_back();
		std::vector<FVisit> Stack{{Center, 0, 0, 0, false}};
		while (!Stack.empty())
		{
			FVisit Visit = Stack.back();
			Stack.pop_back();
			int u = Visit.Vertex;
			if (Visit.bExit)
			{
				Records[u].back().End = static_cast<int>(Data.Order.size());
				continue;
			}
			int Position = static_cast<int>(Data.Order.size());
			Data.Order.push_back(u);
			Data.Active.insert(Position);
			Data.Branches[Visit.Branch].insert({Visit.Distance, u});
			Records[u].push_back(FRecord{Center, Visit.Distance, Visit.Branch, Position, -1});
			Stack.push_back(FVisit{u, Visit.Parent, Visit.Distance, Visit.Branch, true});
			for (FEdge Edge : Tree.Edges[u])
			{
				int v = Edge.Destination;
				if (Blocked[v] || v == Visit.Parent)
				{
					continue;
				}
				int Branch = Visit.Branch;
				if (u == Center)
				{
					Branch = static_cast<int>(Data.Branches.size());
					Data.Branches.emplace_back();
				}
				Stack.push_back(FVisit{v, u, Visit.Distance + 1, Branch, false});
			}
		}
		for (int Branch = 0; Branch < static_cast<int>(Data.Branches.size()); ++Branch)
		{
			Data.Maxima.insert({Data.Branches[Branch].rbegin()->first, Branch});
		}
		Best.insert({Data.Diameter(), Center});
	}
public:
	FOnlineDiameters(int n, const FTree& InTree) : Tree(InTree), Centers(n + 1), Records(n + 1), Blocked(n + 1), TemporaryParent(n + 1), Size(n + 1)
	{
		std::vector<int> Tasks{1};
		while (!Tasks.empty())
		{
			int Start = Tasks.back();
			Tasks.pop_back();
			int Center = FindCenter(Start);
			BuildCenter(Center);
			Blocked[Center] = true;
			for (FEdge Edge : Tree.Edges[Center])
			{
				if (!Blocked[Edge.Destination])
				{
					Tasks.push_back(Edge.Destination);
				}
			}
		}
	}
	void Cut(int u, int v)
	{
		int Levels = static_cast<int>(std::min(Records[u].size(), Records[v].size()));
		for (int Level = 0; Level < Levels; ++Level)
		{
			const FRecord& First = Records[u][Level];
			const FRecord& Second = Records[v][Level];
			if (First.Center != Second.Center)
			{
				break;
			}
			const FRecord& Child = First.Distance > Second.Distance ? First : Second;
			FCenter& Data = Centers[Child.Center];
			auto Iterator = Data.Active.lower_bound(Child.Begin);
			if (Iterator == Data.Active.end() || *Iterator >= Child.End)
			{
				continue;
			}
			Best.erase({Data.Diameter(), Child.Center});
			while (Iterator != Data.Active.end() && *Iterator < Child.End)
			{
				int Vertex = Data.Order[*Iterator];
				const FRecord& Record = Records[Vertex][Level];
				auto& Branch = Data.Branches[Record.Branch];
				Data.Maxima.erase({Branch.rbegin()->first, Record.Branch});
				Branch.erase({Record.Distance, Vertex});
				if (!Branch.empty())
				{
					Data.Maxima.insert({Branch.rbegin()->first, Record.Branch});
				}
				Iterator = Data.Active.erase(Iterator);
			}
			Best.insert({Data.Diameter(), Child.Center});
		}
	}
	int Maximum() const
	{
		return Best.rbegin()->first;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	FTree Tree(N);
	for (int i = 1; i < N; ++i)
	{
		int u;
		int v;
		int s;
		std::cin >> u >> v >> s;
		Tree.Edges[u].push_back(FEdge{v, s});
		Tree.Edges[v].push_back(FEdge{u, s});
	}
	Tree.Build();
	FOnlineDiameters Diameters(N, Tree);
	FDisjointSet Skip(N);
	for (int u : Tree.Order)
	{
		if (u != 1 && !Tree.Lit[u])
		{
			Diameters.Cut(u, Tree.Parent[u]);
			Skip.Parent[u] = Skip.Find(Tree.Parent[u]);
		}
	}
	while (M--)
	{
		int u;
		int v;
		std::cin >> u >> v;
		int Common = Tree.Ancestor(u, v);
		for (int Start : {u, v})
		{
			int Current = Skip.Find(Start);
			while (Tree.Depth[Current] > Tree.Depth[Common])
			{
				Diameters.Cut(Current, Tree.Parent[Current]);
				Skip.Parent[Current] = Skip.Find(Tree.Parent[Current]);
				Current = Skip.Find(Current);
			}
		}
		std::cout << Diameters.Maximum() << '\n';
	}
}
