// Codex (GPT-6): forward batched averaging using a truncated matrix power.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>

using FInt = std::int64_t;
constexpr FInt Mod = 1000000007;
constexpr FInt Half = 500000004;

struct FFamily
{
	int People;
	int Money;
};

FInt Power(FInt Base, FInt Exponent)
{
	FInt Result = 1;
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

int main()
{
	int n;
	if (std::scanf("%d", &n) != 1)
	{
		return 0;
	}
	int k;
	int InitialMoney;
	std::scanf("%d%d", &k, &InitialMoney);
	std::vector<FFamily> Families;
	Families.reserve(n - 1);
	for (int i = 1; i < n; ++i)
	{
		FFamily Family;
		std::scanf("%d%d", &Family.People, &Family.Money);
		if (FInt(Family.Money) * k > FInt(InitialMoney) * Family.People)
		{
			Families.push_back(Family);
		}
	}
	std::sort(Families.begin(), Families.end(), [](const FFamily& A, const FFamily& B)
	{
		return FInt(A.Money) * B.People < FInt(B.Money) * A.People;
	});
	std::vector<FInt> Inverse(k + 1);
	Inverse[1] = 1;
	for (int i = 2; i <= k; ++i)
	{
		Inverse[i] = Mod - Mod / i * Inverse[Mod % i] % Mod;
	}
	std::vector<FInt> Values(k, InitialMoney * Inverse[k] % Mod);
	std::vector<FInt> Next(k);
	std::vector<FInt> Kernel(k);
	for (const FFamily& Family : Families)
	{
		FInt Mean = Family.Money * Power(Family.People, Mod - 2) % Mod;
		Kernel[0] = Power(Half, Family.People);
		for (int d = 1; d < k; ++d)
		{
			Kernel[d] = Kernel[d - 1] * (Family.People + d - 1) % Mod * Inverse[d] % Mod * Half % Mod;
		}
		for (int i = 0; i < k; ++i)
		{
			FInt Sum = Mean;
			for (int j = 0; j <= i; ++j)
			{
				Sum = (Sum + Kernel[i - j] * ((Values[j] - Mean + Mod) % Mod)) % Mod;
			}
			Next[i] = Sum;
		}
		Values.swap(Next);
	}
	FInt Answer = 0;
	for (FInt Value : Values)
	{
		Answer = (Answer + Value) % Mod;
	}
	std::printf("%lld\n", static_cast<long long>(Answer));
	return 0;
}
