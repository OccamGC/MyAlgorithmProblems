// Codex (GPT-6): sorted averaging, seven exact statistics, and backward
// integer threshold comparison for p_1 = 1 and initial p_i <= 20.
#include <algorithm>
#include <cstdio>
#include <vector>

constexpr long long Mod = 1000000007;
constexpr long long Half = (Mod + 1) / 2;
struct FFamily
{
	int People;
	int Money;
};
int main()
{
	int n;
	std::scanf("%d", &n);
	std::vector<FFamily> Families(n);
	long long TotalMoney = 0;
	long long Others = -1;
	int MaxPeople = 1;
	for (FFamily& f : Families)
	{
		std::scanf("%d%d", &f.People, &f.Money);
		TotalMoney += f.Money;
		Others += f.People;
		MaxPeople = std::max(MaxPeople, f.People);
	}
	long long Initial = Families[0].Money;
	if (Others == 0)
	{
		std::printf("%lld\n0\n0\n1\n1\n1\n1\n", Initial);
		return 0;
	}
	std::vector<long long> Inverse(MaxPeople + 1);
	std::vector<long long> Power(MaxPeople + 1);
	Inverse[1] = 1;
	Power[0] = 1;
	for (int i = 1; i <= MaxPeople; ++i)
	{
		if (i > 1)
		{
			Inverse[i] = Mod - (Mod / i) * Inverse[Mod % i] % Mod;
		}
		Power[i] = Power[i - 1] * Half % Mod;
	}
	std::sort(Families.begin() + 1, Families.end(), [](FFamily a, FFamily b)
	{
		return 1LL * a.Money * b.People < 1LL * b.Money * a.People;
	});
	FFamily Minimum = Families[1];
	long long Least = Minimum.Money * Inverse[Minimum.People] % Mod;
	bool bAllRicher = Minimum.Money > Initial * Minimum.People;
	if (bAllRicher)
	{
		Least = (Initial + Least) * Half % Mod;
	}
	bool bHasRicher = false;
	long long Answer = Initial;
	for (int i = 1; i < n; ++i)
	{
		FFamily f = Families[i];
		if (f.Money <= Initial * f.People)
		{
			continue;
		}
		bHasRicher = true;
		long long Value = f.Money * Inverse[f.People] % Mod;
		Answer = (Value + (Answer - Value + Mod) * Power[f.People]) % Mod;
	}
	long long Gap;
	if (bHasRicher)
	{
		// 2*lcm(1,...,20): all input means and the minimum final mean
		// are integral in this scale. Reverse the affine updates exactly.
		constexpr long long Scale = 465585120;
		long long InitialScaled = Initial * Scale;
		long long LeastScaled = 1LL * Minimum.Money * Scale / Minimum.People;
		if (bAllRicher)
		{
			LeastScaled = (InitialScaled + LeastScaled) / 2;
		}
		long long Threshold = 2 * LeastScaled;
		bool bAtLeastTwice = false;
		for (int i = n - 1; i >= 1; --i)
		{
			if (Threshold <= InitialScaled)
			{
				bAtLeastTwice = true;
				break;
			}
			FFamily f = Families[i];
			if (f.Money <= Initial * f.People)
			{
				continue;
			}
			long long Value = 1LL * f.Money * Scale / f.People;
			if (Threshold >= Value)
			{
				break;
			}
			long long Factor = 1LL << f.People;
			long long Difference = Value - Threshold;
			if (Difference > (Value - InitialScaled) / Factor)
			{
				bAtLeastTwice = true;
				break;
			}
			Threshold = Value - Factor * Difference;
			bAtLeastTwice = Threshold <= InitialScaled;
		}
		long long Deduction = bAtLeastTwice ? 2 * Least : Answer;
		Gap = Others == 1 ? 0 : (TotalMoney % Mod - Answer - Deduction) % Mod;
	}
	else
	{
		long long Outside = TotalMoney - Initial;
		long long Numerator = Initial * Minimum.People - Minimum.Money;
		if (Others >= 2)
		{
			Numerator = std::max(Numerator, Outside * Minimum.People - 2LL * Minimum.Money);
			Numerator = std::max(Numerator, (Outside - Initial) * Minimum.People);
		}
		Gap = Numerator % Mod * Inverse[Minimum.People] % Mod;
	}
	Gap = (Gap + Mod) % Mod;
	long long PerCapitaGap = (Answer - Least + Mod) % Mod;
	bool bStrict = bHasRicher ? Others >= 2 : Minimum.Money < Initial * Minimum.People;
	std::printf("%lld\n%lld\n%lld\n1\n%d\n1\n%d\n", Answer, Gap, PerCapitaGap, bStrict, bStrict);
}
