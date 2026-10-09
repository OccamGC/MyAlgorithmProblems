// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Problem setter's per-block transform variant: O(L log^2 L) time, O(L) space.
#include <array>
#include <iostream>
#include <vector>
#include "fwt.hpp"

int n;
std::vector<int> a;
std::vector<int> b;
std::array<int, 3> Answer{};

void Decompose(int Left, int Right, int Size)
{
	if (Left + Right > n)
	{
		return;
	}
	if (Left + Right + 2 * Size - 2 <= n)
	{
		for (int Operation = 0; Operation < 3; ++Operation)
		{
			std::vector<int> x(a.begin() + Left, a.begin() + Left + Size);
			std::vector<int> y(b.begin() + Right, b.begin() + Right + Size);
			for (int Half = 1; Half < Size; Half <<= 1)
			{
				Butterfly(x, Half, Operation, false);
				Butterfly(y, Half, Operation, false);
			}
			for (int i = 0; i < Size; ++i)
			{
				x[i] = static_cast<std::int64_t>(x[i]) * y[i] % Modulus;
			}
			for (int Half = 1; Half < Size; Half <<= 1)
			{
				Butterfly(x, Half, Operation, true);
			}
			int Base = Offset(Left, Right, Operation);
			for (int i = 0; i < Size; ++i)
			{
				Answer[(Base + i) % 3] = Add(Answer[(Base + i) % 3], x[i]);
			}
		}
		return;
	}
	int Half = Size / 2;
	Decompose(Left, Right, Half);
	Decompose(Left + Half, Right, Half);
	Decompose(Left, Right + Half, Half);
	Decompose(Left + Half, Right + Half, Half);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cin >> n;
	int Length = 1;
	while (Length <= n)
	{
		Length <<= 1;
	}
	a.resize(Length);
	b.resize(Length);
	for (int i = 0; i <= n; ++i)
	{
		std::cin >> a[i];
	}
	for (int i = 0; i <= n; ++i)
	{
		std::cin >> b[i];
	}
	Decompose(0, 0, Length);
	for (int Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
