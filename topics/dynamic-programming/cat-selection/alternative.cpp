// Problem setter's subset search and feasibility pruning from the teaching notes.
// Codex (GPT-6): precomputed powers, explicit base cases and portable long long.
#include <algorithm>
#include <iostream>
#include <limits>
#include <vector>

class FSearch
{
public:
	int n;
	int k;
	std::vector<long long> Values;
	std::vector<long long> Power;
	long long Answer = std::numeric_limits<long long>::lowest();

	void Visit(int Position, int Chosen, long long Score)
	{
		if (Chosen == k)
		{
			Answer = std::max(Answer, Score);
			return;
		}
		if (n - Position < k - Chosen)
		{
			return;
		}
		Visit(Position + 1, Chosen + 1, Score + Values[Position] * Power[k - Chosen - 1]);
		Visit(Position + 1, Chosen, Score);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	FSearch Search;
	std::cin >> Search.n >> Search.k;
	Search.Values.resize(Search.n);
	for (auto& Value : Search.Values)
	{
		std::cin >> Value;
	}
	Search.Power.assign(Search.k + 1, 1);
	for (int i = 1; i <= Search.k; ++i)
	{
		Search.Power[i] = Search.Power[i - 1] * 3;
	}
	Search.Visit(0, 0, 0);
	std::cout << Search.Answer << '\n';
}
