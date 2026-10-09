// Codex (GPT-6): transpose the optimal averaging grid and sum its coefficients.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

using Int64 = std::int64_t;
constexpr Int64 Mod = 1000000007;
constexpr Int64 Half = (Mod + 1) / 2;

Int64 Power(Int64 Base, Int64 Exponent)
{
	Int64 Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Mod;
		}
		Base = Base * Base % Mod;
		Exponent >>= 1;
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	Int64 k, InitialMoney;
	std::cin >> n >> k >> InitialMoney;
	std::vector<int> Rich;
	for (int i = 1; i < n; ++i)
	{
		int People, Money;
		std::cin >> People >> Money;
		if (People == 1 && Money * k > InitialMoney)
		{
			Rich.push_back(Money);
		}
	}
	std::sort(Rich.begin(), Rich.end(), [](int A, int B)
	{
		return A > B;
	});
	if (Rich.empty())
	{
		std::cout << InitialMoney % Mod << '\n';
		return 0;
	}
	std::vector<int> Inverse(Rich.size() + 1);
	Inverse[1] = 1;
	for (int i = 2; i <= static_cast<int>(Rich.size()); ++i)
	{
		Inverse[i] = static_cast<int>(Mod - Mod / i * Inverse[Mod % i] % Mod);
	}
	const Int64 InitialMean = InitialMoney * Power(k, Mod - 2) % Mod;
	Int64 Coefficient = Power(Half, k);
	Int64 Prefix = 0;
	Int64 Answer = InitialMoney % Mod;
	for (int d = 0; d < static_cast<int>(Rich.size()); ++d)
	{
		if (d > 0)
		{
			Coefficient = Coefficient * (k + d - 1) % Mod * Half % Mod * Inverse[d] % Mod;
		}
		Prefix = (Prefix + Coefficient) % Mod;
		const Int64 Difference = (Rich[d] - InitialMean + Mod) % Mod;
		Answer = (Answer + Difference * (1 - Prefix + Mod)) % Mod;
	}
	std::cout << Answer << '\n';
}
