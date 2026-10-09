// Codex (GPT-6): aggregate at most three exact richer per-person wealth levels.
#ifndef EDIT_TOWN_WEALTH_HPP
#define EDIT_TOWN_WEALTH_HPP

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

using Int64 = std::int64_t;
constexpr Int64 Mod = 1000000007;
constexpr Int64 Half = (Mod + 1) / 2;

struct WealthGroup
{
	int People;
	int Money;
	Int64 Count;
};

struct Town
{
	int Targets;
	int InitialMoney;
	std::vector<WealthGroup> Groups;
};

inline Int64 Power(Int64 Base, Int64 Exponent)
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

inline Town ReadTown()
{
	int n;
	Town Input;
	std::cin >> n >> Input.Targets >> Input.InitialMoney;
	for (int i = 1; i < n; ++i)
	{
		int People, Money;
		std::cin >> People >> Money;
		if (People == 0 || static_cast<Int64>(Money) * Input.Targets
			<= static_cast<Int64>(Input.InitialMoney) * People)
		{
			continue;
		}
		bool Found = false;
		for (WealthGroup& Group : Input.Groups)
		{
			if (static_cast<Int64>(Money) * Group.People
				== static_cast<Int64>(Group.Money) * People)
			{
				Group.Count += People;
				Found = true;
				break;
			}
		}
		if (!Found)
		{
			Input.Groups.push_back({People, Money, People});
		}
	}
	std::sort(Input.Groups.begin(), Input.Groups.end(), [](const WealthGroup& A, const WealthGroup& B)
	{
		return static_cast<Int64>(A.Money) * B.People > static_cast<Int64>(B.Money) * A.People;
	});
	return Input;
}

inline std::vector<Int64> SmallInverses(int Count)
{
	std::vector<Int64> Inverse(Count + 1);
	Inverse[1] = 1;
	for (int i = 2; i <= Count; ++i)
	{
		Inverse[i] = Mod - Mod / i * Inverse[Mod % i] % Mod;
	}
	return Inverse;
}

#endif
