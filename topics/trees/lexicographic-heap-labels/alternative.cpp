// Codex (GPT-6): ancestor-set characterization, proof and static sorting solution using classical persistent segment trees.

#include <algorithm>
#include <array>
#include <cstdio>
#include <iterator>
#include <map>
#include <string>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

class FInput
{
	char Buffer[1 << 16];
	int Position = 0;
	int Length = 0;
public:
	int Get()
	{
		if (Position == Length)
		{
			Length = static_cast<int>(std::fread(Buffer, 1, sizeof(Buffer), stdin));
			Position = 0;
			if (Length == 0)
			{
				return EOF;
			}
		}
		return Buffer[Position++];
	}
	int Read()
	{
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		bool bNegative = Character == '-';
		if (bNegative)
		{
			Character = Get();
		}
		long long Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return static_cast<int>(bNegative ? -Value : Value);
	}
	std::string Token()
	{
		std::string Result;
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		while (Character > ' ' && Character != EOF)
		{
			Result.push_back(static_cast<char>(Character));
			Character = Get();
		}
		return Result;
	}
};

class FOutput
{
	char Buffer[1 << 16];
	int Length = 0;
public:
	void Put(char Character)
	{
		if (Length == static_cast<int>(sizeof(Buffer)))
		{
			Flush();
		}
		Buffer[Length++] = Character;
	}
	void Write(long long Value, char End = '\n')
	{
		if (Value < 0)
		{
			Put('-');
			Value = -Value;
		}
		char Digits[24];
		int Count = 0;
		do
		{
			Digits[Count++] = static_cast<char>('0' + Value % 10);
			Value /= 10;
		} while (Value > 0);
		while (Count > 0)
		{
			Put(Digits[--Count]);
		}
		Put(End);
	}
	void Flush()
	{
		std::fwrite(Buffer, 1, Length, stdout);
		Length = 0;
	}
	~FOutput()
	{
		Flush();
	}
};

class FFenwick
{
	std::vector<int> Tree;
public:
	explicit FFenwick(int n) : Tree(n + 1)
	{
	}
	void Add(int Position, int Value)
	{
		for (; Position < static_cast<int>(Tree.size()); Position += Position & -Position)
		{
			Tree[Position] += Value;
		}
	}
	int Sum(int Position) const
	{
		int Result = 0;
		for (; Position > 0; Position -= Position & -Position)
		{
			Result += Tree[Position];
		}
		return Result;
	}
};

struct FRootedTree
{
	int n;
	int Root;
	std::vector<std::vector<int>> Edges;
	std::vector<int> Parent;
	std::vector<int> Order;
	std::vector<int> In;
	std::vector<int> Out;
	std::vector<int> Size;
	explicit FRootedTree(FInput& Input)
	{
		n = Input.Read();
		Root = Input.Read();
		Edges.resize(n + 1);
		Parent.resize(n + 1);
		In.resize(n + 1);
		Out.resize(n + 1);
		Size.assign(n + 1, 1);
		for (int i = 1; i < n; ++i)
		{
			int u = Input.Read();
			int v = Input.Read();
			Edges[u].push_back(v);
			Edges[v].push_back(u);
		}
		std::vector<int> Stack{Root};
		int Timer = 0;
		while (!Stack.empty())
		{
			int u = Stack.back();
			Stack.pop_back();
			if (u < 0)
			{
				u = -u;
				Out[u] = ++Timer;
				Size[Parent[u]] += Size[u];
				continue;
			}
			In[u] = ++Timer;
			Order.push_back(u);
			Stack.push_back(-u);
			for (int v : Edges[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Stack.push_back(v);
				}
			}
		}
	}
};

void PrintRank(const std::vector<int>& Labels, FOutput& Output)
{
	int n = static_cast<int>(Labels.size()) - 1;
	constexpr std::array<int, 2> Moduli{100000007, 100000009};
	std::array<long long, 2> Factorial{1, 1};
	std::array<long long, 2> Answer{};
	FFenwick Counts(n);
	for (int i = n; i >= 1; --i)
	{
		int Smaller = Counts.Sum(Labels[i] - 1);
		for (int j = 0; j < 2; ++j)
		{
			Answer[j] = (Answer[j] + Smaller * Factorial[j]) % Moduli[j];
			Factorial[j] = Factorial[j] * (n - i + 1) % Moduli[j];
		}
		Counts.Add(Labels[i], 1);
	}
	Output.Write(Answer[0], ' ');
	Output.Write(Answer[1]);
}

class FPersistentSet
{
	struct FNode
	{
		int Left = 0;
		int Right = 0;
	};
	int n;
	std::vector<FNode> Nodes{FNode{}};
	int Insert(int Previous, int Left, int Right, int Position)
	{
		int Node = static_cast<int>(Nodes.size());
		Nodes.push_back(Nodes[Previous]);
		if (Left != Right)
		{
			int Middle = (Left + Right) / 2;
			if (Position <= Middle)
			{
				int Child = Insert(Nodes[Previous].Left, Left, Middle, Position);
				Nodes[Node].Left = Child;
			}
			else
			{
				int Child = Insert(Nodes[Previous].Right, Middle + 1, Right, Position);
				Nodes[Node].Right = Child;
			}
		}
		return Node;
	}
public:
	explicit FPersistentSet(int Count) : n(Count)
	{
		int Levels = 1;
		while ((1 << Levels) < n)
		{
			++Levels;
		}
		Nodes.reserve(static_cast<std::size_t>(n) * (Levels + 1) + 1);
	}
	int Insert(int Previous, int Position)
	{
		return Insert(Previous, 1, n, Position);
	}
	bool Greater(int First, int Second) const
	{
		if (First == Second)
		{
			return false;
		}
		int Left = 1;
		int Right = n;
		while (Left != Right)
		{
			int Middle = (Left + Right) / 2;
			if (Nodes[First].Left != Nodes[Second].Left)
			{
				First = Nodes[First].Left;
				Second = Nodes[Second].Left;
				Right = Middle;
			}
			else
			{
				First = Nodes[First].Right;
				Second = Nodes[Second].Right;
				Left = Middle + 1;
			}
		}
		return First != 0;
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FRootedTree Tree(Input);
	FPersistentSet Sets(Tree.n);
	std::vector<int> Versions(Tree.n + 1);
	for (int u : Tree.Order)
	{
		Versions[u] = Sets.Insert(Versions[Tree.Parent[u]], u);
	}
	std::vector<int> Sorted = Tree.Order;
	std::sort(Sorted.begin(), Sorted.end(), [&](int u, int v)
	{
		return Sets.Greater(Versions[u], Versions[v]);
	});
	std::vector<int> Labels(Tree.n + 1);
	for (int i = 0; i < Tree.n; ++i)
	{
		Labels[Sorted[i]] = Tree.n - i;
	}
	PrintRank(Labels, Output);
}
