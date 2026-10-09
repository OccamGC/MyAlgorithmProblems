// Codex (GPT-6): grouped tail coefficients after freeing enough fixed slots.
#include "wealth.hpp"

Int64 Tail(Int64 PeopleBefore, int k, Int64 HalfPower, const std::vector<Int64>& Inverse)
{
	Int64 Choose = 1;
	Int64 RowPower = 1;
	Int64 Sum = k;
	for (int j = 1; j < k; ++j)
	{
		Choose = Choose * ((PeopleBefore + j - 1) % Mod) % Mod * Inverse[j] % Mod;
		RowPower = RowPower * Half % Mod;
		Sum = (Sum + (k - j) * Choose % Mod * RowPower) % Mod;
	}
	return Sum * HalfPower % Mod;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	const Town Input = ReadTown();
	const int k = Input.Targets;
	const std::vector<Int64> Inverse = SmallInverses(k);
	const Int64 InitialMean = Input.InitialMoney * Inverse[k] % Mod;
	Int64 Answer = Input.InitialMoney;
	Int64 PeopleBefore = 0;
	Int64 HalfPower = 1;
	Int64 PreviousTail = k;
	for (const WealthGroup& Group : Input.Groups)
	{
		PeopleBefore += Group.Count;
		HalfPower = HalfPower * Power(Half, Group.Count) % Mod;
		const Int64 CurrentTail = Tail(PeopleBefore, k, HalfPower, Inverse);
		const Int64 Weight = (PreviousTail - CurrentTail + Mod) % Mod;
		const Int64 Mean = Group.Money * Power(Group.People, Mod - 2) % Mod;
		Answer = (Answer + (Mean - InitialMean + Mod) * Weight) % Mod;
		PreviousTail = CurrentTail;
	}
	std::cout << Answer << '\n';
}
