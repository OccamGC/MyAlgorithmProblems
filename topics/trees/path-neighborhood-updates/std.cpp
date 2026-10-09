// Problem setter's solution: caterpillar numbering of heavy chains and lazy range operations.
// GPT-6: explicit interval unions/differences, iterative preprocessing, 64-bit tags,
// empty-neighborhood specification, implementation and verification.
#include <algorithm>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>
using FInt = long long;
using FInterval = std::pair<int, int>;
struct FNode
{
	FInt Sum = 0;
	FInt Maximum = 0;
	FInt Added = 0;
	FInt Assigned = 0;
	bool bAssigned = false;
};
struct FAnswer
{
	FInt Sum = 0;
	FInt Maximum = std::numeric_limits<FInt>::lowest();
};
class FSegmentTree
{
	std::vector<FNode> Nodes;
	void Assign(int Node, int Length, FInt Value)
	{
		Nodes[Node].Sum = Length * Value;
		Nodes[Node].Maximum = Value;
		Nodes[Node].Assigned = Value;
		Nodes[Node].bAssigned = true;
		Nodes[Node].Added = 0;
	}
	void Add(int Node, int Length, FInt Value)
	{
		Nodes[Node].Sum += Length * Value;
		Nodes[Node].Maximum += Value;
		Nodes[Node].Added += Value;
	}
	void Push(int Node, int Left, int Right)
	{
		int Middle = (Left + Right) / 2;
		if (Nodes[Node].bAssigned)
		{
			Assign(2 * Node, Middle - Left + 1, Nodes[Node].Assigned);
			Assign(2 * Node + 1, Right - Middle, Nodes[Node].Assigned);
			Nodes[Node].bAssigned = false;
		}
		if (Nodes[Node].Added)
		{
			Add(2 * Node, Middle - Left + 1, Nodes[Node].Added);
			Add(2 * Node + 1, Right - Middle, Nodes[Node].Added);
			Nodes[Node].Added = 0;
		}
	}
public:
	explicit FSegmentTree(int n) : Nodes(4 * n)
	{
	}
	void Update(int Node, int Left, int Right, int l, int r, FInt Value, bool bAssign)
	{
		if (l <= Left && Right <= r)
		{
			if (bAssign)
			{
				Assign(Node, Right - Left + 1, Value);
			}
			else
			{
				Add(Node, Right - Left + 1, Value);
			}
			return;
		}
		Push(Node, Left, Right);
		int Middle = (Left + Right) / 2;
		if (l <= Middle)
		{
			Update(Node * 2, Left, Middle, l, r, Value, bAssign);
		}
		if (r > Middle)
		{
			Update(Node * 2 + 1, Middle + 1, Right, l, r, Value, bAssign);
		}
		Nodes[Node].Sum = Nodes[Node * 2].Sum + Nodes[Node * 2 + 1].Sum;
		Nodes[Node].Maximum = std::max(Nodes[Node * 2].Maximum, Nodes[Node * 2 + 1].Maximum);
	}
	void Query(int Node, int Left, int Right, int l, int r, FAnswer& Answer)
	{
		if (l <= Left && Right <= r)
		{
			Answer.Sum += Nodes[Node].Sum;
			Answer.Maximum = std::max(Answer.Maximum, Nodes[Node].Maximum);
			return;
		}
		Push(Node, Left, Right);
		int Middle = (Left + Right) / 2;
		if (l <= Middle)
		{
			Query(Node * 2, Left, Middle, l, r, Answer);
		}
		if (r > Middle)
		{
			Query(Node * 2 + 1, Middle + 1, Right, l, r, Answer);
		}
	}
};
class FLayout
{
	std::vector<std::vector<int>> Adjacent;
	std::vector<int> Parent;
	std::vector<int> Depth;
	std::vector<int> Heavy;
	std::vector<int> Head;
	std::vector<int> Id;
	std::vector<int> Tail;
	std::vector<FInterval> Hair;
	std::vector<FInterval> Descendants;
	int Counter = 0;
	void NumberChain(int Top)
	{
		std::vector<int> Chain;
		for (int u = Top; u; u = Heavy[u])
		{
			Chain.push_back(u);
			Head[u] = Top;
			if (u != Top)
			{
				Id[u] = ++Counter;
			}
		}
		Tail[Top] = Chain.back();
		for (int u : Chain)
		{
			Hair[u].first = Counter + 1;
			for (int v : Adjacent[u])
			{
				if (v != Parent[u] && v != Heavy[u])
				{
					Id[v] = ++Counter;
				}
			}
			Hair[u].second = Counter;
		}
		for (int u : Chain)
		{
			Descendants[u].first = Counter + 1;
			for (int v : Adjacent[u])
			{
				if (v != Parent[u] && v != Heavy[u])
				{
					NumberChain(v);
				}
			}
			Descendants[u].second = Counter;
		}
	}
	static std::vector<FInterval> Merge(std::vector<FInterval> Ranges)
	{
		std::sort(Ranges.begin(), Ranges.end());
		std::vector<FInterval> Result;
		for (FInterval Range : Ranges)
		{
			if (Range.first < 1 || Range.first > Range.second)
			{
				continue;
			}
			if (!Result.empty() && Range.first <= Result.back().second + 1)
			{
				Result.back().second = std::max(Result.back().second, Range.second);
			}
			else
			{
				Result.push_back(Range);
			}
		}
		return Result;
	}
	std::vector<FInterval> Segments(int a, int b, int& Lca) const
	{
		std::vector<FInterval> Result;
		while (Head[a] != Head[b])
		{
			if (Depth[Head[a]] < Depth[Head[b]])
			{
				std::swap(a, b);
			}
			Result.push_back({Head[a], a});
			a = Parent[Head[a]];
		}
		if (Depth[a] > Depth[b])
		{
			std::swap(a, b);
		}
		Lca = a;
		Result.push_back({a, b});
		return Result;
	}
	void AppendChain(int Top, int Bottom, std::vector<FInterval>& Ranges) const
	{
		if (Top == Head[Top])
		{
			Ranges.push_back({Id[Top], Id[Top]});
			if (Top == Bottom)
			{
				return;
			}
			Top = Heavy[Top];
		}
		Ranges.push_back({Id[Top], Id[Bottom]});
	}
public:
	explicit FLayout(int n) : Adjacent(n + 1), Parent(n + 1), Depth(n + 1), Heavy(n + 1),
		Head(n + 1), Id(n + 1), Tail(n + 1), Hair(n + 1), Descendants(n + 1)
	{
		for (int i = 1; i < n; ++i)
		{
			int u;
			int v;
			std::cin >> u >> v;
			Adjacent[u].push_back(v);
			Adjacent[v].push_back(u);
		}
		std::vector<int> Order{1};
		for (int i = 0; i < n; ++i)
		{
			int u = Order[i];
			for (int v : Adjacent[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Depth[v] = Depth[u] + 1;
					Order.push_back(v);
				}
			}
		}
		std::vector<int> Size(n + 1, 1);
		Size[0] = 0;
		for (int i = n - 1; i >= 0; --i)
		{
			int u = Order[i];
			if (Parent[u])
			{
				Size[Parent[u]] += Size[u];
				if (Size[u] > Size[Heavy[Parent[u]]])
				{
					Heavy[Parent[u]] = u;
				}
			}
		}
		Id[1] = ++Counter;
		NumberChain(1);
	}
	std::vector<FInterval> Ranges(int Region, int a, int b) const
	{
		std::vector<FInterval> Result;
		if (Region == 2)
		{
			int Bottom = Tail[Head[a]];
			AppendChain(a, Bottom, Result);
			Result.push_back({Hair[a].first, Hair[Bottom].second});
			Result.push_back({Descendants[a].first, Descendants[Bottom].second});
			return Merge(Result);
		}
		int Lca = 0;
		std::vector<FInterval> Parts = Segments(a, b, Lca);
		std::vector<FInterval> Path;
		for (FInterval Part : Parts)
		{
			AppendChain(Part.first, Part.second, Path);
		}
		Path = Merge(Path);
		if (Region == 0)
		{
			return Path;
		}
		for (FInterval Part : Parts)
		{
			Result.push_back({Hair[Part.first].first, Hair[Part.second].second});
			int Child = Heavy[Part.second];
			if (Child)
			{
				Result.push_back({Id[Child], Id[Child]});
			}
		}
		if (Parent[Lca])
		{
			Result.push_back({Id[Parent[Lca]], Id[Parent[Lca]]});
		}
		Result = Merge(Result);
		std::vector<FInterval> Difference;
		int First = 0;
		for (FInterval Range : Result)
		{
			int Position = Range.first;
			while (First < static_cast<int>(Path.size()) && Path[First].second < Position)
			{
				++First;
			}
			for (int i = First; i < static_cast<int>(Path.size()) && Path[i].first <= Range.second; ++i)
			{
				if (Position < Path[i].first)
				{
					Difference.push_back({Position, Path[i].first - 1});
				}
				Position = std::max(Position, Path[i].second + 1);
			}
			if (Position <= Range.second)
			{
				Difference.push_back({Position, Range.second});
			}
		}
		return Difference;
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	FLayout Layout(n);
	FSegmentTree Tree(n);
	while (m--)
	{
		int Type;
		int a;
		int b = 0;
		FInt Value = 0;
		std::cin >> Type >> a;
		int Region = (Type - 1) % 3;
		int Action = (Type - 1) / 3;
		if (Region != 2)
		{
			std::cin >> b;
		}
		if (Action < 2)
		{
			std::cin >> Value;
		}
		std::vector<FInterval> Ranges = Layout.Ranges(Region, a, b);
		FAnswer Answer;
		for (FInterval Range : Ranges)
		{
			if (Action < 2)
			{
				Tree.Update(1, 1, n, Range.first, Range.second, Value, Action == 1);
			}
			else
			{
				Tree.Query(1, 1, n, Range.first, Range.second, Answer);
			}
		}
		if (Action == 2)
		{
			if (Ranges.empty())
			{
				std::cout << "EMPTY\n";
			}
			else
			{
				std::cout << Answer.Maximum << '\n';
			}
		}
		else if (Action == 3)
		{
			std::cout << Answer.Sum << '\n';
		}
	}
}
