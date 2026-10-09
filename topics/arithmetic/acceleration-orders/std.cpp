// Problem setter's formula d = |a*t*t|/2.
// Codex (GPT-6): equivalent integer representation and portable output.
#include <cstdlib>
#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		long long a;
		long long t;
		std::cin >> a >> t;
		long long TwiceDistance = std::abs(a) * t * t;
		std::cout << TwiceDistance / 2 << (TwiceDistance % 2 == 0 ? ".0\n" : ".5\n");
	}
}
