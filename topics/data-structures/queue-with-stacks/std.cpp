// Problem setter's empty-stack greedy strategy and bottom markers. Codex (GPT-6): proof, empty-input handling and portable implementation.

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

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::string Operations = m == 0 ? std::string{} : Input.Token();
	int Waiting = 0;
	int Needed = 0;
	for (char Operation : Operations)
	{
		if (Operation == '0')
		{
			++Waiting;
		}
		else if (Waiting > 0)
		{
			--Waiting;
			++Needed;
		}
	}
	std::vector<char> Bottom(Needed + 1);
	int Empty = n;
	int Pushed = 0;
	int Popped = 0;
	int Answer = 0;
	for (char Operation : Operations)
	{
		if (Operation == '0' && Pushed < Needed)
		{
			++Pushed;
			if (Empty > 0)
			{
				--Empty;
				Bottom[Pushed] = true;
				Answer += 2;
			}
			else
			{
				Answer += 4;
			}
		}
		else if (Operation == '1' && Popped < Pushed)
		{
			Empty += Bottom[++Popped];
		}
		if (Popped < Pushed && Empty == n)
		{
			--Empty;
			Bottom[Pushed] = true;
		}
	}
	Output.Write(Answer);
}
