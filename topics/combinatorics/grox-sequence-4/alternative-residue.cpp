// Codex (GPT-6): residue-valued tensor transforms applied to the setter's block decomposition.
// O(L (1 + log L)) time and O(L) space; no full convolution or inverse transform.
#include <array>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

constexpr int Modulus = 1004535809;
using FResidues = std::array<int, 3>;

int Add(int Left, int Right)
{
	int Sum = Left + Right;
	return Sum >= Modulus ? Sum - Modulus : Sum;
}

void Decompose(int a, int b, int Size, int Bit, int n,
	std::vector<std::vector<std::pair<int, int>>>& Blocks)
{
	if (a + b > n)
	{
		return;
	}
	if (a + b + 2 * Size - 2 <= n)
	{
		Blocks[Bit].emplace_back(a, b);
		return;
	}
	int Half = Size / 2;
	Decompose(a, b, Half, Bit - 1, n, Blocks);
	Decompose(a + Half, b, Half, Bit - 1, n, Blocks);
	Decompose(a, b + Half, Half, Bit - 1, n, Blocks);
	Decompose(a + Half, b + Half, Half, Bit - 1, n, Blocks);
}

void Advance(std::vector<FResidues>& Values, int Half, int Operation)
{
	int Shift = Half % 3;
	for (int Start = 0; Start < static_cast<int>(Values.size()); Start += 2 * Half)
	{
		for (int i = 0; i < Half; ++i)
		{
			FResidues Left = Values[Start + i];
			FResidues Right = Values[Start + Half + i];
			for (int r = 0; r < 3; ++r)
			{
				int Previous = (r + 3 - Shift) % 3;
				if (Operation == 0) // XOR: [[1, z^Half], [z^Half, 1]].
				{
					Values[Start + i][r] = Add(Left[r], Right[Previous]);
					Values[Start + Half + i][r] = Add(Left[Previous], Right[r]);
				}
				else if (Operation == 1) // OR: [[1, z^Half], [z^Half, z^Half]].
				{
					Values[Start + i][r] = Add(Left[r], Right[Previous]);
					Values[Start + Half + i][r] = Add(Left[Previous], Right[Previous]);
				}
				else // AND: [[1, 1], [1, z^Half]].
				{
					Values[Start + i][r] = Add(Left[r], Right[r]);
					Values[Start + Half + i][r] = Add(Left[r], Right[Previous]);
				}
			}
		}
	}
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
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
	std::vector<std::vector<std::pair<int, int>>> Blocks(Bits + 1);
	Decompose(0, 0, Length, Bits, n, Blocks);
	FResidues Answer{};
	for (int Operation = 0; Operation < 3; ++Operation)
	{
		std::vector<FResidues> Values(Length);
		for (int i = 0; i < Length; ++i)
		{
			Values[i][0] = b[i];
		}
		for (int Bit = 0; Bit <= Bits; ++Bit)
		{
			if (Bit > 0)
			{
				Advance(Values, 1 << (Bit - 1), Operation);
			}
			for (const auto& Block : Blocks[Bit])
			{
				int Offset = Operation == 0 ? (Block.first ^ Block.second)
					: Operation == 1 ? (Block.first | Block.second) : (Block.first & Block.second);
				for (int i = 0; i < (1 << Bit); ++i)
				{
					for (int r = 0; r < 3; ++r)
					{
						int Value = static_cast<std::int64_t>(a[Block.first + i])
							* Values[Block.second + i][r] % Modulus;
						int Target = (Offset + r) % 3;
						Answer[Target] = Add(Answer[Target], Value);
					}
				}
			}
		}
	}
	for (int Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
