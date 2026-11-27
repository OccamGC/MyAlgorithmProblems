// Suffix convolution. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <vector>

constexpr long long Modulus = 1004535809;

long long Normalize(long long Value)
{
	Value %= Modulus;
	return Value < 0 ? Value + Modulus : Value;
}

long long Power(long long Base, long long Exponent)
{
	Base = Normalize(Base);
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

void Transform(std::vector<long long>& Values, bool bInverse)
{
	int Length = static_cast<int>(Values.size());
	int Reversed = 0;
	for (int i = 1; i < Length; ++i)
	{
		int Bit = Length / 2;
		while (Reversed & Bit)
		{
			Reversed ^= Bit;
			Bit >>= 1;
		}
		Reversed ^= Bit;
		if (i < Reversed)
		{
			std::swap(Values[i], Values[Reversed]);
		}
	}
	for (int Width = 2; Width <= Length; Width *= 2)
	{
		long long Root = Power(3, (Modulus - 1) / Width);
		if (bInverse)
		{
			Root = Power(Root, Modulus - 2);
		}
		for (int Start = 0; Start < Length; Start += Width)
		{
			long long Factor = 1;
			for (int j = 0; j < Width / 2; ++j)
			{
				long long Left = Values[Start + j];
				long long Right = Values[Start + j + Width / 2] * Factor % Modulus;
				Values[Start + j] = (Left + Right) % Modulus;
				Values[Start + j + Width / 2] = Normalize(Left - Right);
				Factor = Factor * Root % Modulus;
			}
		}
	}
	if (bInverse)
	{
		long long InverseLength = Power(Length, Modulus - 2);
		for (long long& Value : Values)
		{
			Value = Value * InverseLength % Modulus;
		}
	}
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int k;
	int q;
	std::cin >> n >> m >> k >> q;
	std::vector<int> Supply(n);
	for (int& Value : Supply)
	{
		std::cin >> Value;
	}
	int Length = 1;
	while (Length < n + m)
	{
		Length *= 2;
	}
	std::vector<long long> Starts(Length);
	for (int i = 0; i < k; ++i)
	{
		int p;
		std::cin >> p;
		++Starts[p - 1];
	}
	std::vector<std::vector<int>> Stops(n);
	std::vector<int> Begins(n);
	for (int i = 0; i < q; ++i)
	{
		int l;
		int r;
		std::cin >> l >> r;
		++Begins[l - 1];
		if (r < n)
		{
			Stops[r].push_back(r - l + 1);
		}
	}
	std::vector<long long> Spectrum(Length);
	for (int i = 0; i < n; ++i)
	{
		if (Begins[i] == 0 && Stops[i].empty())
		{
			continue;
		}
		std::vector<long long> Weight(Length);
		Weight[0] = Begins[i];
		for (int Offset : Stops[i])
		{
			Weight[Offset] = Normalize(Weight[Offset] - 1);
		}
		std::vector<long long> Suffix(Length);
		std::copy(Supply.begin() + i, Supply.end(), Suffix.begin());
		Transform(Suffix, false);
		Transform(Weight, false);
		for (int j = 0; j < Length; ++j)
		{
			Spectrum[j] = (Spectrum[j] + Suffix[j] * Weight[j]) % Modulus;
		}
	}
	Transform(Starts, false);
	for (int j = 0; j < Length; ++j)
	{
		Spectrum[j] = Spectrum[j] * Starts[j] % Modulus;
	}
	Transform(Spectrum, true);
	for (int i = 0; i < m; ++i)
	{
		std::cout << Spectrum[i] << (i + 1 == m ? '\n' : ' ');
	}
}
