// Setter's neighbor-query idea; GPT-6: interactive protocol and endpoint implementation.
#include <cstdlib>
#include <iostream>
#include "solver.hpp"
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	if (!(std::cin >> n))
	{
		return 0;
	}
	auto Ask = [](const std::vector<int>& Query)
	{
		std::cout << "? " << Query.size();
		for (int Value : Query)
		{
			std::cout << ' ' << Value;
		}
		std::cout << std::endl;
		int Reply;
		if (!(std::cin >> Reply) || Reply < 0)
		{
			std::exit(0);
		}
		return Reply;
	};
	std::vector<int> Answer = RecoverPermutation(n, Ask);
	std::cout << '!';
	for (int Value : Answer)
	{
		std::cout << ' ' << Value;
	}
	std::cout << std::endl;
}
