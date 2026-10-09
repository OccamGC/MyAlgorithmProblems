// Codex (GPT-6): apply the reverse-complement orbit count with modulus 2P.
// Exact halving avoids assuming that two has an inverse modulo P.

#include <iostream>

long long Power(long long Base, long long Exponent, long long Modulus)
{
	Base %= Modulus;
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

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int M;
	std::cin >> M;
	long long Answer = 0;
	while (M-- > 0)
	{
		long long N;
		long long K;
		long long P;
		std::cin >> N >> K >> P;
		const long long TwiceModulus = 2 * P;
		long long Numerator;
		if (N & 1)
		{
			Numerator = Power(2 * K, N, TwiceModulus);
		}
		else
		{
			const long long Half = Power(2 * K, N / 2, TwiceModulus);
			Numerator = (Half * Half + Half) % TwiceModulus;
		}
		Answer ^= Numerator / 2;
	}
	std::cout << Answer << '\n';
}
