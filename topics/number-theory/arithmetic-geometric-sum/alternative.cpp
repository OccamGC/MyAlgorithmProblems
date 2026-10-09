// Codex (GPT-6): concatenate geometric blocks with weighted sums, without division.

#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Modulus = 1000000007;

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Modulus;
		}
		Base = Base * Base % Modulus;
		Exponent >>= 1;
	}
	return Result;
}

struct FBlock
{
	long long Length;
	long long Power;
	long long Sum;
	long long Weighted;
};

FBlock Combine(const FBlock& Left, const FBlock& Right)
{
	const long long Shifted = (Right.Weighted + Left.Length % Modulus * Right.Sum) % Modulus;
	return FBlock
	{
		Left.Length + Right.Length,
		Left.Power * Right.Power % Modulus,
		(Left.Sum + Left.Power * Right.Sum) % Modulus,
		(Left.Weighted + Left.Power * Shifted) % Modulus
	};
}

long long Calculate(long long l, long long r, long long a, long long b, long long c, long long d)
{
	const long long q = Power(c, b);
	long long Remaining = r - l + 1;
	FBlock Result{0, 1, 0, 0};
	FBlock Current{1, q, 1, 0};
	while (Remaining > 0)
	{
		if (Remaining & 1)
		{
			Result = Combine(Result, Current);
		}
		Current = Combine(Current, Current);
		Remaining >>= 1;
	}
	const long long First = (a + b * l) % Modulus;
	const long long Sum = (First * Result.Sum + b * Result.Weighted) % Modulus;
	return Power(c, d) * Power(q, l) % Modulus * Sum % Modulus;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int m;
	std::cin >> m;
	while (m-- > 0)
	{
		long long l;
		long long r;
		long long a;
		long long b;
		long long c;
		long long d;
		std::cin >> l >> r >> a >> b >> c >> d;
		std::cout << Calculate(l, r, a, b, c, d) << '\n';
	}
}
