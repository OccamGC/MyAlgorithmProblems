// Setter direction: inclusion-exclusion and Stirling numbers.
// Codex (GPT-6): correct surjection counting, precise leaf identities, boundary cases, and verification.
#include <iostream>
#include <vector>
using Integer = long long;
constexpr Integer Mod = 998244353;
Integer Power(Integer Base, int Exponent)
{
	Integer Result = 1;
	while (Exponent)
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
	int n;
	int m;
	std::cin >> n >> m;
	if (n <= 2)
	{
		std::cout << (n == m) << '\n';
		return 0;
	}
	if (m < 2 || m >= n)
	{
		std::cout << 0 << '\n';
		return 0;
	}
	std::vector<Integer> Factorial(n + 1, 1);
	std::vector<Integer> Inverse(n + 1, 1);
	for (int i = 1; i <= n; ++i)
	{
		Factorial[i] = Factorial[i - 1] * i % Mod;
	}
	Inverse[n] = Power(Factorial[n], Mod - 2);
	for (int i = n; i > 0; --i)
	{
		Inverse[i - 1] = Inverse[i] * i % Mod;
	}
	int Internal = n - m;
	Integer Onto = 0;
	for (int j = 0; j <= Internal; ++j)
	{
		Integer Choose = Factorial[Internal] * Inverse[j] % Mod * Inverse[Internal - j] % Mod;
		Integer Term = Choose * Power(Internal - j, n - 2) % Mod;
		Onto = (Onto + (j & 1 ? Mod - Term : Term)) % Mod;
	}
	Integer Answer = Factorial[n] * Inverse[m] % Mod * Inverse[Internal] % Mod;
	Answer = Answer * Onto % Mod * Factorial[n - 1] % Mod;
	std::cout << Answer << '\n';
}
