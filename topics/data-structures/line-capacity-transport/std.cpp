// Problem setter's solution; portable implementation and analysis: GPT-6.
#include <queue>
#include <array>
#include <iterator>

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <string>
#include <set>
#include <limits>
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

struct FNode
{
	int NegativeWeight = 0;
	int ZeroWeight = 0;
	int PositiveWeight = 0;
	int MaximumNegative = -1000000000;
	int MinimumPositive = 1000000000;
	int ZeroCount = 0;
	int Lazy = 0;
};

class FFlow
{
	int n;
	std::vector<FNode> Tree;
	std::vector<int> Value;
	std::vector<int> Weight;
	void Pull(int Node)
	{
		FNode& Current = Tree[Node];
		const FNode& Left = Tree[Node * 2];
		const FNode& Right = Tree[Node * 2 + 1];
		Current.NegativeWeight = Left.NegativeWeight + Right.NegativeWeight;
		Current.ZeroWeight = Left.ZeroWeight + Right.ZeroWeight;
		Current.PositiveWeight = Left.PositiveWeight + Right.PositiveWeight;
		Current.MaximumNegative = std::max(Left.MaximumNegative, Right.MaximumNegative);
		Current.MinimumPositive = std::min(Left.MinimumPositive, Right.MinimumPositive);
		Current.ZeroCount = Left.ZeroCount + Right.ZeroCount;
	}
	void Shift(int Node, int Delta)
	{
		Tree[Node].Lazy += Delta;
		Tree[Node].MaximumNegative += Delta;
		Tree[Node].MinimumPositive += Delta;
	}
	void Push(int Node)
	{
		int Delta = Tree[Node].Lazy;
		if (Delta != 0)
		{
			Shift(Node * 2, Delta);
			Shift(Node * 2 + 1, Delta);
			Tree[Node].Lazy = 0;
		}
	}
	void Build(int Node, int l, int r)
	{
		if (l == r)
		{
			Tree[Node].ZeroWeight = Weight[l];
			Tree[Node].ZeroCount = 1;
			return;
		}
		int Middle = (l + r) / 2;
		Build(Node * 2, l, Middle);
		Build(Node * 2 + 1, Middle + 1, r);
		Pull(Node);
	}
	int Query(int Node, int l, int r, int From, int To, int Direction) const
	{
		if (From <= l && r <= To)
		{
			return Tree[Node].ZeroWeight + Direction * (Tree[Node].PositiveWeight - Tree[Node].NegativeWeight);
		}
		// Pending shifts preserve every sign, hence these weight sums remain current.
		int Middle = (l + r) / 2;
		int Result = 0;
		if (From <= Middle)
		{
			Result += Query(Node * 2, l, Middle, From, To, Direction);
		}
		if (To > Middle)
		{
			Result += Query(Node * 2 + 1, Middle + 1, r, From, To, Direction);
		}
		return Result;
	}
	void Change(int Node, int l, int r, int From, int To, int Delta)
	{
		FNode& Current = Tree[Node];
		if (l == r)
		{
			Value[l] += Current.Lazy + Delta;
			Current = FNode{};
			if (Value[l] < 0)
			{
				Current.NegativeWeight = Weight[l];
				Current.MaximumNegative = Value[l];
			}
			else if (Value[l] > 0)
			{
				Current.PositiveWeight = Weight[l];
				Current.MinimumPositive = Value[l];
			}
			else
			{
				Current.ZeroCount = 1;
				Current.ZeroWeight = Weight[l];
			}
			return;
		}
		if (From <= l && r <= To && Current.ZeroCount == 0 &&
			Current.MaximumNegative + Delta != 0 && Current.MinimumPositive + Delta != 0)
		{
			Shift(Node, Delta);
			return;
		}
		Push(Node);
		int Middle = (l + r) / 2;
		if (From <= Middle)
		{
			Change(Node * 2, l, Middle, From, To, Delta);
		}
		if (To > Middle)
		{
			Change(Node * 2 + 1, Middle + 1, r, From, To, Delta);
		}
		Pull(Node);
	}
public:
	explicit FFlow(const std::vector<int>& Distance)
		: n(static_cast<int>(Distance.size())), Tree(4 * n), Value(n), Weight(Distance)
	{
		Build(1, 0, n - 1);
	}
	int Cost(int l, int r, int Direction) const
	{
		return Query(1, 0, n - 1, l, r, Direction);
	}
	void Add(int l, int r, int Delta)
	{
		Change(1, 0, n - 1, l, r, Delta);
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Capacity(n + 2);
	std::set<int> Available;
	for (int i = 1; i <= n; ++i)
	{
		Capacity[i] = Input.Read();
		if (Capacity[i] != 0)
		{
			Available.insert(i);
		}
	}
	Capacity[n + 1] = m + 1;
	Available.insert(n + 1);
	std::vector<int> Distance(n);
	for (int& Value : Distance)
	{
		Value = Input.Read();
	}
	FFlow Flow(Distance);
	long long Answer = 0;
	for (int i = 0; i < m; ++i)
	{
		int p = Input.Read();
		int Destination = p;
		if (Capacity[p] == 0)
		{
			auto Right = Available.lower_bound(p);
			int r = *Right;
			int RightCost = Flow.Cost(p - 1, r - 2, 1);
			int LeftCost = std::numeric_limits<int>::max();
			int l = -1;
			if (Right != Available.begin())
			{
				l = *std::prev(Right);
				LeftCost = Flow.Cost(l - 1, p - 2, -1);
			}
			if (LeftCost <= RightCost)
			{
				Destination = l;
				Answer += LeftCost;
				Flow.Add(l - 1, p - 2, -1);
			}
			else
			{
				Destination = r;
				Answer += RightCost;
				Flow.Add(p - 1, r - 2, 1);
			}
		}
		if (--Capacity[Destination] == 0)
		{
			Available.erase(Destination);
		}
		Output.Write(Answer, '\n');
	}
}
