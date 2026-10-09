// Codex (GPT-6): evaluate a proven optimal moving schedule by affine powers.
// Shares the optimal schedule proof, but does not use the final wealth formula.
#include <algorithm>
#include <cstdint>
#include <iostream>

using Int64 = std::int64_t;
constexpr Int64 Mod = 1000000007;

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

Int64 Transfer(Int64 Money, Int64 TotalMoney, Int64 From, Int64 To, Int64 Population)
{
	if (From == To)
	{
		return Money;
	}
	if (To < From)
	{
		return Money * To % Mod * Power(From, Mod - 2) % Mod;
	}
	const Int64 Outside = (TotalMoney - Money + Mod) % Mod
		* (Population - To) % Mod * Power(Population - From, Mod - 2) % Mod;
	return (TotalMoney - Outside + Mod) % Mod;
}

Int64 Solve(Int64 k, Int64 m1, Int64 l, Int64 m2)
{
	if (l == 0 || m1 * l >= m2 * k)
	{
		return m1 % Mod;
	}
	const Int64 Population = k + l;
	const Int64 h = Population / 2;
	const Int64 TotalMoney = (m1 + m2) % Mod;
	Int64 Money = Transfer(m1, TotalMoney, k, h, Population);
	const Int64 Retained = h * Power(h + 1, Mod - 2) % Mod;
	const Int64 Incoming = Power(Population - h, Mod - 2);
	Int64 Alpha = Retained * (1 - Incoming + Mod) % Mod;
	Int64 Beta = Retained * Incoming % Mod * TotalMoney % Mod;
	Int64 Repetitions = std::min(k, l);
	while (Repetitions > 0)
	{
		if (Repetitions & 1)
		{
			Money = (Alpha * Money + Beta) % Mod;
		}
		Beta = (Alpha * Beta + Beta) % Mod;
		Alpha = Alpha * Alpha % Mod;
		Repetitions >>= 1;
	}
	Money = Transfer(Money, TotalMoney, h, l, Population);
	return (TotalMoney - Money + Mod) % Mod;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int TestCount;
	std::cin >> TestCount;
	while (TestCount--)
	{
		Int64 k, m1, l, m2;
		std::cin >> k >> m1 >> l >> m2;
		std::cout << Solve(k, m1, l, m2) << '\n';
	}
}
