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

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Values(n + 1);
	int Levels = 1;
	while ((1 << Levels) <= n)
	{
		++Levels;
	}
	std::vector<int> Jump(static_cast<std::size_t>(n + 1) * Levels);
	std::vector<int> ChainLength(n + 1);
	std::vector<int> Logarithm(n + 1);
	std::vector<int> Stack;
	Stack.reserve(n);
	for (int i = 1; i <= n; ++i)
	{
		Values[i] = Input.Read();
		while (!Stack.empty() && Values[Stack.back()] <= Values[i])
		{
			Stack.pop_back();
		}
		int Previous = Stack.empty() ? 0 : Stack.back();
		int Base = i * Levels;
		Jump[Base] = Previous;
		ChainLength[i] = ChainLength[Previous] + 1;
		Logarithm[i] = Logarithm[i / 2] + 1;
		for (int Level = 1; Level < Levels; ++Level)
		{
			Jump[Base + Level] = Jump[Jump[Base + Level - 1] * Levels + Level - 1];
		}
		Stack.push_back(i);
	}
	for (int Query = 0; Query < m; ++Query)
	{
		int Left = Input.Read();
		int Right = Input.Read();
		int Answer = 1;
		for (int Level = Logarithm[ChainLength[Right]] - 1; Level >= 0; --Level)
		{
			int Destination = Jump[Right * Levels + Level];
			if (Destination >= Left)
			{
				Answer += 1 << Level;
				Right = Destination;
			}
		}
		Output.Write(Answer);
	}
}
