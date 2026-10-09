// Problem setter's solution, developed with Codex (GPT-6).
// Applies quotient-state DP and sorted meet-in-the-middle enumeration.

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

namespace Swords
{
using FInt = std::int64_t;
constexpr int Mod = 998244353;
constexpr int ProbabilityScale = 1000000;

int Power(int Base, int Exponent)
{
	int Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = static_cast<FInt>(Result) * Base % Mod;
		}
		Base = static_cast<FInt>(Base) * Base % Mod;
		Exponent >>= 1;
	}
	return Result;
}

struct FSword
{
	FInt Multiplier;
	int Probability;
};

struct FState
{
	FInt Product;
	int Probability;
};

FInt IntegerSqrt(FInt Value)
{
	FInt Root = 0;
	for (FInt Bit = FInt{1} << 31; Bit > 0; Bit >>= 1)
	{
		const FInt Candidate = Root + Bit;
		if (Candidate <= Value / Candidate)
		{
			Root = Candidate;
		}
	}
	return Root;
}

int SolveDp(const std::vector<FSword>& Items, FInt K)
{
	if (K == 1)
	{
		return 1;
	}
	if (Items.empty())
	{
		return 0;
	}
	const FInt T = K - 1;
	const FInt Root = IntegerSqrt(T);
	const FInt LargeCount = T / (Root + 1);
	std::vector<FInt> Threshold(Root + LargeCount + 1);
	for (FInt t = 0; t <= Root; ++t)
	{
		Threshold[t] = t;
	}
	for (FInt d = 1; d <= LargeCount; ++d)
	{
		Threshold[Root + LargeCount - d + 1] = T / d;
	}
	std::vector<int> Probability(Threshold.size(), 1);
	Probability[0] = 0;
	for (const FSword& Item : Items)
	{
		const int p = Item.Probability;
		const int q = (1 - p + Mod) % Mod;
		for (std::size_t Index = Threshold.size() - 1; Index > 0; --Index)
		{
			const FInt Next = Threshold[Index] / Item.Multiplier;
			const FInt NextIndex = Next <= Root ? Next : Root + LargeCount - T / Next + 1;
			Probability[Index] = (static_cast<FInt>(q) * Probability[Index]
				+ static_cast<FInt>(p) * Probability[NextIndex]) % Mod;
		}
	}
	return (1 - Probability.back() + Mod) % Mod;
}

// Each extension merges two already sorted lists in linear time.
// Products at least Cap cannot contribute to any failure event.
std::vector<FState> BuildSorted(const std::vector<FSword>& Items, int Begin, int End, FInt Cap)
{
	std::vector<FState> States = {{1, 1}};
	for (int i = Begin; i < End; ++i)
	{
		const FInt m = Items[i].Multiplier;
		const FInt SafeLimit = (Cap - 1) / m;
		const int p = Items[i].Probability;
		const std::size_t TriggerCount = std::upper_bound(States.begin(), States.end(), SafeLimit,
			[](FInt Value, const FState& State)
			{
				return Value < State.Product;
			}) - States.begin();
		std::vector<FState> Next;
		Next.reserve(States.size() + TriggerCount);
		std::size_t Left = 0;
		std::size_t Right = 0;
		FInt Triggered = TriggerCount == 0 ? Cap : States[0].Product * m;
		while (Left < States.size() || Right < TriggerCount)
		{
			if (Right == TriggerCount || (Left < States.size() && States[Left].Product <= Triggered))
			{
				Next.push_back(States[Left++]);
			}
			else
			{
				Next.push_back({Triggered,
					static_cast<int>(static_cast<FInt>(States[Right].Probability) * p % Mod)});
				++Right;
				if (Right < TriggerCount)
				{
					Triggered = States[Right].Product * m;
				}
			}
		}
		States.swap(Next);
	}
	return States;
}

// Eight products of residues and a reduced carry fit in signed int64_t.
class FAccumulator
{
	FInt Sum = 0;
	int Count = 0;
public:
	void AddProduct(int a, int b)
	{
		Sum += static_cast<FInt>(a) * b;
		if (++Count == 8)
		{
			Sum %= Mod;
			Count = 0;
		}
	}
	int Get() const
	{
		return static_cast<int>(Sum % Mod);
	}
};

int TotalWeight(const std::vector<FState>& States)
{
	int Total = 0;
	for (const FState& State : States)
	{
		Total += State.Probability;
		if (Total >= Mod)
		{
			Total -= Mod;
		}
	}
	return Total;
}

void MakePrefix(std::vector<FState>& States)
{
	int Total = 0;
	for (FState& State : States)
	{
		Total += State.Probability;
		if (Total >= Mod)
		{
			Total -= Mod;
		}
		State.Probability = Total;
	}
}

