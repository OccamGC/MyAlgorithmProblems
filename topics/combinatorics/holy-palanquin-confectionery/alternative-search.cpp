// Problem setter's solution: canonical nondecreasing purchases with zero pruning.
// Codex (GPT-6): modular accumulation, cleaned output and portable implementation.
#include <iostream>

constexpr long long Mod = 998244353;
long long Answer = 0;

void Search(int Price, int Remaining)
{
	if (Price + 1 < Remaining)
	{
		Search(Price + 1, Remaining);
	}
	Remaining -= Price;
	Answer = (Answer + Remaining) % Mod;
	if (Remaining > Price)
	{
		Search(Price, Remaining);
	}
}

int main()
{
	int X;
	std::cin >> X;
	Answer = X;
	if (X > 0)
	{
		Search(1, X);
	}
	std::cout << Answer << '\n';
}
