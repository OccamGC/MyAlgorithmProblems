// Codex (GPT-6): forward convolution for each aggregated wealth level.
#include "wealth.hpp"

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	const Town Input = ReadTown();
	const int k = Input.Targets;
	const std::vector<Int64> Inverse = SmallInverses(k);
	std::vector<Int64> Values(k, Input.InitialMoney * Inverse[k] % Mod);
	std::vector<Int64> Next(k);
	std::vector<Int64> Kernel(k);
	for (auto It = Input.Groups.rbegin(); It != Input.Groups.rend(); ++It)
	{
		const WealthGroup& Group = *It;
		const Int64 Mean = Group.Money * Power(Group.People, Mod - 2) % Mod;
		Kernel[0] = Power(Half, Group.Count);
		for (int d = 1; d < k; ++d)
		{
			Kernel[d] = Kernel[d - 1] * ((Group.Count + d - 1) % Mod)
				% Mod * Inverse[d] % Mod * Half % Mod;
		}
		for (int i = 0; i < k; ++i)
		{
			Int64 Sum = Mean;
			for (int j = 0; j <= i; ++j)
			{
				Sum = (Sum + Kernel[i - j] * ((Values[j] - Mean + Mod) % Mod)) % Mod;
			}
			Next[i] = Sum;
		}
		Values.swap(Next);
	}
	Int64 Answer = 0;
	for (Int64 Value : Values)
	{
		Answer = (Answer + Value) % Mod;
	}
	std::cout << Answer << '\n';
}
