// Direct convolution. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	constexpr int Modulus = 100000007;
	int n;
	std::cin >> n;
	std::vector<int> Ways(1, 1);
	for (int i = 1; i <= n; ++i)
	{
		int k;
		int v;
		std::cin >> k >> v;
		int Limit = std::min(k, v / i);
		std::vector<int> Next(Ways.size() + Limit, 0);
		for (int Old = 0; Old < static_cast<int>(Ways.size()); ++Old)
		{
			for (int Added = 0; Added <= Limit; ++Added)
			{
				int& Count = Next[Old + Added];
				Count += Ways[Old];
				if (Count >= Modulus)
				{
					Count -= Modulus;
				}
			}
		}
		Ways.swap(Next);
	}
	for (std::size_t i = 0; i < Ways.size(); ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Ways[i];
	}
	std::cout << '\n';
}
