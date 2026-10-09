// Setter method: skip factorial-size lexicographic blocks using descending suffixes.
// Codex (GPT-6): formal cyclic semantics, portable style, dynamic storage, and independent verification.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <vector>
using Integer = long long;
void Advance(std::vector<int>& a, Integer& Remaining, const std::array<Integer, 13>& Factorial)
{
	int n = static_cast<int>(a.size()) - 1;
	int i;
	for (i = n - 1; i >= 1 && Remaining; --i)
	{
		if (a[i] >= a[i + 1])
		{
			continue;
		}
		int j = i + 1;
		while (j < n && a[j + 1] > a[i])
		{
			++j;
		}
		if (n - i <= 12 && (j - i) * Factorial[n - i] <= Remaining)
		{
			Remaining -= (j - i) * Factorial[n - i];
			for (int Position = i; Position < j; ++Position)
			{
				std::swap(a[Position], a[Position + 1]);
			}
		}
		else
		{
			--Remaining;
			int Steps = 0;
			if (n - i <= 12)
			{
				Steps = static_cast<int>(Remaining / Factorial[n - i]);
				Remaining %= Factorial[n - i];
			}
			int Position = n - (j - Steps - i - 1);
			std::reverse(a.begin() + i + 1, a.end());
			std::swap(a[i], a[Position]);
			while (Position > i + 1 && a[Position - 1] > a[Position])
			{
				std::swap(a[Position], a[Position - 1]);
				--Position;
			}
			break;
		}
	}
	if (i && Remaining)
	{
		i = std::max(i + 1, n - 12);
		for (; i < n && Remaining; ++i)
		{
			int Steps = static_cast<int>(Remaining / Factorial[n - i]);
			if (Steps == 0)
			{
				continue;
			}
			Remaining %= Factorial[n - i];
			int Position = i + Steps;
			std::swap(a[i], a[Position]);
			while (Position > i + 1 && a[Position - 1] > a[Position])
			{
				std::swap(a[Position], a[Position - 1]);
				--Position;
			}
		}
	}
}
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::array<Integer, 13> Factorial{};
	Factorial[0] = 1;
	for (int i = 1; i <= 12; ++i)
	{
		Factorial[i] = Factorial[i - 1] * i;
	}
	int T;
	std::cin >> T;
	while (T--)
	{
		int n;
		Integer k;
		std::cin >> n >> k;
		std::vector<int> a(n + 1);
		for (int i = 1; i <= n; ++i)
		{
			std::cin >> a[i];
		}
		if (n <= 12)
		{
			k %= Factorial[n];
		}
		if (k)
		{
			Advance(a, k, Factorial);
		}
		if (k)
		{
			--k;
			std::iota(a.begin(), a.end(), 0);
			if (k)
			{
				Advance(a, k, Factorial);
			}
		}
		for (int i = 1; i <= n; ++i)
		{
			std::cout << a[i] << (i == n ? '\n' : ' ');
		}
	}
}
