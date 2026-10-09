#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	constexpr int Mod = 1000000007;
	int n;
	int m;
	int LengthA;
	int LengthB;
	std::cin >> n >> m >> LengthA >> LengthB;
	const int Length = std::max(LengthA, LengthB);
	std::vector<int> a(Length);
	std::vector<int> b(Length);
	for (int i = Length - LengthA; i < Length; ++i)
	{
		std::cin >> a[i];
	}
	for (int i = Length - LengthB; i < Length; ++i)
	{
		std::cin >> b[i];
	}
	const int Bound = n - 1;
	const int States = 2 * Bound + 1;
	std::vector<std::array<int, 2>> Current(States);
	Current[Bound][1] = 1;
	for (int i = 0; i < Length; ++i)
	{
		std::vector<std::array<int, 2>> Next(States);
		for (int Difference = -Bound; Difference <= Bound; ++Difference)
		{
			for (int Tight = 0; Tight <= 1; ++Tight)
			{
				const int Count = Current[Difference + Bound][Tight];
				if (Count == 0)
				{
					continue;
				}
				const int Limit = Tight ? b[i] : n - 1;
				for (int Digit = 0; Digit <= Limit; ++Digit)
				{
					const int Updated = std::clamp(Difference * m + Digit - a[i], -Bound, Bound);
					const int NextTight = Tight && Digit == b[i];
					int& Target = Next[Updated + Bound][NextTight];
					Target += Count;
					if (Target >= Mod)
					{
						Target -= Mod;
					}
				}
			}
		}
		Current.swap(Next);
	}
	int Answer = 0;
	for (int Difference = 1; Difference <= Bound; ++Difference)
	{
		for (int Tight = 0; Tight <= 1; ++Tight)
		{
			Answer += Current[Difference + Bound][Tight];
			if (Answer >= Mod)
			{
				Answer -= Mod;
			}
		}
	}
	std::cout << Answer << '\n';
}
