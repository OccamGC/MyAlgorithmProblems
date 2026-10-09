// Codex (GPT-6): remove dominated empty/fern cells, then enumerate
// tulip masks and the four remaining plant choices exactly.
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>

class FGarden
{
public:
	int n;
	int m;
	int A;
	std::vector<long double> Effects;
	long double Best = 0;
	void Search(int At, long double Wheat, long double Corn, long double Bloom,
		long double Glove, long double Penalty)
	{
		if (At == static_cast<int>(Effects.size()))
		{
			long double Milk = 0.04L * A * 1.05L * 1.05L * 1.1L * 0.002L * Bloom;
			long double Kitty = 1 + 0.05L * Milk;
			const long double Coefficient[] = {0.1L, 0.125L, 0.15L, 0.175L};
			for (long double c : Coefficient)
			{
				long double Factor = 1 + c * Milk;
				Kitty *= Factor * Factor;
			}
			Kitty *= 1 + 0.115L * Milk;
			long double Factor = 1 + 0.2L * Milk;
			Kitty *= Factor * Factor * Factor * Factor * Factor;
			long double Value = (1 + 0.00044L * Glove) * Kitty * (1 + 0.01L * Wheat)
				* Penalty * (0.02L * Corn + 0.04L * Glove);
			Best = std::max(Best, Value);
			return;
		}
		long double f = Effects[At];
		Search(At + 1, Wheat + f, Corn, Bloom, Glove, Penalty);
		Search(At + 1, Wheat, Corn + f, Bloom, Glove, Penalty);
		Search(At + 1, Wheat, Corn, Bloom + f, Glove, Penalty);
		Search(At + 1, Wheat, Corn, Bloom, Glove + f, Penalty * (1 - 0.01L * f));
	}
	void Solve()
	{
		int Cells = n * m;
		for (long double Soil : {1.0L, 1.25L})
		{
			for (int Mask = 0; Mask < (1 << Cells); ++Mask)
			{
				Effects.clear();
				for (int i = 0; i < Cells; ++i)
				{
					if ((Mask >> i) & 1)
					{
						continue;
					}
					int Neighbors = 0;
					for (int j = 0; j < Cells; ++j)
					{
						if (((Mask >> j) & 1) && std::abs(i / m - j / m) <= 1
							&& std::abs(i % m - j % m) <= 1)
						{
							++Neighbors;
						}
					}
					Effects.push_back(Soil * (1 + 0.2L * Neighbors * Soil));
				}
				Search(0, 0, 0, 0, 0, 1);
			}
		}
		std::printf("%.18Le\n", Best);
	}
};
int main()
{
	FGarden Garden;
	if (std::scanf("%d%d%d", &Garden.n, &Garden.m, &Garden.A) != 3)
	{
		return 0;
	}
	Garden.Solve();
}
