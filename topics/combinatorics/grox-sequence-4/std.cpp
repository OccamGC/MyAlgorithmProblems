// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Phased block transforms: O(L log L) time and O(L log L) space.
#include <array>
#include <iostream>
#include <utility>
#include <vector>
#include "fwt.hpp"

int n;
std::vector<std::vector<std::pair<int, int>>> Missions;

void Decompose(int a, int b, int Bit)
{
	int Size = 1 << Bit;
	if (a + b > n)
	{
		return;
	}
	if (a + b + 2 * Size - 2 <= n)
	{
		Missions[Bit].emplace_back(a, b);
		return;
	}
	int Half = Size / 2;
	Decompose(a, b, Bit - 1);
	Decompose(a + Half, b, Bit - 1);
	Decompose(a, b + Half, Bit - 1);
	Decompose(a + Half, b + Half, Bit - 1);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cin >> n;
	int Length = 1;
	int Bits = 0;
	while (Length <= n)
	{
		Length <<= 1;
		++Bits;
	}
	std::vector<int> a(Length);
	std::vector<int> b(Length);
	for (int i = 0; i <= n; ++i)
	{
		std::cin >> a[i];
	}
	for (int i = 0; i <= n; ++i)
	{
		std::cin >> b[i];
	}
	Missions.resize(Bits + 1);
	Decompose(0, 0, Bits);
	std::array<int, 3> Answer{};
	for (int Operation = 0; Operation < 3; ++Operation)
	{
		std::vector<int> Left = a;
		std::vector<int> Right = b;
		std::vector<std::vector<int>> Result(Bits + 1, std::vector<int>(Length));
		for (int Bit = 0; Bit <= Bits; ++Bit)
		{
			if (Bit > 0)
			{
				Butterfly(Left, 1 << (Bit - 1), Operation, false);
				Butterfly(Right, 1 << (Bit - 1), Operation, false);
			}
			for (const auto& Mission : Missions[Bit])
			{
				int Base = Offset(Mission.first, Mission.second, Operation);
				for (int j = 0; j < (1 << Bit); ++j)
				{
					int Value = static_cast<std::int64_t>(Left[Mission.first + j]) * Right[Mission.second + j] % Modulus;
					Result[Bit][Base + j] = Add(Result[Bit][Base + j], Value);
				}
			}
		}
		for (int Bit = Bits; Bit > 0; --Bit)
		{
			Butterfly(Result[Bit], 1 << (Bit - 1), Operation, true);
			for (int i = 0; i < Length; ++i)
			{
				Result[Bit - 1][i] = Add(Result[Bit - 1][i], Result[Bit][i]);
			}
		}
		for (int i = 0; i <= n; ++i)
		{
			Answer[i % 3] = Add(Answer[i % 3], Result[0][i]);
		}
	}
	for (int Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
