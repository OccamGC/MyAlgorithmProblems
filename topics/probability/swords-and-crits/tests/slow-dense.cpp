// Correct comparison witness: dense product DP below the maximum small threshold.
// Uses odds, descending updates, zero skips, and reuses one distribution for all queries.
#define SWORDS_LIBRARY_ONLY
#include "../std.cpp"

std::vector<int> SolveDense(const std::vector<Swords::FSword>& Items,
	const std::vector<Swords::FInt>& Thresholds)
{
	using namespace Swords;
	const FInt Cap = *std::max_element(Thresholds.begin(), Thresholds.end());
	if (Cap > 20000000)
	{
		return Solve(Items, Thresholds);
	}
	if (Cap == 1)
	{
		return std::vector<int>(Thresholds.size(), 1);
	}
	int Scale;
	const auto Odds = PrepareOdds(Items, Scale);
	std::vector<int> Weights(Cap, 0);
	Weights[1] = 1;
	for (const auto& Item : Odds)
	{
		for (FInt Value = (Cap - 1) / Item.Multiplier; Value > 0; --Value)
		{
			if (Weights[Value] != 0)
			{
				const FInt Next = Value * Item.Multiplier;
				Weights[Next] = (Weights[Next] + static_cast<FInt>(Weights[Value]) * Item.Probability) % Mod;
			}
		}
	}
	for (FInt Value = 1; Value < Cap; ++Value)
	{
		Weights[Value] += Weights[Value - 1];
		if (Weights[Value] >= Mod)
		{
			Weights[Value] -= Mod;
		}
	}
	std::vector<int> Answers;
	for (FInt K : Thresholds)
	{
		const int Failure = static_cast<FInt>(Scale) * Weights[K - 1] % Mod;
		Answers.push_back((1 - Failure + Mod) % Mod);
	}
	return Answers;
}

int main()
{
	return Swords::Run(SolveDense);
}
