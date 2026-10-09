// Problem setter's solution: track each original element, then take weighted sums.
// Codex (GPT-6): rolling probability storage and C++17 implementation.

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
	std::vector<int> a(n);
	for (int& x : a)
	{
		std::cin >> x;
	}
	long long InvN = Power(n, Mod - 2);
	long long Alpha = (n - 1) * InvN % Mod;
	std::vector<long long> Answer(n, 0);
	for (int Source = 0; Source < n; ++Source)
	{
		std::vector<long long> Probability(n, 0);
		Probability[Source] = 1;
		for (int i = 0; i < n; ++i)
		{
			long long Current = Probability[i];
			for (int j = 0; j < n; ++j)
			{
				if (j != i)
				{
					Probability[j] = (Alpha * Probability[j] + InvN * Current) % Mod;
				}
			}
			Probability[i] = InvN;
		}
		for (int j = 0; j < n; ++j)
		{
			Answer[j] = (Answer[j] + Probability[j] * a[Source]) % Mod;
		}
	}

	for (int i = 0; i < n; ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Answer[i];
	}
	std::cout << '\n';

}
