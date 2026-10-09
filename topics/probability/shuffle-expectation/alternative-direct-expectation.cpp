// Original editorial solution: update all position expectations after each swap.
// Codex (GPT-6): rolling storage and explicit handling of simultaneous updates.

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

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<long long> Expected(n);
	long long Sum = 0;
	for (long long& x : Expected)
	{
		std::cin >> x;
		Sum += x;
	}
	long long InvN = Power(n, Mod - 2);
	long long Alpha = (n - 1) * InvN % Mod;
	long long Mean = Sum * InvN % Mod;
	for (int i = 0; i < n; ++i)
	{
		long long Current = Expected[i];
		for (int j = 0; j < n; ++j)
		{
			if (j != i)
			{
				Expected[j] = (Alpha * Expected[j] + InvN * Current) % Mod;
			}
		}
		Expected[i] = Mean;
	}
	for (int i = 0; i < n; ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Expected[i];
	}
	std::cout << '\n';
}
