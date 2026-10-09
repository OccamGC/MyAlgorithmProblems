#pragma once
#include <cstdint>
#include <vector>

constexpr int Modulus = 1004535809;

inline int Add(int Left, int Right)
{
	int Result = Left + Right;
	return Result >= Modulus ? Result - Modulus : Result;
}

inline int Subtract(int Left, int Right)
{
	int Result = Left - Right;
	return Result < 0 ? Result + Modulus : Result;
}

inline void Butterfly(std::vector<int>& Values, int Half, int Operation, bool bInverse)
{
	for (int Start = 0; Start < static_cast<int>(Values.size()); Start += 2 * Half)
	{
		for (int j = 0; j < Half; ++j)
		{
			int& Left = Values[Start + j];
			int& Right = Values[Start + j + Half];
			if (Operation == 0)
			{
				int Sum = Add(Left, Right);
				int Difference = Subtract(Left, Right);
				if (bInverse)
				{
					Sum = static_cast<std::int64_t>(Sum) * ((Modulus + 1) / 2) % Modulus;
					Difference = static_cast<std::int64_t>(Difference) * ((Modulus + 1) / 2) % Modulus;
				}
				Left = Sum;
				Right = Difference;
			}
			else if (Operation == 1)
			{
				Right = bInverse ? Subtract(Right, Left) : Add(Right, Left);
			}
			else
			{
				Left = bInverse ? Subtract(Left, Right) : Add(Left, Right);
			}
		}
	}
}

inline int Offset(int Left, int Right, int Operation)
{
	if (Operation == 0)
	{
		return Left ^ Right;
	}
	return Operation == 1 ? Left | Right : Left & Right;
}
