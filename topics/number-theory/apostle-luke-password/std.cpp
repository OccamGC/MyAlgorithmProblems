// Problem setter's solution: simplify the factorial expression and use Miller-Rabin.
// Codex (GPT-6): preserve the p = 1 term, define p = 0, and use exact portable modular multiplication.
#include <cstdint>
#include <iostream>

using FUnsigned = std::uint64_t;

FUnsigned Multiply(FUnsigned Left, FUnsigned Right, FUnsigned Mod)
{
	FUnsigned Result = 0;
	while (Right > 0)
	{
		if (Right & 1)
		{
			Result += Left;
			if (Result >= Mod)
			{
				Result -= Mod;
			}
		}
		Left += Left;
		if (Left >= Mod)
		{
			Left -= Mod;
		}
		Right >>= 1;
	}
	return Result;
}

FUnsigned Power(FUnsigned Base, FUnsigned Exponent, FUnsigned Mod)
{
	FUnsigned Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Multiply(Result, Base, Mod);
		}
		Base = Multiply(Base, Base, Mod);
		Exponent >>= 1;
	}
	return Result;
}

bool IsPrime(FUnsigned Value)
{
	if (Value < 2)
	{
		return false;
	}
	constexpr int Bases[] = {2, 3, 5, 7, 11, 13, 17, 19, 23};
	for (int Base : Bases)
	{
		if (Value % Base == 0)
		{
			return Value == static_cast<FUnsigned>(Base);
		}
	}
	FUnsigned Odd = Value - 1;
	int Twos = 0;
	while ((Odd & 1) == 0)
	{
		Odd >>= 1;
		++Twos;
	}
	for (int Base : Bases)
	{
		FUnsigned Residue = Power(Base, Odd, Value);
		if (Residue == 1 || Residue == Value - 1)
		{
			continue;
		}
		bool bPassed = false;
		for (int i = 1; i < Twos; ++i)
		{
			Residue = Multiply(Residue, Residue, Value);
			if (Residue == Value - 1)
			{
				bPassed = true;
				break;
			}
		}
		if (!bPassed)
		{
			return false;
		}
	}
	return true;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	FUnsigned G;
	FUnsigned k;
	FUnsigned b;
	std::cin >> N >> G >> k >> b;
	int Answer = 0;
	FUnsigned p = k * G + b;
	for (int i = 0; i < N; ++i)
	{
		Answer += p == 1 || IsPrime(p);
		std::cout << Answer << '\n';
		p += k;
	}
}
