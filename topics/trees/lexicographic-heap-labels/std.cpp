// Problem setter's component sizes, ancestor jumps and label intervals. Codex (GPT-6): proof, specified moduli, iterative DFS and portable implementation.

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

class FOccupied
{
	int n;
	std::vector<char> Present;
	void Insert(int Node, int Left, int Right, int Position)
	{
		Present[Node] = true;
		if (Left == Right)
		{
			return;
		}
		int Middle = (Left + Right) / 2;
		if (Position <= Middle)
		{
			Insert(Node * 2, Left, Middle, Position);
		}
		else
		{
			Insert(Node * 2 + 1, Middle + 1, Right, Position);
		}
	}
	int First(int Node, int Left, int Right, int Begin, int End) const
	{
		if (!Present[Node] || Right < Begin || Left > End)
		{
			return End + 1;
		}
		if (Left == Right)
		{
			return Left;
		}
		int Middle = (Left + Right) / 2;
		int Result = First(Node * 2, Left, Middle, Begin, End);
		return Result <= End ? Result : First(Node * 2 + 1, Middle + 1, Right, Begin, End);
	}
public:
	explicit FOccupied(int Count) : n(Count), Present(4 * n + 4)
	{
	}
	void Insert(int Position)
	{
		Insert(1, 1, n, Position);
	}
	int First(int Begin, int End) const
	{
		return First(1, 1, n, Begin, End);
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FRootedTree Tree(Input);
	int n = Tree.n;
	int Levels = 1;
	while ((1 << Levels) <= n)
	{
		++Levels;
	}
	std::vector<std::vector<int>> Jump(Levels, std::vector<int>(n + 1));
	std::vector<std::vector<int>> Minimum = Jump;
	Jump[0] = Tree.Parent;
	Minimum[0] = Tree.Parent;
	for (int j = 1; j < Levels; ++j)
	{
		for (int u = 1; u <= n; ++u)
		{
			int Middle = Jump[j - 1][u];
			Jump[j][u] = Jump[j - 1][Middle];
			Minimum[j][u] = std::min(Minimum[j - 1][u], Minimum[j - 1][Middle]);
		}
	}
	std::vector<int> Labels(n + 1);
	std::vector<int> Right(n + 1);
	Right[0] = n;
	FFenwick Corrections(2 * n);
	FOccupied Occupied(n);
	for (int u = 1; u <= n; ++u)
	{
		int Ancestor = u;
		for (int j = Levels - 1; j >= 0; --j)
		{
			if (Minimum[j][Ancestor] > u)
			{
				Ancestor = Jump[j][Ancestor];
			}
		}
		int Top = Tree.Parent[Ancestor];
		int Count = Tree.Size[u] + Corrections.Sum(Tree.In[u]) - Corrections.Sum(Tree.Out[u]);
		if (Top != Tree.Parent[u])
		{
			Corrections.Add(Tree.In[Top] + 1, -Count);
			Corrections.Add(Tree.In[u], Count);
		}
		Labels[u] = Occupied.First(Labels[Top] + 1, Right[Top]) - Count;
		Right[u] = Labels[u] + Count - 1;
		Occupied.Insert(Labels[u]);
	}
	PrintRank(Labels, Output);
}
