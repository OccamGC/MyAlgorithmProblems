#pragma once
#include <algorithm>
#include <vector>
#include "ntt.hpp"

// Standard Newton iteration and polynomial arithmetic, implemented by Codex (GPT-6).
template<FInteger Modulus, FInteger Root>
struct FPolynomialArithmetic
{
	using FSeries = std::vector<FInteger>;

	static void Trim(FSeries& Values)
	{
		while (Values.size() > 1 && Values.back() == 0)
		{
			Values.pop_back();
		}
	}

	static FSeries Multiply(const FSeries& Left, const FSeries& Right, int Limit)
	{
		int LeftSize = std::min(static_cast<int>(Left.size()), Limit);
		int RightSize = std::min(static_cast<int>(Right.size()), Limit);
		int Size = std::min(LeftSize + RightSize - 1, Limit);
		if (std::min(LeftSize, RightSize) <= 16)
		{
			FSeries Result(Size);
			for (int i = 0; i < LeftSize; ++i)
			{
				for (int j = 0; j < RightSize && i + j < Size; ++j)
				{
					Result[i + j] = (Result[i + j] + Left[i] * Right[j]) % Modulus;
				}
			}
			return Result;
		}
		int Length = 1;
		while (Length < LeftSize + RightSize - 1)
		{
			Length <<= 1;
		}
		FSeries a(Length);
		FSeries b(Length);
		for (int i = 0; i < LeftSize; ++i)
		{
			a[i] = Left[i];
		}
		for (int i = 0; i < RightSize; ++i)
		{
			b[i] = Right[i];
		}
		Transform(a, false, Modulus, Root);
		Transform(b, false, Modulus, Root);
		for (int i = 0; i < Length; ++i)
		{
			a[i] = a[i] * b[i] % Modulus;
		}
		Transform(a, true, Modulus, Root);
		a.resize(Size);
		return a;
	}

	static FSeries Inverse(const FSeries& Values, int Length)
	{
		FSeries Result{Power(Values[0], Modulus - 2, Modulus)};
		while (static_cast<int>(Result.size()) < Length)
		{
			int Next = std::min(2 * static_cast<int>(Result.size()), Length);
			FSeries Correction = Multiply(Values, Result, Next);
			Correction.resize(Next);
			for (FInteger& Value : Correction)
			{
				Value = (Modulus - Value) % Modulus;
			}
			Correction[0] = (Correction[0] + 2) % Modulus;
			Result = Multiply(Result, Correction, Next);
			Result.resize(Next);
		}
		return Result;
	}

	static FSeries Logarithm(const FSeries& Values, int Length)
	{
		if (Length == 1)
		{
			return FSeries{0};
		}
		FSeries Derivative(std::max(1, static_cast<int>(Values.size()) - 1));
		for (int i = 1; i < static_cast<int>(Values.size()); ++i)
		{
			Derivative[i - 1] = i * Values[i] % Modulus;
		}
		FSeries Product = Multiply(Derivative, Inverse(Values, Length), Length - 1);
		Product.resize(Length - 1);
		FSeries Inverses(Length, 1);
		for (int i = 2; i < Length; ++i)
		{
			Inverses[i] = Modulus - (Modulus / i) * Inverses[Modulus % i] % Modulus;
		}
		FSeries Result(Length);
		for (int i = 1; i < Length; ++i)
		{
			Result[i] = Product[i - 1] * Inverses[i] % Modulus;
		}
		return Result;
	}

	static FSeries Exponential(const FSeries& Values, int Length)
	{
		FSeries Result{1};
		while (static_cast<int>(Result.size()) < Length)
		{
			int Next = std::min(2 * static_cast<int>(Result.size()), Length);
			FSeries Correction = Logarithm(Result, Next);
			for (int i = 0; i < Next; ++i)
			{
				FInteger Target = i < static_cast<int>(Values.size()) ? Values[i] : 0;
				Correction[i] = (Target - Correction[i] + Modulus) % Modulus;
			}
			Correction[0] = (Correction[0] + 1) % Modulus;
			Result = Multiply(Result, Correction, Next);
			Result.resize(Next);
		}
		return Result;
	}

	// The divisor is monic; polynomial product-tree nodes satisfy this requirement.
	static FSeries Remainder(FSeries Values, const FSeries& Divisor)
	{
		Trim(Values);
		if (Values.size() < Divisor.size())
		{
			return Values;
		}
		int Degree = static_cast<int>(Divisor.size()) - 1;
		int QuotientLength = static_cast<int>(Values.size()) - Degree;
		if (Degree <= 32 || QuotientLength <= 16)
		{
			for (int i = static_cast<int>(Values.size()) - 1; i >= Degree; --i)
			{
				FInteger Factor = Values[i];
				for (int j = 0; j <= Degree; ++j)
				{
					Values[i - Degree + j] = (Values[i - Degree + j]
						- Factor * Divisor[j] % Modulus + Modulus) % Modulus;
				}
			}
		}
		else
		{
			FSeries ReversedValues(Values.rbegin(), Values.rend());
			FSeries ReversedDivisor(Divisor.rbegin(), Divisor.rend());
			FSeries Quotient = Multiply(ReversedValues,
				Inverse(ReversedDivisor, QuotientLength), QuotientLength);
			Quotient.resize(QuotientLength);
			std::reverse(Quotient.begin(), Quotient.end());
			FSeries Product = Multiply(Quotient, Divisor, static_cast<int>(Values.size()));
			for (int i = 0; i < Degree; ++i)
			{
				Values[i] = (Values[i] - Product[i] + Modulus) % Modulus;
			}
		}
		Values.resize(std::max(1, Degree));
		Trim(Values);
		return Values;
	}
};
