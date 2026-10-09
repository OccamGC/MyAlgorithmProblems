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

class FPostal
{
	static constexpr long long Infinity = 1LL << 60;
	int n;
	std::vector<long long> Position;
	std::vector<long long> Prefix;
	std::vector<long long> Previous;
	std::vector<long long> Current;
	std::vector<long long> Costs;
	long long Cost(int Left, int Right) const
	{
		return Costs[static_cast<std::size_t>(Left) * (n + 1) + Right];
	}

	void Compute(int Left, int Right, int First, int Last)
	{
		if (Left > Right)
		{
			return;
		}
		int Middle = (Left + Right) / 2;
		int Best = First;
		long long Value = Infinity;
		for (int Split = First; Split <= std::min(Last, Middle - 1); ++Split)
		{
			long long Candidate = Previous[Split] + Cost(Split, Middle);
			if (Candidate < Value)
			{
				Value = Candidate;
				Best = Split;
			}
		}
		Current[Middle] = Value;
		Compute(Left, Middle - 1, First, Best);
		Compute(Middle + 1, Right, Best, Last);
	}
public:
	void Run(FInput& Input, FOutput& Output)
	{
		n = Input.Read();
		int m = Input.Read();
		Position.resize(n + 1);
		Prefix.resize(n + 1);
		for (int i = 1; i <= n; ++i)
		{
			Position[i] = Input.Read();
		}
		std::sort(Position.begin() + 1, Position.end());
		for (int i = 1; i <= n; ++i)
		{
			Prefix[i] = Prefix[i - 1] + Position[i];
		}
		Costs.resize(static_cast<std::size_t>(n + 1) * (n + 1));
		for (int Left = 1; Left <= n; ++Left)
		{
			int Split = Left;
			for (int Right = Left + 1; Right <= n; ++Right)
			{
				while (Split + 1 < Right && Position[Split + 1] - Position[Left] <= Position[Right] - Position[Split + 1])
				{
					++Split;
				}
				Costs[static_cast<std::size_t>(Left) * (n + 1) + Right] = Prefix[Split] - Prefix[Left] - Position[Left] * (Split - Left)
					+ Position[Right] * (Right - Split - 1LL) - (Prefix[Right - 1] - Prefix[Split]);
			}
		}
		Previous.assign(n + 1, Infinity);
		Current.resize(n + 1);
		for (int i = 1; i <= n; ++i)
		{
			Previous[i] = Position[i] * (i - 1LL) - Prefix[i - 1];
		}
		for (int Count = 2; Count <= m; ++Count)
		{
			std::fill(Current.begin(), Current.end(), Infinity);
			Compute(Count, n, Count - 1, n - 1);
			Previous.swap(Current);
		}
		long long Answer = Infinity;
		for (int i = m; i <= n; ++i)
		{
			Answer = std::min(Answer, Previous[i] + Prefix[n] - Prefix[i] - Position[i] * (n - i));
		}
		Output.Write(Answer);
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FPostal Solver;
	Solver.Run(Input, Output);
}
