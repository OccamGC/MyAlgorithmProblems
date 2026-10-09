// Problem setter's solution: move the larger label to its parent.
// Codex (GPT-6): C++17 formatting and 64-bit boundary validation.
#include <iostream>
#include <utility>

int Distance(unsigned long long a, unsigned long long b)
{
	int Answer = 0;
	while (a != b)
	{
		if (a < b)
		{
			std::swap(a, b);
		}
		a /= 2;
		++Answer;
	}
	return Answer;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int m;
	std::cin >> m;
	for (int i = 1; i <= m; ++i)
	{
		unsigned long long a;
		unsigned long long b;
		std::cin >> a >> b;
		std::cout << "Case #" << i << ": " << Distance(a, b) << '\n';
	}
}
