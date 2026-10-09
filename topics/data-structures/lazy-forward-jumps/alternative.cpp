// Codex (GPT-6): application of rooted link-cut trees to dynamic forward jumps.
// No path reversal is needed because every jump points to a larger position.
#include <vector>
#include "buffered-input.hpp"

struct FNode
{
	int Child[2] = {0, 0};
	int Parent = 0;
	int Size = 1;
};
class FLinkCut
{
public:
	std::vector<FNode> Nodes;
	explicit FLinkCut(int Count) : Nodes(Count + 1)
	{
		Nodes[0].Size = 0;
	}
	bool IsRoot(int u) const
	{
		int p = Nodes[u].Parent;
		return p == 0 || (Nodes[p].Child[0] != u && Nodes[p].Child[1] != u);
	}
	void Pull(int u)
	{
		Nodes[u].Size = 1 + Nodes[Nodes[u].Child[0]].Size + Nodes[Nodes[u].Child[1]].Size;
	}
	void Rotate(int u)
	{
		int p = Nodes[u].Parent;
		int g = Nodes[p].Parent;
		int Side = Nodes[p].Child[1] == u;
		int Middle = Nodes[u].Child[Side ^ 1];
		if (!IsRoot(p))
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
	void Splay(int u)
	{
		while (!IsRoot(u))
		{
			int p = Nodes[u].Parent;
			int g = Nodes[p].Parent;
			if (!IsRoot(p))
			{
				bool bSame = (Nodes[g].Child[1] == p) == (Nodes[p].Child[1] == u);
				Rotate(bSame ? p : u);
			}
			Rotate(u);
		}
	}
	void Access(int u)
	{
		int Previous = 0;
		for (int v = u; v != 0; v = Nodes[v].Parent)
		{
			Splay(v);
			Nodes[v].Child[1] = Previous;
			if (Previous != 0)
			{
				Nodes[Previous].Parent = v;
			}
			Pull(v);
			Previous = v;
		}
		Splay(u);
	}
	void Change(int u, int Parent)
	{
		Access(u);
		int Ancestors = Nodes[u].Child[0];
		if (Ancestors != 0)
		{
			Nodes[Ancestors].Parent = 0;
		}
		Nodes[u].Child[0] = 0;
		Pull(u);
		Nodes[u].Parent = Parent;
	}
	int CountJumps(int u)
	{
		Access(u);
		return Nodes[u].Size - 1;
	}
};

int main()
{
	FInput Input;
	int n = Input.Read();
	int q = Input.Read();
	int Type = Input.Read();
	int Exit = n + 2;
	FLinkCut Tree(Exit);
	for (int i = 0; i <= n; ++i)
	{
		int Jump = Input.Read();
		Tree.Nodes[i + 1].Parent = i + Jump > n ? Exit : i + Jump + 1;
	}
	int Odd = 0;
	int Even = 0;
	long long Sum = 0;
	for (int i = 1; i <= q; ++i)
	{
		int Operation = Input.Read();
		int Position = Input.Read();
		if (Operation == 1)
		{
			int Jump = Input.Read();
			Tree.Change(Position + 1, Position + Jump > n ? Exit : Position + Jump + 1);
		}
		else
		{
			int Value = Position > n ? 0 : Tree.CountJumps(Position + 1);
			if (Type == 2)
			{
				std::printf("%d\n", Value);
			}
			else
			{
				if (i & 1)
				{
					Odd ^= Value;
				}
				else
				{
					Even ^= Value;
				}
				Sum += Value;
			}
		}
	}
	if (Type == 1)
	{
		std::printf("%d %d %lld\n", Odd, Even, Sum);
	}
}
