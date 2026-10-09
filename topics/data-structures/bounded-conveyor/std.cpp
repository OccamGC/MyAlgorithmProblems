// Problem setter's solution: sentinel-slot circular queue.
// Codex (GPT-6): portable buffered input, signed endpoints and implementation cleanup.
#include <cstdio>
#include <cstdlib>
#include <cstdint>

struct FInput
{
	char Buffer[4096];
	int Position = 0;
	int Length = 0;
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
		return static_cast<unsigned char>(Buffer[Position++]);
	}
	int Read()
	{
		int c = Get();
		while (c != EOF && c <= ' ')
		{
			c = Get();
		}
		bool bNegative = c == '-';
		if (bNegative)
		{
			c = Get();
		}
		std::int64_t Value = 0;
		while (c >= '0' && c <= '9')
		{
			Value = Value * 10 + c - '0';
			c = Get();
		}
		return static_cast<int>(bNegative ? -Value : Value);
	}
};

struct FQueue
{
	int* Data;
	int Length;
	int Head = 0;
	int Tail = 0;
	int Next(int Position) const
	{
		return Position + 1 == Length ? 0 : Position + 1;
	}
	void Insert(int Value)
	{
		int After = Next(Tail);
		if (After != Head)
		{
			Data[Tail] = Value;
			Tail = After;
		}
	}
	void Pop()
	{
		if (Head != Tail)
		{
			std::printf("%d\n", Data[Head]);
			Head = Next(Head);
		}
	}
};

int main()
{
	FInput Reader;
	int n = Reader.Read();
	int m = Reader.Read();
	FQueue Conveyor;
	Conveyor.Length = n + 1;
	Conveyor.Data = static_cast<int*>(std::malloc(sizeof(int) * Conveyor.Length));
	if (Conveyor.Data == nullptr)
	{
		return 1;
	}
	for (int i = 0; i < m; ++i)
	{
		int Operation = Reader.Read();
		if (Operation == 1)
		{
			Conveyor.Insert(Reader.Read());
		}
		else
		{
			Conveyor.Pop();
		}
	}
	std::free(Conveyor.Data);
}
