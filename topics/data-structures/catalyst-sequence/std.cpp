// Problem setter's solution: split minimum gaps at sqrt(U), using an eight-way bit tree.
// Codex (GPT-6): C++17 implementation; explicit singleton and zero-gap handling.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

class FValueSet
{
	int Base = 0;
	std::vector<std::uint8_t> Mask;
	std::vector<bool> Present;
	std::array<int, 256> First{};
	std::array<int, 256> Last{};

public:
	explicit FValueSet(int Limit) : Present(Limit + 1)
	{
		int Leaves = 1;
		while (Leaves <= Limit)
		{
			Leaves *= 8;
		}
		Base = (Leaves - 1) / 7;
		Mask.resize(Base);
		for (int Bits = 1; Bits < 256; ++Bits)
		{
			for (int i = 0; i < 8; ++i)
			{
				if (Bits & (1 << i))
				{
					Last[Bits] = i;
				}
			}
			for (int i = 7; i >= 0; --i)
			{
				if (Bits & (1 << i))
				{
					First[Bits] = i;
				}
			}
		}
	}

	void Insert(int Value)
	{
		Present[Value] = true;
		for (int Node = Base + Value; Node > 0; )
		{
			int Child = (Node - 1) % 8;
			Node = (Node - 1) / 8;
			bool bWasEmpty = Mask[Node] == 0;
			Mask[Node] |= static_cast<std::uint8_t>(1 << Child);
			if (!bWasEmpty)
			{
				break;
			}
		}
	}

	void Erase(int Value)
	{
		Present[Value] = false;
		for (int Node = Base + Value; Node > 0; )
		{
			int Child = (Node - 1) % 8;
			Node = (Node - 1) / 8;
			Mask[Node] &= static_cast<std::uint8_t>(~(1 << Child));
			if (Mask[Node] != 0)
			{
				break;
			}
		}
	}

	int Neighbour(int Value, bool bNext) const
	{
		if (Present[Value])
		{
			return Value;
		}
		int Node = Base + Value;
		while (Node > 0)
		{
			int Child = (Node - 1) % 8;
			Node = (Node - 1) / 8;
			int Bits = bNext ? (Mask[Node] & (255 << (Child + 1))) : (Mask[Node] & ((1 << Child) - 1));
			if (Bits == 0)
			{
				continue;
			}
			Node = Node * 8 + 1 + (bNext ? First[Bits] : Last[Bits]);
			while (Node < Base)
			{
				Node = Node * 8 + 1 + (bNext ? First[Mask[Node]] : Last[Mask[Node]]);
			}
			return Node - Base;
		}
		return -1;
	}

	int Gap(int Value, int Infinity) const
	{
		int Before = Neighbour(Value, false);
		int After = Neighbour(Value, true);
		int Result = Infinity;
		if (Before >= 0)
		{
			Result = std::min(Result, Value - Before);
		}
		if (After >= 0)
		{
			Result = std::min(Result, After - Value);
		}
		return Result;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> a(n);
	int Upper = 0;
	for (int& Value : a)
	{
		std::cin >> Value;
		Upper = std::max(Upper, Value);
	}
	int Threshold = static_cast<int>(std::sqrt(Upper)) + 1;
	std::vector<int> Answer(Upper);
	std::vector<int> Left(n);
	FValueSet Values(Upper);
	for (int i = 0; i < n; ++i)
	{
		Left[i] = i;
	}
	for (int i = 0; i < n; ++i)
	{
		int Minimum = Upper;
		int j = i;
		for (; j < n; ++j)
		{
			Minimum = std::min(Minimum, Values.Gap(a[j], Upper));
			if (j > i)
			{
				Answer[Minimum] = std::max(Answer[Minimum], j - i + 1);
			}
			if (Minimum <= Threshold)
			{
				break;
			}
			Left[j] = std::min(Left[j], i);
			Values.Insert(a[j]);
		}
		for (int k = i; k < j; ++k)
		{
			Values.Erase(a[k]);
		}
	}
	for (int Gap = std::min(Threshold, Upper - 1); Gap >= 1; --Gap)
	{
		int Begin = 0;
		for (int End = 0; End < n; ++End)
		{
			while (Values.Gap(a[End], Upper) < Gap)
			{
				Values.Erase(a[Begin++]);
			}
			if (Begin < Left[End])
			{
				Left[End] = Begin;
				Answer[Gap] = std::max(Answer[Gap], End - Begin + 1);
			}
			Values.Insert(a[End]);
		}
		for (int i = Begin; i < n; ++i)
		{
			Values.Erase(a[i]);
		}
	}
	std::vector<bool> Seen(Upper + 1);
	for (int Value : a)
	{
		if (Seen[Value])
		{
			Answer[0] = n;
		}
		Seen[Value] = true;
	}
	for (int Value : Answer)
	{
		std::cout << Value << '\n';
	}
}
