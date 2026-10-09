// Codex (GPT-6): closed-form optimum for two fixed household slots.
// Optimize exact rational wealth before taking the residue.
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

Int64 Solve(Int64 k, Int64 m1, Int64 l, Int64 m2)
{
	if (l == 0 || m1 * l >= m2 * k)
	{
		return m1 % Mod;
	}
	const Int64 Total = k + l;
	const Int64 Half = Total / 2;
	const Int64 Denominator = Total % 2 == 0
		? Half * (Half + 1) : (Half + 1) * (Half + 1);
	const Int64 r = std::min(k, l);
	const Int64 InverseTotal = Power(Total, Mod - 2);
	const Int64 Ratio = (Denominator - Total) % Mod
		* Power(Denominator % Mod, Mod - 2) % Mod;
	const Int64 Gap = (m2 * k - m1 * l) % Mod
		* Power(k, Mod - 2) % Mod * Power(l, Mod - 2) % Mod;
	const Int64 Bonus = r * r % Mod * InverseTotal % Mod
		* Gap % Mod * Power(Ratio, r) % Mod;
	return (k * ((m1 + m2) % Mod) % Mod * InverseTotal + Bonus) % Mod;
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
