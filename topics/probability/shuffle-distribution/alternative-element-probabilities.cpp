// Problem setter's element-location recurrence, adapted to value probabilities.
// Codex (GPT-6): aggregate same-value elements and implement the matrix output.

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
	std::vector<std::vector<long long>> Answer(n, std::vector<long long>(n, 0));
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
			Answer[j][a[Source] - 1] = (Answer[j][a[Source] - 1] + Probability[j]) % Mod;
		}
	}

	for (const auto& Row : Answer)
	{
		for (int j = 0; j < n; ++j)
		{
			std::cout << (j == 0 ? "" : " ") << Row[j];
		}
		std::cout << '\n';
	}

}
