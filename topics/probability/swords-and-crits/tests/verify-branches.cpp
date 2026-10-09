// Force both algorithms on small inputs, independent of the automatic choice.
#define SWORDS_LIBRARY_ONLY
#include "../std.cpp"
#include <stdexcept>

std::vector<int> Verify(const std::vector<Swords::FSword>& Items,
	const std::vector<Swords::FInt>& Thresholds)
{
	using namespace Swords;
	const auto Answers = Solve(Items, Thresholds);
	for (std::size_t j = 0; j < Thresholds.size(); ++j)
	{
		const FInt K = Thresholds[j];
		if (SolveMitm(Items, K) != Answers[j])
		{
			throw std::runtime_error("forced meet-in-the-middle mismatch");
		}
		if (K <= 1000000 && SolveDp(Items, K) != Answers[j])
		{
			throw std::runtime_error("forced quotient DP mismatch");
		}
	}
	return Answers;
}

int main()
{
	return Swords::Run(Verify);
}
