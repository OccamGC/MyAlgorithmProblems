// Correct comparison witness: quotient DP + ordered enumeration + binary searches.
#define SWORDS_LIBRARY_ONLY
#include "../std.cpp"

std::vector<int> SolveSlowBinary(const std::vector<Swords::FSword>& Items,
	const std::vector<Swords::FInt>& Thresholds)
{
	using namespace Swords;
	if (UseDp(Items.size(), Thresholds))
	{
		return Solve(Items, Thresholds);
	}
	const FInt Cap = *std::max_element(Thresholds.begin(), Thresholds.end());
	const int Middle = static_cast<int>(Items.size()) / 2;
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	auto Left = BuildSorted(Odds, 0, Middle, Cap);
	MakePrefix(Left);
	auto Right = BuildSorted(Odds, Middle, static_cast<int>(Items.size()), Cap);
	int Prefix = 0;
	for (auto& State : Right)
	{
		Prefix += State.Probability;
		if (Prefix >= Mod)
		{
			Prefix -= Mod;
		}
		State.Probability = Prefix;
	}
	std::vector<int> Answers;
	for (FInt K : Thresholds)
	{
		if (K == 1)
		{
			Answers.push_back(1);
			continue;
		}
		FWeightedRuns Answer;
		for (const auto& State : Left)
		{
			if (State.Product >= K)
			{
				break;
			}
			const FInt Limit = (K - 1) / State.Product;
			const auto Position = std::upper_bound(Right.begin(), Right.end(), Limit,
				[](FInt Value, const FState& Candidate)
				{
					return Value < Candidate.Product;
				});
			Answer.Append(State.Probability, Position == Right.begin() ? 0 : (Position - 1)->Probability);
		}
		Answers.push_back((1 - static_cast<FInt>(Answer.Get()) * Scale % Mod + Mod) % Mod);
	}
	return Answers;
}

int main()
{
	return Swords::Run(SolveSlowBinary);
}
