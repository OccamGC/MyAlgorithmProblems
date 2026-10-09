// Codex (GPT-6): optimal averaging proof, batched tail coefficients, and implementation.
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

FInt Tail(FInt PeopleBefore, int Targets, FInt Power, const std::vector<FInt>& Inverse)
{
	FInt Choose = 1;
	FInt HalfPower = 1;
	FInt Sum = Targets;
	for (int J = 1; J < Targets; ++J)
	{
		Choose = Choose * ((PeopleBefore + J - 1) % Mod) % Mod * Inverse[J] % Mod;
		HalfPower = HalfPower * Half % Mod;
		Sum = (Sum + (Targets - J) * Choose % Mod * HalfPower) % Mod;
	}
	return Sum * Power % Mod;
}

int main()
{
	int N;
	if (std::scanf("%d", &N) != 1)
	{
		return 0;
	}
	int K;
	int InitialMoney;
	std::scanf("%d%d", &K, &InitialMoney);
	int MaxPeople = K;
	std::vector<FFamily> Families;
	Families.reserve(N - 1);
	for (int I = 1; I < N; ++I)
	{
		FFamily Family;
		std::scanf("%d%d", &Family.People, &Family.Money);
		MaxPeople = std::max(MaxPeople, Family.People);
		if (FInt(Family.Money) * K > FInt(InitialMoney) * Family.People)
		{
			Families.push_back(Family);
		}
	}
	std::sort(Families.begin(), Families.end(), [](const FFamily& A, const FFamily& B)
	{
		return FInt(A.Money) * B.People > FInt(B.Money) * A.People;
	});
	std::vector<FInt> Inverse(MaxPeople + 1);
	std::vector<FInt> Powers(MaxPeople + 1);
	Inverse[1] = 1;
	Powers[0] = 1;
	for (int I = 1; I <= MaxPeople; ++I)
	{
		if (I > 1)
		{
			Inverse[I] = Mod - Mod / I * Inverse[Mod % I] % Mod;
		}
		Powers[I] = Powers[I - 1] * Half % Mod;
	}
	FInt InitialMean = InitialMoney * Inverse[K] % Mod;
	FInt Answer = InitialMoney;
	FInt PeopleBefore = 0;
	FInt Power = 1;
	FInt PreviousTail = K;
	for (const FFamily& Family : Families)
	{
		PeopleBefore += Family.People;
		Power = Power * Powers[Family.People] % Mod;
		FInt CurrentTail = Tail(PeopleBefore, K, Power, Inverse);
		FInt Weight = (PreviousTail - CurrentTail + Mod) % Mod;
		FInt Difference = (Family.Money * Inverse[Family.People] % Mod - InitialMean + Mod) % Mod;
		Answer = (Answer + Difference * Weight) % Mod;
		PreviousTail = CurrentTail;
	}
	std::printf("%lld\n", static_cast<long long>(Answer));
	return 0;
}
