// Problem setter's solution supplies the symmetry-count formula.
// Codex (GPT-6): two-level fixed-base power table for constant-time queries.

#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Modulus = 1000000007;

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Modulus;
		}
		Base = Base * Base % Modulus;
		Exponent >>= 1;
	}
	return Result;
}

class FPowerTable
{
private:
	static constexpr int BlockSize = 32768;
	static constexpr int MaximumExponent = 1999999999;
	std::array<int, BlockSize> Low{};
	std::array<int, MaximumExponent / BlockSize + 1> High{};

public:
	FPowerTable()
	{
		Low[0] = 1;
		for (int i = 1; i < BlockSize; ++i)
		{
			Low[i] = 2LL * Low[i - 1] % Modulus;
		}
		const long long Step = 2LL * Low[BlockSize - 1] % Modulus;
		High[0] = 1;
		for (int i = 1; i < static_cast<int>(High.size()); ++i)
		{
			High[i] = High[i - 1] * Step % Modulus;
		}
	}

	long long Get(int Exponent) const
	{
		return static_cast<long long>(High[Exponent / BlockSize]) * Low[Exponent % BlockSize] % Modulus;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	const FPowerTable Powers;
	int m;
	std::cin >> m;
	long long Answer = 0;
	while (m-- > 0)
	{
		long long n;
		std::cin >> n;
		long long Count;
		if (n & 1)
		{
			Count = Powers.Get(static_cast<int>(2 * n - 1));
		}
		else
		{
			const long long Half = Powers.Get(static_cast<int>(n - 1));
			Count = Half * (2 * Half + 1) % Modulus;
		}
		Answer ^= Count;
	}
	std::cout << Answer << '\n';
}
