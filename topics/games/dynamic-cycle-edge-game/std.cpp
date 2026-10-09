// Problem setter's data structure: an implicit splay tree with range minima.
// Codex (GPT-6): corrected game characterization using the actual minimum,
// endpoint parity, first/last minimum aggregation and empty-cycle conventions.
#include <algorithm>
#include <vector>
#include "buffered-input.hpp"

struct FNode
{
	int Child[2] = {0, 0};
	int Parent = 0;
	int Size = 0;
	int Value = 101;
	int Minimum = 101;
	int First = 0;
	int Last = 0;
};
class FSplay
{
public:
	std::vector<FNode> Nodes;
	int Root = 0;
	int Used = 0;
	explicit FSplay(int Capacity) : Nodes(Capacity)
	{
	}
	void Pull(int u)
	{
		FNode& Node = Nodes[u];
		int Left = Node.Child[0];
		int Right = Node.Child[1];
		Node.Size = Nodes[Left].Size + 1 + Nodes[Right].Size;
		Node.Minimum = std::min(Node.Value, std::min(Nodes[Left].Minimum, Nodes[Right].Minimum));
		if (Left != 0 && Nodes[Left].Minimum == Node.Minimum)
		{
			Node.First = Nodes[Left].First;
		}
		else if (Node.Value == Node.Minimum)
		{
			Node.First = Nodes[Left].Size;
		}
		else
		{
			Node.First = Nodes[Left].Size + 1 + Nodes[Right].First;
		}
		if (Right != 0 && Nodes[Right].Minimum == Node.Minimum)
		{
			Node.Last = Nodes[Left].Size + 1 + Nodes[Right].Last;
		}
		else if (Node.Value == Node.Minimum)
		{
			Node.Last = Nodes[Left].Size;
		}
		else
		{
			Node.Last = Nodes[Left].Last;
		}
	}
	int New(int Value, int Parent)
	{
		int u = ++Used;
		Nodes[u].Value = Value;
		Nodes[u].Minimum = Value;
		Nodes[u].Size = 1;
		Nodes[u].Parent = Parent;
		return u;
	}
	int Build(const std::vector<int>& Values, int Left, int Right, int Parent)
	{
		if (Left > Right)
		{
			return 0;
		}
		int Middle = (Left + Right) / 2;
		int u = New(Values[Middle], Parent);
		Nodes[u].Child[0] = Build(Values, Left, Middle - 1, u);
		Nodes[u].Child[1] = Build(Values, Middle + 1, Right, u);
		Pull(u);
		return u;
	}
	void Rotate(int u)
	{
		int p = Nodes[u].Parent;
		int g = Nodes[p].Parent;
		int Side = Nodes[p].Child[1] == u;
		int Middle = Nodes[u].Child[Side ^ 1];
		if (g != 0)
		{
			Nodes[g].Child[Nodes[g].Child[1] == p] = u;
		}
		Nodes[u].Parent = g;
		Nodes[u].Child[Side ^ 1] = p;
		Nodes[p].Parent = u;
		Nodes[p].Child[Side] = Middle;
		if (Middle != 0)
		{
			Nodes[Middle].Parent = p;
		}
		Pull(p);
		Pull(u);
	}
	void Splay(int u, int Target = 0)
	{
		Pull(u);
		while (Nodes[u].Parent != Target)
		{
			int p = Nodes[u].Parent;
			int g = Nodes[p].Parent;
			if (g != Target)
			{
				bool bSame = (Nodes[g].Child[1] == p) == (Nodes[p].Child[1] == u);
				Rotate(bSame ? p : u);
			}
			Rotate(u);
		}
		if (Target == 0)
		{
			Root = u;
		}
	}
	int At(int Position) const
	{
		int u = Root;
		while (Nodes[Nodes[u].Child[0]].Size != Position)
		{
			int LeftSize = Nodes[Nodes[u].Child[0]].Size;
			if (Position < LeftSize)
			{
				u = Nodes[u].Child[0];
			}
			else
			{
				Position -= LeftSize + 1;
				u = Nodes[u].Child[1];
			}
		}
		return u;
	}
	void Change(int Position, int Value)
	{
		int u = At(Position);
		Nodes[u].Value = Value;
		Splay(u);
	}
	void Insert(int Position, int Value)
	{
		int Left = At(Position - 1);
		Splay(Left);
		int Right = At(Position);
		Splay(Right, Left);
		Nodes[Right].Child[0] = New(Value, Right);
		Pull(Right);
		Pull(Left);
	}
	void Erase(int Position)
	{
		int Left = At(Position - 1);
		Splay(Left);
		int Right = At(Position + 1);
		Splay(Right, Left);
		Nodes[Right].Child[0] = 0;
		Pull(Right);
		Pull(Left);
	}
	bool Wins(int n) const
	{
		if (n == 0)
		{
			return false;
		}
		const FNode& Node = Nodes[Root];
		if (Node.Minimum > 0 && (n & 1))
		{
			return true;
		}
		return ((Node.First - 1) & 1) || ((n - Node.Last) & 1);
	}
};
int main()
{
	FInput Input;
	int n = Input.Read();
	int q = Input.Read();
	std::vector<int> Values(n + 2, 101);
	for (int i = 1; i <= n; ++i)
	{
		Values[i] = Input.Read();
	}
	FSplay Tree(n + q + 5);
	Tree.Root = Tree.Build(Values, 0, n + 1, 0);
	std::printf("%d\n", Tree.Wins(n) ? 1 : 0);
	for (int i = 0; i < q; ++i)
	{
		int Operation = Input.Read();
		int Position = Input.Read();
		if (Operation == 1)
		{
			Tree.Change(Position, Input.Read());
		}
		else if (Operation == 2)
		{
			Tree.Insert(Position, Input.Read());
			++n;
		}
		else
		{
			Tree.Erase(Position);
			--n;
		}
		std::printf("%d\n", Tree.Wins(n) ? 1 : 0);
	}
}
