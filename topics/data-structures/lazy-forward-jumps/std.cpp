// Problem setter's solution: lazily repair a descending suffix of the jump DP.
// Codex (GPT-6): portable input, explicit validity invariant and boundary handling.
#include <algorithm>
#include <vector>
#include "buffered-input.hpp"

int main()
{
	FInput Input;
	int n = Input.Read();
	int q = Input.Read();
	int Type = Input.Read();
	std::vector<int> Jump(n + 1);
	std::vector<int> Answer(n + 1);
	for (int i = 0; i <= n; ++i)
	{
		Jump[i] = Input.Read();
	}
	int High = n;
	int Odd = 0;
	int Even = 0;
	long long Sum = 0;
	for (int i = 1; i <= q; ++i)
	{
		int Operation = Input.Read();
		int Position = Input.Read();
		if (Operation == 1)
		{
			Jump[Position] = Input.Read();
			High = std::max(High, Position);
		}
		else
		{
			int Value = 0;
			if (Position <= n)
			{
				while (High >= Position)
				{
					int Next = High + Jump[High];
					Answer[High] = Next > n ? 1 : Answer[Next] + 1;
					--High;
				}
				Value = Answer[Position];
			}
			if (Type == 2)
			{
				std::printf("%d\n", Value);
			}
			else
			{
				if (i & 1)
				{
					Odd ^= Value;
				}
				else
				{
					Even ^= Value;
				}
				Sum += Value;
			}
		}
	}
	if (Type == 1)
	{
		std::printf("%d %d %lld\n", Odd, Even, Sum);
	}
}
