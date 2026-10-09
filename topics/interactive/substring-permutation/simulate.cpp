// GPT-6: offline harness for the same solver. Not an interactive submission.
#include <iostream>
#include <stdexcept>
#include "solver.hpp"
int main()
{
	int n;
	std::cin >> n;
	std::vector<int> Hidden(n);
	std::vector<int> Position(n + 1);
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Hidden[i];
		Position[Hidden[i]] = i;
	}
	int Queries = 0;
	auto Ask = [&](const std::vector<int>& Query)
	{
		if (++Queries > 800 || Query.empty() || Query.size() > 100)
		{
			throw std::runtime_error("query limit");
		}
		int Previous = -2;
		int Run = 0;
		int Best = 0;
		for (int Value : Query)
		{
			if (Value < 1 || Value > n)
			{
				throw std::runtime_error("invalid value");
			}
			int Current = Position[Value];
			Run = Current == Previous + 1 ? Run + 1 : 1;
			Best = std::max(Best, Run);
			Previous = Current;
		}
		return Best;
	};
	std::vector<int> Answer = RecoverPermutation(n, Ask);
	if (Answer != Hidden)
	{
		throw std::runtime_error("incorrect reconstruction");
	}
	for (int i = 0; i < n; ++i)
	{
		std::cout << Answer[i] << (i + 1 == n ? '\n' : ' ');
	}
	std::cout << Queries << '\n';
}
