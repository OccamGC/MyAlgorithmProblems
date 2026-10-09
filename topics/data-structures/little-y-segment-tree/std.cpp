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
	for (int i = 1; i <= n; ++i)
	{
		Values[i] = Input.Read();
	}
	std::vector<int> Head(n + 1, -1);
	std::vector<int> Next(m);
	std::vector<int> Left(m);
	std::vector<int> Answers(m);
	for (int i = 0; i < m; ++i)
	{
		Left[i] = Input.Read();
		int Right = Input.Read();
		Next[i] = Head[Right];
		Head[Right] = i;
	}
	std::vector<int> Stack;
	Stack.reserve(n);
	for (int Right = 1; Right <= n; ++Right)
	{
		while (!Stack.empty() && Values[Stack.back()] <= Values[Right])
		{
			Stack.pop_back();
		}
		Stack.push_back(Right);
		for (int Query = Head[Right]; Query != -1; Query = Next[Query])
		{
			Answers[Query] = static_cast<int>(Stack.end() - std::lower_bound(Stack.begin(), Stack.end(), Left[Query]));
		}
	}
	for (int Answer : Answers)
	{
		Output.Write(Answer);
	}
}
