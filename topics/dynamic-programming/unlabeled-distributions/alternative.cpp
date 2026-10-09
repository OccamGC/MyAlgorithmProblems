// Codex (GPT-6): apply Euler's pentagonal recurrence, then remove oversized parts.

#include <algorithm>
#include <iostream>
#include <vector>

constexpr int Modulus = 1000000007;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Counts(n + 1, 0);
	Counts[0] = 1;
	for (int Total = 1; Total <= n; ++Total)
	{
		long long Value = 0;
		for (int k = 1; k * (3 * k - 1) / 2 <= Total; ++k)
		{
			const int First = k * (3 * k - 1) / 2;
			const int Second = k * (3 * k + 1) / 2;
			const int Sign = k % 2 == 1 ? 1 : -1;
			Value += Sign * Counts[Total - First];
			if (Second <= Total)
			{
				Value += Sign * Counts[Total - Second];
			}
		}
		Counts[Total] = static_cast<int>((Value % Modulus + Modulus) % Modulus);
	}
	for (int Part = m + 1; Part <= n; ++Part)
	{
		for (int Total = n; Total >= Part; --Total)
		{
			Counts[Total] -= Counts[Total - Part];
			if (Counts[Total] < 0)
			{
				Counts[Total] += Modulus;
			}
		}
	}
	for (int i = 1; i <= n; ++i)
	{
		std::cout << Counts[i] << '\n';
	}
}
