// Codex (GPT-6): canonical run-count proof, prefix DP, transition tables and implementation. Finite-state DP is a classical technique.

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

class FPrefixStates
{
	std::array<std::array<unsigned short, 512>, 11> WithoutPair{};
	std::array<std::array<unsigned short, 512>, 11> NewPair{};
public:
	FPrefixStates()
	{
		for (int Count = 0; Count <= 10; ++Count)
		{
			for (int Mask = 1; Mask < 512; ++Mask)
			{
				for (int State = 0; State < 9; ++State)
				{
					if ((Mask & (1 << State)) == 0)
					{
						continue;
					}
					int x = State / 3;
					int y = State % 3;
					for (int Pair = 0; Pair < 2; ++Pair)
					{
						int z = ((Count - x - y - 2 * Pair) % 3 + 3) % 3;
						if (Count >= x + y + z + 2 * Pair)
						{
							auto& Table = Pair == 0 ? WithoutPair : NewPair;
							Table[Count][Mask] |= 1 << (3 * y + z);
						}
					}
				}
			}
		}
	}
	void Run(FInput& Input, FOutput& Output) const
	{
		int n = Input.Read();
		int First = 1;
		int Second = 0;
		for (int i = 0; i < n; ++i)
		{
			int Count = Input.Read();
			int Kind = Count < 8 ? Count : 8 + (Count - 8) % 3;
			Second = WithoutPair[Kind][Second] | NewPair[Kind][First];
			First = WithoutPair[Kind][First];
			Output.Write(First & 1, ' ');
			Output.Write(Second & 1);
		}
	}
};

int main()
{
	FInput Input;
	FOutput Output;
	FPrefixStates Solver;
	Solver.Run(Input, Output);
}
