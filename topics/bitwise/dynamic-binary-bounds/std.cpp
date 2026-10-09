// Classical digit DP and segment-tree matrix products; derivation and implementation: GPT-6.
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

constexpr int Modulus = 998244353;
constexpr int States = 32;
constexpr int Entries = 243;
using FMatrix = std::array<int, Entries>;
std::array<std::array<int, States>, States> Index;
std::array<int, Entries + 1> Begin;
std::array<int, 1024> LeftIndex;
std::array<int, 1024> RightIndex;

void Prepare()
{
	int Count = 0;
	for (int s = 0; s < States; ++s)
	{
		for (int t = 0; t < States; ++t)
		{
			if ((s & t) == s)
			{
				Index[s][t] = Count++;
			}
		}
	}
	int Term = 0;
	for (int s = 0; s < States; ++s)
	{
		for (int t = 0; t < States; ++t)
		{
			if ((s & t) == s)
			{
				Begin[Index[s][t]] = Term;
				for (int u = 0; u < States; ++u)
				{
					if ((s & u) == s && (u & t) == u)
					{
						LeftIndex[Term] = Index[s][u];
						RightIndex[Term++] = Index[u][t];
					}
				}
			}
		}
	}
	Begin[Entries] = Term;
}

FMatrix Multiply(const FMatrix& Left, const FMatrix& Right)
{
	FMatrix Result{};
	for (int i = 0; i < Entries; ++i)
	{
		std::uint64_t Sum = 0;
		int Block = 0;
		for (int j = Begin[i]; j < Begin[i + 1]; ++j)
		{
			Sum += std::uint64_t(Left[LeftIndex[j]]) * Right[RightIndex[j]];
			if (++Block == 8)
			{
				Sum %= Modulus;
				Block = 0;
			}
		}
		Result[i] = static_cast<int>(Sum % Modulus);
	}
	return Result;
}

FMatrix Leaf(const std::array<std::string, 5>& Bounds, int Position)
{
	FMatrix Result{};
	for (int s = 0; s < States; ++s)
	{
		for (int a = 0; a <= 1; ++a)
		{
			for (int b = 0; b <= 1; ++b)
			{
				std::array<int, 5> Bits{a, b, a & b, a ^ b, a | b};
				int t = s;
				bool bValid = true;
				for (int i = 0; i < 5; ++i)
				{
					if ((s & (1 << i)) == 0)
					{
						int Bound = Bounds[i][Position] - '0';
						if (Bits[i] > Bound)
						{
							bValid = false;
						}
						else if (Bits[i] < Bound)
						{
							t |= 1 << i;
						}
					}
				}
				if (bValid)
				{
					++Result[Index[s][t]];
				}
			}
		}
	}
	return Result;
}

int Normalize(long long Value)
{
	Value %= Modulus;
	return static_cast<int>(Value < 0 ? Value + Modulus : Value);
}

void Print(const FMatrix& Product, FOutput& Output)
{
	std::array<long long, 4> Sums{};
	for (int Subset = 0; Subset < 8; ++Subset)
	{
		int s = ((~Subset) & 7) << 2;
		int Count = (Subset & 1) + ((Subset >> 1) & 1) + ((Subset >> 2) & 1);
		for (int t = 0; t < States; ++t)
		{
			if ((s & t) == s)
			{
				Sums[Count] += Product[Index[s][t]];
			}
		}
	}
	Output.Write(Normalize(Sums[0] - Sums[1] + Sums[2] - Sums[3]), ' ');
	Output.Write(Normalize(Sums[1] - 2 * Sums[2] + 3 * Sums[3]), ' ');
	Output.Write(Normalize(Sums[2] - 3 * Sums[3]), ' ');
	Output.Write(Normalize(Sums[3]), '\n');
}

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::array<std::string, 5> Bounds;
	for (std::string& Row : Bounds)
	{
		Row = Input.Token();
	}
	Prepare();
	int Base = 1;
	while (Base < n)
	{
		Base *= 2;
	}
	std::vector<FMatrix> Tree(2 * Base);
	for (int i = 0; i < Base; ++i)
	{
		if (i < n)
		{
			Tree[Base + i] = Leaf(Bounds, i);
		}
		else
		{
			for (int s = 0; s < States; ++s)
			{
				Tree[Base + i][Index[s][s]] = 1;
			}
		}
	}
	for (int Node = Base - 1; Node > 0; --Node)
	{
		Tree[Node] = Multiply(Tree[Node * 2], Tree[Node * 2 + 1]);
	}
	Print(Tree[1], Output);
	for (int i = 0; i < m; ++i)
	{
		int x = Input.Read() - 1;
		int y = Input.Read();
		int Position = n - y;
		Bounds[x][Position] = Bounds[x][Position] == '0' ? '1' : '0';
		int Node = Base + Position;
		Tree[Node] = Leaf(Bounds, Position);
		while ((Node /= 2) != 0)
		{
			Tree[Node] = Multiply(Tree[Node * 2], Tree[Node * 2 + 1]);
		}
		Print(Tree[1], Output);
	}
}
