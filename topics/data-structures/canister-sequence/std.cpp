// Deterministic implicit splay tree; range moves use positions after removal.
// Codex (GPT-6): rewritten propagation, interval isolation and boundary handling.
#include <algorithm>
#include <iostream>
#include <vector>

struct FNode
{
	int Child[2] = {0, 0};
	int Parent = 0;
	int Size = 0;
	int Value = 0;
	int First = 0;
	int Last = 0;
	int Runs = 0;
	int Assignment = 0;
	bool bReverse = false;
};

class FSequence
{
	std::vector<FNode> Nodes;
	std::vector<int> Stack;
	int Root = 0;

	void Pull(int x)
	{
		const FNode& Left = Nodes[Nodes[x].Child[0]];
		const FNode& Right = Nodes[Nodes[x].Child[1]];
		Nodes[x].Size = Left.Size + 1 + Right.Size;
		Nodes[x].First = Left.Size ? Left.First : Nodes[x].Value;
		Nodes[x].Last = Right.Size ? Right.Last : Nodes[x].Value;
		Nodes[x].Runs = Left.Runs + 1 + Right.Runs;
		Nodes[x].Runs -= Left.Size && Left.Last == Nodes[x].Value;
		Nodes[x].Runs -= Right.Size && Right.First == Nodes[x].Value;
	}

	void Assign(int x, int Value)
	{
		if (x != 0)
		{
			Nodes[x].Value = Value;
			Nodes[x].First = Value;
			Nodes[x].Last = Value;
			Nodes[x].Assignment = Value;
			Nodes[x].Runs = 1;
		}
	}

	void Reverse(int x)
	{
		if (x != 0)
		{
			std::swap(Nodes[x].Child[0], Nodes[x].Child[1]);
			std::swap(Nodes[x].First, Nodes[x].Last);
			Nodes[x].bReverse = !Nodes[x].bReverse;
		}
	}

	void Push(int x)
	{
		if (Nodes[x].Assignment != 0)
		{
			Assign(Nodes[x].Child[0], Nodes[x].Assignment);
			Assign(Nodes[x].Child[1], Nodes[x].Assignment);
			Nodes[x].Assignment = 0;
		}
		if (Nodes[x].bReverse)
		{
			Reverse(Nodes[x].Child[0]);
			Reverse(Nodes[x].Child[1]);
			Nodes[x].bReverse = false;
		}
	}

	int Build(const std::vector<int>& Values, int l, int r, int Parent)
	{
		if (l > r)
		{
			return 0;
		}
		int Middle = (l + r) / 2;
		int x = Middle + 1;
		Nodes[x].Value = Values[Middle];
		Nodes[x].Parent = Parent;
		Nodes[x].Child[0] = Build(Values, l, Middle - 1, x);
		Nodes[x].Child[1] = Build(Values, Middle + 1, r, x);
		Pull(x);
		return x;
	}

	void Rotate(int x)
	{
		int p = Nodes[x].Parent;
		int g = Nodes[p].Parent;
		int Side = Nodes[p].Child[1] == x;
		int Middle = Nodes[x].Child[Side ^ 1];
		if (g != 0)
		{
			Nodes[g].Child[Nodes[g].Child[1] == p] = x;
		}
		Nodes[x].Parent = g;
		Nodes[p].Child[Side] = Middle;
		if (Middle != 0)
		{
			Nodes[Middle].Parent = p;
		}
		Nodes[x].Child[Side ^ 1] = p;
		Nodes[p].Parent = x;
		Pull(p);
		Pull(x);
	}

	void Splay(int x, int Goal = 0)
	{
		Stack.clear();
		for (int v = x; v != Goal; v = Nodes[v].Parent)
		{
			Stack.push_back(v);
		}
		for (auto It = Stack.rbegin(); It != Stack.rend(); ++It)
		{
			Push(*It);
		}
		while (Nodes[x].Parent != Goal)
		{
			int p = Nodes[x].Parent;
			int g = Nodes[p].Parent;
			if (g != Goal)
			{
				bool bAligned = (Nodes[p].Child[1] == x) == (Nodes[g].Child[1] == p);
				Rotate(bAligned ? p : x);
			}
			Rotate(x);
		}
		if (Goal == 0)
		{
			Root = x;
		}
	}

	int Find(int Rank)
	{
		int x = Root;
		while (true)
		{
			Push(x);
			int LeftSize = Nodes[Nodes[x].Child[0]].Size;
			if (Rank == LeftSize)
			{
				return x;
			}
			if (Rank < LeftSize)
			{
				x = Nodes[x].Child[0];
			}
			else
			{
				Rank -= LeftSize + 1;
				x = Nodes[x].Child[1];
			}
		}
	}

	int Isolate(int l, int r)
	{
		int Left = Find(l - 1);
		Splay(Left);
		int Right = Find(r + 1);
		Splay(Right, Left);
		return Right;
	}

	void Refresh(int Right)
	{
		Pull(Right);
		Pull(Root);
	}

public:
	explicit FSequence(const std::vector<int>& Values) : Nodes(Values.size() + 1)
	{
		Root = Build(Values, 0, static_cast<int>(Values.size()) - 1, 0);
		Stack.reserve(Values.size());
	}

	void Change(int l, int r, int Value, bool bReverse)
	{
		int Right = Isolate(l, r);
		int Middle = Nodes[Right].Child[0];
		if (bReverse)
		{
			Reverse(Middle);
		}
		else
		{
			Assign(Middle, Value);
		}
		Refresh(Right);
	}

	int Query(int l, int r)
	{
		int Right = Isolate(l, r);
		return Nodes[Nodes[Right].Child[0]].Runs;
	}

	void Move(int l, int Length, int Destination)
	{
		int Right = Isolate(l, l + Length - 1);
		int Middle = Nodes[Right].Child[0];
		Nodes[Right].Child[0] = 0;
		Nodes[Middle].Parent = 0;
		Refresh(Right);
		Right = Isolate(Destination, Destination - 1);
		Nodes[Right].Child[0] = Middle;
		Nodes[Middle].Parent = Right;
		Refresh(Right);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Values(n + 2, -1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Values[i];
	}
	FSequence Sequence(Values);
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		int l;
		int r;
		std::cin >> Operation >> l >> r;
		if (Operation == 1)
		{
			int v;
			std::cin >> v;
			Sequence.Change(l, r, v, false);
		}
		else if (Operation == 2)
		{
			Sequence.Change(l, r, 0, true);
		}
		else if (Operation == 3)
		{
			int Destination;
			std::cin >> Destination;
			Sequence.Move(l, r, Destination);
		}
		else
		{
			std::cout << Sequence.Query(l, r) << '\n';
		}
	}
}
