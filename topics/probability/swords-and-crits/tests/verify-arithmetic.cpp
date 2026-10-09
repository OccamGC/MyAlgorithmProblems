// Check signed 64-bit boundary operations against an independent Python oracle.
#define SWORDS_LIBRARY_ONLY
#include "../std.cpp"

int main()
{
	using namespace Swords;
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int Count;
	std::cin >> Count;
	while (Count-- > 0)
	{
		int Type;
		FInt a;
		std::cin >> Type >> a;
		if (Type == 3)
		{
			std::cout << IntegerSqrt(a) << '\n';
			continue;
		}
		FInt b;
		std::cin >> b;
		if (Type == 2)
		{
			std::cout << (a - 1) / b + 1 << '\n';
			continue;
		}
		FInt K;
		std::cin >> K;
		if (Type == 0)
		{
			std::cout << (a > (K - 1) / b ? K : a * b) << '\n';
		}
		else
		{
			std::cout << (a > (K - 1) / b) << '\n';
		}
	}
	FAccumulator Accumulator;
	for (int i = 0; i < 100000; ++i)
	{
		Accumulator.AddProduct(Mod - 1, Mod - 1);
	}
	std::cout << Accumulator.Get() << '\n';
}
