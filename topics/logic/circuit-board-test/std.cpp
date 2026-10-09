// Problem setter's exact interval simplification; C++17 organization by Codex (GPT-6).
#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		long long x;
		std::cin >> x;
		bool Accepted = 4 <= x && x <= 14;
		std::cout << (Accepted ? "T\n" : "F\n");
	}
}
