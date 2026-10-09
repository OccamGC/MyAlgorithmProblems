#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

// Nonnegative integers in base ten, least significant digit first.
class FInteger
{
public:
	std::vector<int> Digits;

	explicit FInteger(const std::string& Text = "0")
	{
		for (auto It = Text.rbegin(); It != Text.rend(); ++It)
		{
			Digits.push_back(*It - '0');
		}
		Trim();
	}

	void Trim()
	{
		while (!Digits.empty() && Digits.back() == 0)
		{
			Digits.pop_back();
		}
	}

	bool IsZero() const
	{
		return Digits.empty();
	}

	bool operator<(const FInteger& Other) const
	{
		if (Digits.size() != Other.Digits.size())
		{
			return Digits.size() < Other.Digits.size();
		}
		return std::lexicographical_compare(Digits.rbegin(), Digits.rend(), Other.Digits.rbegin(), Other.Digits.rend());
	}

	FInteger operator-(const FInteger& Other) const
	{
		FInteger Result = *this;
		int Borrow = 0;
		for (int i = 0; i < static_cast<int>(Digits.size()); ++i)
		{
			int Value = Digits[i] - Borrow - (i < static_cast<int>(Other.Digits.size()) ? Other.Digits[i] : 0);
			Borrow = Value < 0;
			Result.Digits[i] = Value + 10 * Borrow;
		}
		Result.Trim();
		return Result;
	}

	FInteger operator*(const FInteger& Other) const
	{
		FInteger Result;
		Result.Digits.resize(Digits.size() + Other.Digits.size() + 1);
		for (int i = 0; i < static_cast<int>(Digits.size()); ++i)
		{
			for (int j = 0; j < static_cast<int>(Other.Digits.size()); ++j)
			{
				Result.Digits[i + j] += Digits[i] * Other.Digits[j];
			}
		}
		for (int i = 0; i + 1 < static_cast<int>(Result.Digits.size()); ++i)
		{
			Result.Digits[i + 1] += Result.Digits[i] / 10;
			Result.Digits[i] %= 10;
		}
		Result.Trim();
		return Result;
	}

	std::pair<FInteger, FInteger> Divide(const FInteger& Divisor) const
	{
		FInteger Quotient;
		FInteger Remainder;
		Quotient.Digits.resize(Digits.size());
		for (int i = static_cast<int>(Digits.size()) - 1; i >= 0; --i)
		{
			Remainder.Digits.insert(Remainder.Digits.begin(), Digits[i]);
			Remainder.Trim();
			while (!(Remainder < Divisor))
			{
				Remainder = Remainder - Divisor;
				++Quotient.Digits[i];
			}
		}
		Quotient.Trim();
		return {Quotient, Remainder};
	}

	void Print() const
	{
		if (IsZero())
		{
			std::cout << '0';
		}
		for (auto It = Digits.rbegin(); It != Digits.rend(); ++It)
		{
			std::cout << *It;
		}
		std::cout << '\n';
	}
};

FInteger Gcd(FInteger a, FInteger b)
{
	while (!b.IsZero())
	{
		FInteger Remainder = a.Divide(b).second;
		a = std::move(b);
		b = std::move(Remainder);
	}
	return a;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	FInteger Answer("1");
	for (int i = 0; i < n; ++i)
	{
		std::string Prefix;
		std::string Period;
		std::cin >> Prefix >> Period;
		const int FractionLength = static_cast<int>(Prefix.size()) - 2;
		Prefix.erase(1, 1);
		const FInteger Numerator = FInteger(Prefix + Period) - FInteger(Prefix);
		FInteger Denominator(std::string(Period.size(), '9') + std::string(FractionLength, '0'));
		Denominator = Denominator.Divide(Gcd(Numerator, Denominator)).first;
		Answer = Answer.Divide(Gcd(Answer, Denominator)).first * Denominator;
	}
	Answer.Print();
}
