// Codex (GPT-6): triangular polynomial antidifference transform with linear coefficient updates.

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
	int Degree = k + (a == 1);
	auto Choose = Binomial(Degree);
	auto Reciprocal = Inverses(Degree);
	std::vector<std::vector<Integer>> Transform(k + 1, std::vector<Integer>(Degree + 1));
	Integer Inverse = Power((a + Mod - 1) % Mod, Mod - 2);
	for (int j = 0; j <= k; ++j)
	{
		for (int t = j; t >= 0; --t)
		{
			int Index = t + (a == 1);
			Integer Sum = 0;
			for (int h = Index + 1; h <= j + (a == 1); ++h)
			{
				Sum = (Sum + Choose[h][t] * Transform[j][h]) % Mod;
			}
			Integer Denominator = a == 1 ? Reciprocal[t + 1] : Inverse;
			Transform[j][Index] = ((t == j) - a * Sum % Mod + Mod) % Mod * Denominator % Mod;
		}
	}
	std::vector<Integer> q(Degree + 1);
	for (int j = 0; j <= k; ++j)
	{
		for (int t = 0; t <= Degree; ++t)
		{
			q[t] = (q[t] + b[j] * Transform[j][t]) % Mod;
		}
	}
	Integer Exponential = Power(a, n + 1);
	for (int Query = 0; Query <= m; ++Query)
	{
		if (Query)
		{
			int Type;
			std::cin >> Type;
			if (Type == 1)
			{
				std::cin >> n;
				Exponential = Power(a, n + 1);
			}
			else
			{
				int j;
				Integer Value;
				std::cin >> j >> Value;
				Integer Delta = (Value - b[j] + Mod) % Mod;
				b[j] = Value;
				for (int t = 0; t <= Degree; ++t)
				{
					q[t] = (q[t] + Delta * Transform[j][t]) % Mod;
				}
			}
		}
		Integer AtEnd = 0;
		Integer AtOne = 0;
		for (int t = Degree; t >= 0; --t)
		{
			AtEnd = (AtEnd * (n + 1) + q[t]) % Mod;
			AtOne = (AtOne + q[t]) % Mod;
		}
		std::cout << (Exponential * AtEnd % Mod - a * AtOne % Mod + Mod) % Mod << '\n';
	}
}
