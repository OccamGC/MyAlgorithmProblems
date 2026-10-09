// Codex (GPT-6): portable buffered input for the problem's nonnegative integers.
#ifndef BUFFERED_INPUT_HPP
#define BUFFERED_INPUT_HPP
#include <cstdio>
struct FInput
{
	char Buffer[32768];
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
	int NonSpace()
	{
		int c = Get();
		while (c != EOF && c <= ' ')
		{
			c = Get();
		}
		return c;
	}
	int Read()
	{
		int c = NonSpace();
		int Value = 0;
		while (c >= '0' && c <= '9')
		{
			Value = Value * 10 + c - '0';
			c = Get();
		}
		return Value;
	}
};
#endif
