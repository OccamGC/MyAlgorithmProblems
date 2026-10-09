#include <array>
#include <iostream>
#include <vector>

constexpr int Bits = 17;

struct FSegment
{
	std::array<int, Bits> Ones{};
	int Length = 0;
	int Xor = 0;
};

FSegment Merge(const FSegment& Left, const FSegment& Right)
{
	FSegment Result;
	Result.Length = Left.Length + Right.Length;
	Result.Xor = Left.Xor ^ Right.Xor;
	for (int Bit = 0; Bit < Bits; ++Bit)
	{
		Result.Ones[Bit] = Left.Ones[Bit] +
			(((Left.Xor >> Bit) & 1) ? Right.Length - Right.Ones[Bit] : Right.Ones[Bit]);
	}
	return Result;
}

FSegment Leaf(int Value)
{
	FSegment Result;
	Result.Length = 1;
	Result.Xor = Value;
	for (int Bit = 0; Bit < Bits; ++Bit)
	{
		Result.Ones[Bit] = (Value >> Bit) & 1;
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
			long long Answer = 0;
			for (int Bit = 0; Bit < Bits; ++Bit)
			{
				Answer += (1LL << Bit) * Result.Ones[Bit] * (Result.Length + 1 - Result.Ones[Bit]);
			}
			std::cout << Answer << '\n';
		}
	}
}
