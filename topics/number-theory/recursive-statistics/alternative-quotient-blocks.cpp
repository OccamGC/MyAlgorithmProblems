// Problem setter's solution: quotient blocks and incremental memoization.
// Codex (GPT-6): portable C++17 implementation and documented boundary cases.
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	constexpr long long Mod = 998244353;
	std::vector<int> Answer = {0, 1};
	int Q;
	std::cin >> Q;
	while (Q-- > 0)
	{
		int x;
		std::cin >> x;
		while (static_cast<int>(Answer.size()) <= x)
		{
			int n = static_cast<int>(Answer.size());
			long long Value = n;
			for (int l = 2; l <= n;)
			{
				int Quotient = n / l;
				int r = n / Quotient;
				Value = (Value + (r - l + 1LL) * Answer[Quotient]) % Mod;
				l = r + 1;
			}
			Answer.push_back(static_cast<int>(Value));
		}
		std::cout << (x <= 0 ? x : Answer[x]) << '\n';
	}
}
