// Codex (GPT-6): derive and implement global affine updates for this shuffle.
// Original probability and expectation recurrences are preserved as alternatives.

#include <iostream>
#include <vector>

constexpr long long Mod = 998244353;

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent % 2 == 1)
		{
			Result = Result * Base % Mod;
		}
		Base = Base * Base % Mod;
		Exponent /= 2;
	}
	return Result;
}

// The input sum is invariant under swaps. Values may also be indicator variables.
void Transform(std::vector<long long>& Value, long long InvN, long long Alpha, long long InvAlpha)
{
	int n = static_cast<int>(Value.size());
	long long Mean = 0;
	for (long long x : Value)
	{
		Mean = (Mean + x) % Mod;
	}
	Mean = Mean * InvN % Mod;
	long long Scale = 1;
	long long Shift = 0;
	long long InvScale = 1;
	for (int i = 0; i < n; ++i)
	{
		long long Current = (Scale * Value[i] + Shift) % Mod;
		Scale = Scale * Alpha % Mod;
		Shift = (Shift * Alpha + Current * InvN) % Mod;
		InvScale = InvScale * InvAlpha % Mod;
		Value[i] = (Mean - Shift + Mod) * InvScale % Mod;
	}
	for (long long& x : Value)
	{
		x = (Scale * x + Shift) % Mod;
	}
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<long long> Value(n);
	for (long long& x : Value)
	{
		std::cin >> x;
	}
	if (n > 1)
	{
		long long InvN = Power(n, Mod - 2);
		long long Alpha = (n - 1) * InvN % Mod;
		Transform(Value, InvN, Alpha, Power(Alpha, Mod - 2));
	}
	for (int i = 0; i < n; ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Value[i];
	}
	std::cout << '\n';
}
