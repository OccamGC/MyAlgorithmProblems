// Codex (GPT-6): direct geometric-power moments; constant-time coefficient updates.

#include <iostream>
#include <vector>
using Integer = long long;
constexpr Integer Mod = 1000000007;
Integer Power(Integer Base, Integer Exponent)
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
std::vector<Integer> Inverses(int Degree)
{
	std::vector<Integer> Result(Degree + 1, 1);
	for (int i = 2; i <= Degree; ++i)
	{
		Result[i] = Mod - (Mod / i) * Result[Mod % i] % Mod;
	}
	return Result;
}

std::vector<std::vector<Integer>> Binomial(int Degree)
{
	std::vector<std::vector<Integer>> Result(Degree + 1, std::vector<Integer>(Degree + 1));
	for (int i = 0; i <= Degree; ++i)
	{
		Result[i][0] = Result[i][i] = 1;
		for (int j = 1; j < i; ++j)
		{
			Result[i][j] = (Result[i - 1][j - 1] + Result[i - 1][j]) % Mod;
		}
	}
	return Result;
}

std::vector<Integer> Moments(Integer n, int k, Integer a, const std::vector<std::vector<Integer>>& Choose, const std::vector<Integer>& Reciprocal)
{
	std::vector<Integer> Sum(k + 1);
	Integer Inverse = Power((1 - a + Mod) % Mod, Mod - 2);
	Integer Boundary = Power(a, n + 1);
	Integer nPower = 1;
	Integer EndPower = n + 1;
	for (int j = 0; j <= k; ++j)
	{
		if (a == 1)
		{
			Integer Value = (EndPower + Mod - 1) % Mod;
			for (int t = 0; t < j; ++t)
			{
				Value = (Value - Choose[j + 1][t] * Sum[t] % Mod + Mod) % Mod;
			}
			Sum[j] = Value * Reciprocal[j + 1] % Mod;
		}
		else
		{
			Integer Value = (j == 0 ? a : 0) - Boundary * nPower % Mod;
			Value = (Value + Mod) % Mod;
			for (int t = 0; t < j; ++t)
			{
				Integer Term = Choose[j][t] * Sum[t] % Mod;
				Value = (Value + ((j - t) & 1 ? Term : Mod - Term)) % Mod;
			}
			Sum[j] = Value * Inverse % Mod;
		}
		nPower = nPower * n % Mod;
		EndPower = EndPower * (n + 1) % Mod;
	}
	return Sum;
}
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	Integer n;
	int m;
	int k;
	Integer a;
	std::cin >> n >> m >> k >> a;
	std::vector<Integer> b(k + 1);
	for (Integer& Value : b)
	{
		std::cin >> Value;
	}
	auto Choose = Binomial(k + 1);
	auto Reciprocal = Inverses(k + 1);
	auto Sum = Moments(n, k, a, Choose, Reciprocal);
	Integer Answer = 0;
	for (int j = 0; j <= k; ++j)
	{
		Answer = (Answer + b[j] * Sum[j]) % Mod;
	}
	std::cout << Answer << '\n';
	for (int Query = 0; Query < m; ++Query)
	{
		int Type;
		std::cin >> Type;
		if (Type == 1)
		{
			std::cin >> n;
			Sum = Moments(n, k, a, Choose, Reciprocal);
			Answer = 0;
			for (int j = 0; j <= k; ++j)
			{
				Answer = (Answer + b[j] * Sum[j]) % Mod;
			}
		}
		else
		{
			int j;
			Integer Value;
			std::cin >> j >> Value;
			Answer = (Answer + (Value - b[j] + Mod) % Mod * Sum[j]) % Mod;
			b[j] = Value;
		}
		std::cout << Answer << '\n';
	}
}
