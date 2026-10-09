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
		int Window = 0;
		for (int j = 0; j < static_cast<int>(Next.size()); ++j)
		{
			if (j < static_cast<int>(Ways.size()))
			{
				Window += Ways[j];
				if (Window >= Modulus)
				{
					Window -= Modulus;
				}
			}
			if (j > Limit && j - Limit - 1 < static_cast<int>(Ways.size()))
			{
				Window -= Ways[j - Limit - 1];
				if (Window < 0)
				{
					Window += Modulus;
				}
			}
			Next[j] = Window;
		}
		Ways.swap(Next);
	}
	for (std::size_t i = 0; i < Ways.size(); ++i)
	{
		std::cout << (i == 0 ? "" : " ") << Ways[i];
	}
	std::cout << '\n';
}
