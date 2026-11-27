// Segment tree with explicit cross sums. C++17 implementation by Codex (GPT-6).
#include <array>
#include <iostream>
#include <vector>

constexpr int Bits = 17;

struct FSegment
{
	std::array<std::array<int, 2>, Bits> Prefix{};
	long long Sum = 0;
	int Xor = 0;
};

FSegment Merge(const FSegment& Left, const FSegment& Right)
{
	FSegment Result;
	Result.Xor = Left.Xor ^ Right.Xor;
	Result.Sum = Left.Sum + Right.Sum;
	for (int Bit = 0; Bit < Bits; ++Bit)
	{
		const int Flip = (Left.Xor >> Bit) & 1;
		auto Suffix = Left.Prefix[Bit];
		// Replace the full prefix by the empty prefix, then XOR with the whole left half.
		--Suffix[Flip];
		++Suffix[0];
		Result.Sum += (1LL << Bit) * (1LL * Suffix[Flip] * Right.Prefix[Bit][1]
			+ 1LL * Suffix[Flip ^ 1] * Right.Prefix[Bit][0]);
		for (int b = 0; b < 2; ++b)
		{
			Result.Prefix[Bit][b] = Left.Prefix[Bit][b] + Right.Prefix[Bit][b ^ Flip];
		}
	}
	return Result;
}

FSegment Leaf(int Value)
{
	FSegment Result;
	Result.Sum = Value;
	Result.Xor = Value;
	for (int Bit = 0; Bit < Bits; ++Bit)
	{
		++Result.Prefix[Bit][(Value >> Bit) & 1];
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int q;
	std::cin >> n >> q;
	int Base = 1;
	while (Base < n)
	{
		Base *= 2;
	}
	std::vector<FSegment> Tree(2 * Base);
	for (int i = 0; i < n; ++i)
	{
		int Value;
		std::cin >> Value;
		Tree[Base + i] = Leaf(Value);
	}
	for (int i = Base - 1; i > 0; --i)
	{
		Tree[i] = Merge(Tree[2 * i], Tree[2 * i + 1]);
	}
	while (q--)
	{
		int Operation;
		int l;
		int r;
		std::cin >> Operation >> l >> r;
		if (Operation == 2)
		{
			int Node = Base + l - 1;
			Tree[Node] = Leaf(r);
			while ((Node /= 2) > 0)
			{
				Tree[Node] = Merge(Tree[2 * Node], Tree[2 * Node + 1]);
			}
		}
		else
		{
			FSegment Left;
			FSegment Right;
			l += Base - 1;
			r += Base;
			while (l < r)
			{
				if (l & 1)
				{
					Left = Merge(Left, Tree[l++]);
				}
				if (r & 1)
				{
					Right = Merge(Tree[--r], Right);
				}
				l /= 2;
				r /= 2;
			}
			FSegment Result = Merge(Left, Right);
			std::cout << Result.Sum << '\n';
		}
	}
}
