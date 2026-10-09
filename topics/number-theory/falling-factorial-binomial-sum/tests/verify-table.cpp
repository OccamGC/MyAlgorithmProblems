// Codex (GPT-6): verify each interval in reverse order with runtime division.
// Also verify the six remaining factors with Wilson's theorem.
#include <cstdio>
#include "../factorial-table.hpp"

int main()
{
	volatile unsigned long long Divisor = 1000000007;
	unsigned long long Product = 1;
	if (FactorialCheckpoint[0] != 1)
	{
		return 1;
	}
	for (int Block = 1; Block <= 1000; ++Block)
	{
		for (int i = Block * CheckpointStep; i > (Block - 1) * CheckpointStep; --i)
		{
			Product = Product * i % Divisor;
		}
		if (Product != static_cast<unsigned long long>(FactorialCheckpoint[Block]))
		{
			std::fprintf(stderr, "Checkpoint %d failed\n", Block);
			return 1;
		}
	}
	for (int i = 1000000006; i > 1000000000; --i)
	{
		Product = Product * i % Divisor;
	}
	if (Product != Divisor - 1)
	{
		return 1;
	}
	std::puts("1001 checkpoints and Wilson remainder passed");
}
