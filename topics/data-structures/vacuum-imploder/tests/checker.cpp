// Usage: checker <input> <reference-output> <contestant-output>; exit 0 accepts.
#include <cmath>
#include <fstream>
#include <string>

int main(int argc, char* argv[])
{
	if (argc != 4)
	{
		return 2;
	}
	std::ifstream Input(argv[1]);
	std::ifstream Reference(argv[2]);
	std::ifstream Contestant(argv[3]);
	int n;
	int m;
	if (!(Input >> n >> m) || !Reference || !Contestant)
	{
		return 2;
	}
	long long Value;
	for (int i = 0; i < 2 * n; ++i)
	{
		if (!(Input >> Value))
		{
			return 2;
		}
	}
	int Rows = n;
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		if (!(Input >> Operation) || Operation < 0 || Operation > 7)
		{
			return 2;
		}
		int Arguments = Operation == 7 ? 1 : (Operation <= 1 || Operation == 6 ? 3 : 2);
		Rows += Operation == 7;
		for (int j = 0; j < Arguments; ++j)
		{
			if (!(Input >> Value))
			{
				return 2;
			}
		}
	}
	constexpr long double Tolerance = 0.050001L;
	for (int i = 0; i < 2 * Rows; ++i)
	{
		long double Expected;
		long double Actual;
		if (!(Reference >> Expected) || !std::isfinite(Expected))
		{
			return 2;
		}
		if (!(Contestant >> Actual) || !std::isfinite(Actual) || std::abs(Expected - Actual) > Tolerance)
		{
			return 1;
		}
	}
	std::string Extra;
	if (Reference >> Extra)
	{
		return 2;
	}
	if (Contestant >> Extra)
	{
		return 1;
	}
	return 0;
}
