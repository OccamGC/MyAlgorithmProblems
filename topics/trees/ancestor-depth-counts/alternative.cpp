#include <algorithm>
#include <array>
#include <cstdio>
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
		int Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return bNegative ? -Value : Value;
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

struct FTree
{
	int n;
	std::vector<int> Parent;
	std::vector<int> Offset;
	std::vector<int> Neighbor;
	std::vector<int> Depth;
	std::vector<int> Size;
	std::vector<int> Order;
	std::vector<long long> Total;
	explicit FTree(FInput& Input)
	{
		n = Input.Read();
		Parent.resize(n + 1);
		Offset.resize(n + 2);
		Depth.resize(n + 1);
		Size.assign(n + 1, 1);
		Total.resize(n + 1);
		Order.reserve(n);
		for (int i = 2; i <= n; ++i)
		{
			Parent[i] = Input.Read();
			++Offset[i + 1];
			++Offset[Parent[i] + 1];
		}
		for (int i = 1; i <= n + 1; ++i)
		{
			Offset[i] += Offset[i - 1];
		}
		Neighbor.resize(2 * (n - 1));
		{
			std::vector<int> Current = Offset;
			for (int i = 2; i <= n; ++i)
			{
				Neighbor[Current[i]++] = Parent[i];
				Neighbor[Current[Parent[i]]++] = i;
			}
		}
		Order.push_back(1);
		for (int Index = 0; Index < n; ++Index)
		{
			int u = Order[Index];
			for (int e = Offset[u]; e < Offset[u + 1]; ++e)
			{
				int v = Neighbor[e];
				if (v != Parent[u])
				{
					Depth[v] = Depth[u] + 1;
					Order.push_back(v);
				}
			}
		}
		for (int Index = n - 1; Index > 0; --Index)
		{
			int u = Order[Index];
			Size[Parent[u]] += Size[u];
		}
		for (int u : Order)
		{
			Total[u] = Total[Parent[u]] + Size[u];
		}
	}
};

class FPathSums
{
	const FTree& Tree;
	std::vector<int> Heavy;
	std::vector<int> Top;
	std::vector<int> Position;
	std::vector<long long> First;
	std::vector<long long> Second;
	void Add(std::vector<long long>& Values, int Index, long long Delta)
	{
		for (; Index <= Tree.n; Index += Index & -Index)
		{
			Values[Index] += Delta;
		}
	}
	long long Sum(const std::vector<long long>& Values, int Index) const
	{
		long long Result = 0;
		for (; Index > 0; Index -= Index & -Index)
		{
			Result += Values[Index];
		}
		return Result;
	}
	long long Prefix(int Index) const
	{
		return Index * Sum(First, Index) - Sum(Second, Index);
	}
	void AddRange(int Left, int Right)
	{
		Add(First, Left, 1);
		Add(First, Right + 1, -1);
		Add(Second, Left, Left - 1);
		Add(Second, Right + 1, -Right);
	}
public:
	explicit FPathSums(const FTree& InTree)
		: Tree(InTree), Heavy(Tree.n + 1), Top(Tree.n + 1), Position(Tree.n + 1), First(Tree.n + 1), Second(Tree.n + 1)
	{
		for (int u : Tree.Order)
		{
			for (int e = Tree.Offset[u]; e < Tree.Offset[u + 1]; ++e)
			{
				int v = Tree.Neighbor[e];
				if (v != Tree.Parent[u] && (Heavy[u] == 0 || Tree.Size[v] > Tree.Size[Heavy[u]]))
				{
					Heavy[u] = v;
				}
			}
		}
		int Timer = 0;
		for (int u : Tree.Order)
		{
			if (Tree.Parent[u] == 0 || Heavy[Tree.Parent[u]] != u)
			{
				for (int v = u; v != 0; v = Heavy[v])
				{
					Top[v] = u;
					Position[v] = ++Timer;
				}
			}
		}
	}
	void Insert(int Vertex)
	{
		while (Vertex != 0)
		{
			AddRange(Position[Top[Vertex]], Position[Vertex]);
			Vertex = Tree.Parent[Top[Vertex]];
		}
	}
	long long Query(int Vertex) const
	{
		long long Answer = 0;
		while (Vertex != 0)
		{
			Answer += Prefix(Position[Vertex]) - Prefix(Position[Top[Vertex]] - 1);
			Vertex = Tree.Parent[Top[Vertex]];
		}
		return Answer;
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FTree Tree(Input);
	FPathSums Sums(Tree);
	std::vector<long long> Less(Tree.n + 1);
	std::vector<long long> Equal(Tree.n + 1);
	int Start = 0;
	while (Start < Tree.n)
	{
		int End = Start;
		int Depth = Tree.Depth[Tree.Order[Start]];
		while (End < Tree.n && Tree.Depth[Tree.Order[End]] == Depth)
		{
			++End;
		}
		for (int i = Start; i < End; ++i)
		{
			int u = Tree.Order[i];
			Less[u] = Sums.Query(u);
		}
		for (int i = Start; i < End; ++i)
		{
			Sums.Insert(Tree.Order[i]);
		}
		for (int i = Start; i < End; ++i)
		{
			int u = Tree.Order[i];
			Equal[u] = Sums.Query(u) - Less[u];
		}
		Start = End;
	}
	for (int u = 1; u <= Tree.n; ++u)
	{
		Output.Write(Less[u], ' ');
		Output.Write(Equal[u], ' ');
		Output.Write(Tree.Total[u] - Less[u] - Equal[u]);
	}
}