// Settle a block of left weights only when its matching right prefix changes.
class FWeightedRuns
{
	FAccumulator Answer;
	int GroupBegin = 0;
	int LeftPrefix = 0;
	int RightPrefix = 0;
	void Flush()
	{
		int Weight = LeftPrefix - GroupBegin;
		if (Weight < 0)
		{
			Weight += Mod;
		}
		Answer.AddProduct(Weight, RightPrefix);
		GroupBegin = LeftPrefix;
	}
public:
	void Append(int Left, int Right)
	{
		if (Right != RightPrefix)
		{
			Flush();
			RightPrefix = Right;
		}
		LeftPrefix = Left;
	}
	int Get()
	{
		Flush();
		return Answer.Get();
	}
};

int JoinLinear(const std::vector<FState>& Left, const std::vector<FState>& Right, FInt K)
{
	std::size_t Position = Right.size();
	FWeightedRuns Answer;
	for (const FState& State : Left)
	{
		if (State.Product >= K)
		{
			break;
		}
		const FInt Limit = (K - 1) / State.Product;
		while (Position > 0 && Right[Position - 1].Product > Limit)
		{
			--Position;
		}
		Answer.Append(State.Probability, Position == 0 ? 0 : Right[Position - 1].Probability);
	}
	return Answer.Get();
}

std::vector<FSword> PrepareOdds(const std::vector<FSword>& Items, int& Scale)
{
	std::vector<FSword> Odds = Items;
	Scale = 1;
	for (FSword& Item : Odds)
	{
		const int Failure = (1 - Item.Probability + Mod) % Mod;
		Scale = static_cast<FInt>(Scale) * Failure % Mod;
		Item.Probability = static_cast<FInt>(Item.Probability) * Power(Failure, Mod - 2) % Mod;
	}
	return Odds;
}

int SolveMitm(const std::vector<FSword>& Items, FInt K)
{
	if (K == 1)
	{
		return 1;
	}
	const int Middle = static_cast<int>(Items.size()) / 2;
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	auto Left = BuildSorted(Odds, 0, Middle, K);
	MakePrefix(Left);
	auto Right = BuildSorted(Odds, Middle, static_cast<int>(Items.size()), K);
	MakePrefix(Right);
	return (1 - static_cast<FInt>(JoinLinear(Left, Right, K)) * Scale % Mod + Mod) % Mod;
}

bool UseDp(std::size_t n, const std::vector<FInt>& Thresholds)
{
	if (n > 44)
	{
		return true;
	}
	FInt DpWork = 0;
	for (FInt K : Thresholds)
	{
		DpWork += n * (2 * IntegerSqrt(K - 1) + 1);
	}
	const FInt MitmWork = (Thresholds.size() + 4) * (FInt{1} << ((n + 1) / 2));
	return DpWork <= MitmWork;
}

std::vector<int> Solve(const std::vector<FSword>& Items, const std::vector<FInt>& Thresholds)
{
	std::vector<int> Answers;
	if (UseDp(Items.size(), Thresholds))
	{
		for (FInt K : Thresholds)
		{
			Answers.push_back(SolveDp(Items, K));
		}
		return Answers;
	}
	const FInt Cap = *std::max_element(Thresholds.begin(), Thresholds.end());
	const int Middle = static_cast<int>(Items.size()) / 2;
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	auto Left = BuildSorted(Odds, 0, Middle, Cap);
	MakePrefix(Left);
	auto Right = BuildSorted(Odds, Middle, static_cast<int>(Items.size()), Cap);
	MakePrefix(Right);
	for (FInt K : Thresholds)
	{
		Answers.push_back(K == 1 ? 1 : (1 - static_cast<FInt>(JoinLinear(Left, Right, K)) * Scale % Mod + Mod) % Mod);
	}
	return Answers;
}

template <typename FSolver>
int Run(FSolver Solver)
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	const int InverseScale = Power(ProbabilityScale, Mod - 2);
	int TestCount;
	std::cin >> TestCount;
	while (TestCount-- > 0)
	{
		int n;
		int q;
		std::cin >> n >> q;
		std::vector<FSword> Items;
		std::vector<FInt> Certain;
		for (int i = 0; i < n; ++i)
		{
			FSword Item;
			int p;
			std::cin >> p >> Item.Multiplier;
			if (p == 0 || Item.Multiplier == 1)
			{
				continue;
			}
			if (p == ProbabilityScale)
			{
				Certain.push_back(Item.Multiplier);
				continue;
			}
			Item.Probability = static_cast<FInt>(p) * InverseScale % Mod;
			Items.push_back(Item);
		}
		std::vector<FInt> Thresholds(q);
		for (FInt& K : Thresholds)
		{
			std::cin >> K;
			for (FInt m : Certain)
			{
				K = (K - 1) / m + 1;
			}
		}
		if (Items.empty())
		{
			for (FInt K : Thresholds)
			{
				std::cout << (K == 1 ? 1 : 0) << '\n';
			}
			continue;
		}
		const auto Answers = Solver(Items, Thresholds);
		for (int Answer : Answers)
		{
			std::cout << Answer << '\n';
		}
	}
	return 0;
}
}

#ifndef SWORDS_LIBRARY_ONLY
int main()
{
	return Swords::Run(Swords::Solve);
}
#endif
