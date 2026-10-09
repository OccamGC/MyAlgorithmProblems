#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

// Exact signed arithmetic for this problem's bounds, using only C++17 types.
// Value = High * Base + Low, with 0 <= Low < Base.
struct FWide
{
	static constexpr long long Base = 1000000000;
	long long High = 0;
	long long Low = 0;

	FWide(long long Value = 0)
		: High(Value / Base), Low(Value % Base)
	{
		Normalize();
	}

	void Normalize()
	{
		High += Low / Base;
		Low %= Base;
		if (Low < 0)
		{
			Low += Base;
			--High;
		}
	}

	FWide Times(long long Factor) const
	{
		FWide Result;
		long long Product = Low * (Factor % Base);
		Result.High = High * Factor + Low * (Factor / Base) + Product / Base;
		Result.Low = Product % Base;
		return Result;
	}

	FWide operator+(const FWide& Other) const
	{
		FWide Result;
		Result.High = High + Other.High;
		Result.Low = Low + Other.Low;
		Result.Normalize();
		return Result;
	}

	FWide operator-(const FWide& Other) const
	{
		FWide Result;
		Result.High = High - Other.High;
		Result.Low = Low - Other.Low;
		Result.Normalize();
		return Result;
	}

	bool operator<(const FWide& Other) const
	{
		return High != Other.High ? High < Other.High : Low < Other.Low;
	}
};

struct FUnitType
{
	long long Shots;
	long long Attack;
	long long Count = 0;
};

FWide DamageAfter(const FUnitType& Unit, long long OtherAttack, long long Killed)
{
	long long WeightedRounds = Unit.Shots * Killed * (2 * Unit.Count - Killed + 1) / 2;
	return FWide(OtherAttack).Times(Unit.Shots * Killed)
		+ FWide(Unit.Attack).Times(WeightedRounds - Killed);
}

// For a concave sequence whose first forward difference is FirstDifference
// and whose forward differences decrease by Step, find an integer maximum.
long long PeakIndex(long long FirstDifference, long long Step, long long Upper)
{
	if (FirstDifference <= 0)
	{
		return 0;
	}
	return std::min(Upper, (FirstDifference - 1) / Step + 1);
}

FWide PeakDamage(const FUnitType& Unit, long long OtherAttack)
{
	long long Step = Unit.Shots * Unit.Attack;
	long long First = Unit.Shots * (OtherAttack + Unit.Attack * Unit.Count) - Unit.Attack;
	long long k = PeakIndex(First, Step, Unit.Count);
	FWide Peak = std::max(FWide(0), DamageAfter(Unit, OtherAttack, k));
	if (Unit.Shots > 1)
	{
		First = Unit.Shots * (OtherAttack + Unit.Attack * (Unit.Count - 1));
		k = PeakIndex(First, Step, Unit.Count - 1);
		FWide BeforeKill = DamageAfter(Unit, OtherAttack, k)
			+ FWide(OtherAttack + Unit.Attack * (Unit.Count - k)).Times(Unit.Shots - 1);
		Peak = std::max(Peak, BeforeKill);
	}
	return Peak;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int Kinds;
	int Num;
	long long InitialHealth;
	long long BorisAttack;
	long long HealthBonus;
	std::cin >> Kinds >> Num >> InitialHealth >> BorisAttack >> HealthBonus;
	std::vector<FUnitType> Types(Kinds);
	std::unordered_map<std::string, int> Index;
	for (int i = 0; i < Kinds; ++i)
	{
		std::string Name;
		long long Health;
		std::cin >> Name >> Health >> Types[i].Attack;
		Types[i].Shots = (Health + BorisAttack - 1) / BorisAttack;
		Index.emplace(Name, i);
	}
	for (int i = 0; i < Num; ++i)
	{
		std::string Name;
		std::cin >> Name;
		++Types[Index.at(Name)].Count;
	}
	std::vector<FUnitType> Hostile;
	std::vector<FUnitType> Harmless;
	long long Healing = 0;
	for (const auto& Unit : Types)
	{
		if (Unit.Count == 0)
		{
			continue;
		}
		if (Unit.Attack > 0)
		{
			Hostile.push_back(Unit);
		}
		else
		{
			Harmless.push_back(Unit);
			Healing -= Unit.Attack * Unit.Count;
		}
	}
	int PositiveKinds = static_cast<int>(Hostile.size());
	int States = 1 << PositiveKinds;
	std::vector<long long> AttackSum(States, -Healing);
	for (int i = 0; i < PositiveKinds; ++i)
	{
		for (int Mask = 0; Mask < (1 << i); ++Mask)
		{
			AttackSum[Mask | (1 << i)] = AttackSum[Mask] + Hostile[i].Attack * Hostile[i].Count;
		}
	}
	std::vector<FWide> dp(States, FWide(-1));
	dp[States - 1] = FWide(InitialHealth + HealthBonus);
	for (int i = 0; i < PositiveKinds; ++i)
	{
		dp[(States - 1) ^ (1 << i)] = FWide(InitialHealth);
	}
	for (int Mask = States - 1; Mask > 0; --Mask)
	{
		if (!(FWide(0) < dp[Mask]))
		{
			continue;
		}
		for (int i = 0; i < PositiveKinds; ++i)
		{
			if ((Mask & (1 << i)) == 0)
			{
				continue;
			}
			const auto& Unit = Hostile[i];
			long long OtherAttack = AttackSum[Mask] - Unit.Attack * Unit.Count;
			if (PeakDamage(Unit, OtherAttack) < dp[Mask])
			{
				int Next = Mask ^ (1 << i);
				dp[Next] = std::max(dp[Next], dp[Mask] - DamageAfter(Unit, OtherAttack, Unit.Count));
			}
		}
	}
	if (!(FWide(0) < dp[0]))
	{
		std::cout << "leave!\n";
		return 0;
	}
	FWide Answer = dp[0];
	for (const auto& Unit : Harmless)
	{
		Answer = Answer + FWide(Healing).Times(Unit.Count * (Unit.Shots - 1));
	}
	std::sort(Harmless.begin(), Harmless.end(), [](const auto& Left, const auto& Right)
	{
		return Left.Attack > Right.Attack;
	});
	for (const auto& Unit : Harmless)
	{
		long long Rate = -Unit.Attack;
		Healing -= Rate * Unit.Count;
		Answer = Answer + FWide(Healing).Times(Unit.Count)
			+ FWide(Rate).Times(Unit.Count * (Unit.Count - 1) / 2);
	}
	if (Answer.High == 0)
	{
		std::cout << Answer.Low << '\n';
	}
	else
	{
		std::cout << Answer.High << std::setw(9) << std::setfill('0') << Answer.Low << '\n';
	}
}
