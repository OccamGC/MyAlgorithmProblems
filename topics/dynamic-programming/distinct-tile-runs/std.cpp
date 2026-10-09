// Codex (GPT-6): finite-state formulation, proof, word-parallel transitions and implementation. Finite-state DP is a classical technique.

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
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

class FRunStates
{
	std::array<std::array<std::uint64_t, 3>, 15> Allowed{};
	std::array<std::uint64_t, 256> Spread{};
	std::uint64_t Advance(std::uint64_t Mask) const
	{
		Mask |= Mask >> 8;
		Mask |= Mask >> 32;
		return Spread[Mask & 255] | (Spread[(Mask >> 16) & 255] << 32);
	}
public:
	FRunStates()
	{
		for (int Mask = 0; Mask < 256; ++Mask)
		{
			for (int Bit = 0; Bit < 8; ++Bit)
			{
				Spread[Mask] |= static_cast<std::uint64_t>((Mask >> Bit) & 1) << (2 * Bit);
			}
		}
		for (int Count = 0; Count <= 14; ++Count)
		{
			for (int State = 0; State < 64; ++State)
			{
				int Required = 0;
				for (int Bit = 0; Bit < 6; ++Bit)
				{
					Required += (State >> Bit) & 1;
				}
				for (int NewRuns = 0; NewRuns <= 2; ++NewRuns)
				{
					int Left = Count - Required - NewRuns;
					if (Left >= 0 && Left != 1 && Left != 2 && Left != 5)
					{
						Allowed[Count][NewRuns] |= std::uint64_t{1} << State;
					}
				}
			}
		}
	}
	std::uint64_t Step(std::uint64_t States, long long Count) const
	{
		int Kind = static_cast<int>(std::min(Count, 14LL));
		std::uint64_t Zero = Advance(States & Allowed[Kind][0]);
		std::uint64_t One = Advance(States & Allowed[Kind][1]);
		std::uint64_t Two = Advance(States & Allowed[Kind][2]);
		return Zero | (One << 1) | (One << 16) | (Two << 17);
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	Input.Read();
	int k = Input.Read();
	std::vector<std::pair<long long, long long>> Records(k);
	for (auto& Record : Records)
	{
		Record.second = Input.Read();
		int Kind = Input.Read();
		int Rank = Input.Read();
		Record.first = (Kind - 1LL) * n + Rank - 1;
	}
	std::sort(Records.begin(), Records.end());
	FRunStates Solver;
	std::uint64_t States = 1;
	long long Previous = -2;
	int Index = 0;
	while (Index < k)
	{
		long long Key = Records[Index].first;
		long long Count = 0;
		while (Index < k && Records[Index].first == Key)
		{
			Count += Records[Index++].second;
		}
		if (Previous < 0 || Key != Previous + 1 || Key / n != Previous / n)
		{
			if ((States & 1) == 0)
			{
				Output.Write(0);
				return 0;
			}
			States = 1;
		}
		States = Solver.Step(States, Count);
		Previous = Key;
	}
	Output.Write(States & 1);
}
