#pragma once
#include <algorithm>
#include <cstdint>
#include <vector>

using FInteger = std::int64_t;

inline FInteger Power(FInteger Base, FInteger Exponent, FInteger Modulus)
{
	FInteger Result = 1;
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

inline void Transform(std::vector<FInteger>& Values, bool bInverse, FInteger Modulus, FInteger Root)
{
	int Length = static_cast<int>(Values.size());
	int j = 0;
	for (int i = 1; i < Length; ++i)
	{
		int Bit = Length >> 1;
		while (j & Bit)
		{
			j ^= Bit;
			Bit >>= 1;
		}
		j ^= Bit;
		if (i < j)
		{
			std::swap(Values[i], Values[j]);
		}
	}
	for (int Block = 2; Block <= Length; Block <<= 1)
	{
		FInteger Step = Power(Root, (Modulus - 1) / Block, Modulus);
		if (bInverse)
		{
			Step = Power(Step, Modulus - 2, Modulus);
		}
		for (int Start = 0; Start < Length; Start += Block)
		{
			FInteger Factor = 1;
			for (int j = 0; j < Block / 2; ++j)
			{
				FInteger Left = Values[Start + j];
				FInteger Right = Values[Start + j + Block / 2] * Factor % Modulus;
				Values[Start + j] = (Left + Right) % Modulus;
				Values[Start + j + Block / 2] = (Left - Right + Modulus) % Modulus;
				Factor = Factor * Step % Modulus;
			}
		}
	}
	if (bInverse)
	{
		FInteger Inverse = Power(Length, Modulus - 2, Modulus);
		for (FInteger& Value : Values)
		{
			Value = Value * Inverse % Modulus;
		}
	}
}
