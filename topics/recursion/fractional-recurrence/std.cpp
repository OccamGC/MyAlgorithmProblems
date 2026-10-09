// Problem setter's solution: memoize recursive values below a cutoff.
// Codex (GPT-6): exact integer-root verification, smaller-input allocation and explicit base case.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using FWide = std::array<std::uint32_t, 4>;

FWide IntegerPower(int Base, int Exponent)
{
	FWide Value{0, 0, 0, 1};
	for (int Step = 0; Step < Exponent; ++Step)
	{
		std::uint64_t Carry = 0;
		for (int i = 3; i >= 0; --i)
		{
			const std::uint64_t Product = static_cast<std::uint64_t>(Value[i]) * Base + Carry;
			Value[i] = static_cast<std::uint32_t>(Product);
			Carry = Product >> 32;
		}
	}
	return Value;
}

int IntegerRoot(int x)
{
	const FWide Target = IntegerPower(x, 4);
	constexpr int MaximumRoot = 16000000;
	const int Guess = static_cast<int>(std::min(std::pow(static_cast<double>(x), 0.8), static_cast<double>(MaximumRoot)));
	if (IntegerPower(Guess, 5) <= Target && Target < IntegerPower(Guess + 1, 5))
	{
		return Guess;
	}
	int Left = 0;
	int Right = std::min(x, MaximumRoot) + 1;
	while (Right - Left > 1)
	{
		const int Middle = Left + (Right - Left) / 2;
		if (IntegerPower(Middle, 5) <= Target)
		{
			Left = Middle;
		}
		else
		{
			Right = Middle;
		}
	}
	return Left;
}

class FEvaluator
{
private:
	std::vector<long long> Memo;

public:
	explicit FEvaluator(int MaximumInput)
		: Memo(std::min(10000000, MaximumInput + 1), -1)
	{
		Memo[0] = 0;
	}

	long long Evaluate(int x)
	{
		if (x < static_cast<int>(Memo.size()) && Memo[x] >= 0)
		{
			return Memo[x];
		}
		const int First = std::max(IntegerRoot(x) - 1, 0);
		const long long Answer = 3 * Evaluate(First) + 2 * Evaluate(x / 2) + x;
		if (x < static_cast<int>(Memo.size()))
		{
			Memo[x] = Answer;
		}
		return Answer;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	std::cin >> N;
	std::vector<int> Queries(N);
	int MaximumInput = 0;
	for (int& x : Queries)
	{
		std::cin >> x;
		MaximumInput = std::max(MaximumInput, x);
	}
	FEvaluator Evaluator(MaximumInput);
	for (int i = 0; i < N; ++i)
	{
		if (i > 0)
		{
			std::cout << ' ';
		}
		std::cout << Evaluator.Evaluate(Queries[i]);
	}
	std::cout << '\n';
}
