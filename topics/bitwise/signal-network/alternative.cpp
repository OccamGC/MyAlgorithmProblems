// Problem setter's solution: a circular origin and segment-tree XOR flags.
// Codex (GPT-6): portable recursive interval traversal and explicit wrap handling.
#include <array>
#include <iostream>

struct FSignal
{
	std::array<bool, 512> Flags{};
	int Origin = 0;
	bool bDirty = true;
	unsigned int Cached = 0;

	void FlipRange(int Node, int Left, int Right, int QueryLeft, int QueryRight)
	{
		if (QueryLeft <= Left && Right <= QueryRight)
		{
			Flags[Node] = !Flags[Node];
			return;
		}
		const int Middle = (Left + Right) / 2;
		if (QueryLeft <= Middle)
		{
			FlipRange(Node * 2, Left, Middle, QueryLeft, QueryRight);
		}
		if (QueryRight > Middle)
		{
			FlipRange(Node * 2 + 1, Middle + 1, Right, QueryLeft, QueryRight);
		}
	}

	unsigned int ReadRange(int Node, int Left, int Right, int QueryLeft, int QueryRight, bool bInherited) const
	{
		const bool bValue = bInherited != Flags[Node];
		if (Left == Right)
		{
			return static_cast<unsigned int>(bValue) << (Left - QueryLeft);
		}
		const int Middle = (Left + Right) / 2;
		unsigned int Result = 0;
		if (QueryLeft <= Middle)
		{
			Result |= ReadRange(Node * 2, Left, Middle, QueryLeft, QueryRight, bValue);
		}
		if (QueryRight > Middle)
		{
			Result |= ReadRange(Node * 2 + 1, Middle + 1, Right, QueryLeft, QueryRight, bValue);
		}
		return Result;
	}

	void Rotate(int Shift)
	{
		Origin = (Origin + Shift) % 128;
		bDirty = true;
	}

	void Flip(int l, int r)
	{
		const int Start = (Origin + l) % 128;
		const int End = Start + r - l;
		if (End < 128)
		{
			FlipRange(1, 0, 127, Start, End);
		}
		else
		{
			FlipRange(1, 0, 127, Start, 127);
			FlipRange(1, 0, 127, 0, End - 128);
		}
		bDirty = true;
	}

	unsigned int LowBits()
	{
		if (!bDirty)
		{
			return Cached;
		}
		if (Origin + 15 < 128)
		{
			Cached = ReadRange(1, 0, 127, Origin, Origin + 15, false);
		}
		else
		{
			Cached = ReadRange(1, 0, 127, Origin, 127, false);
			Cached |= ReadRange(1, 0, 127, 0, Origin + 15 - 128, false) << (128 - Origin);
		}
		bDirty = false;
		return Cached;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	FSignal Signal;
	int N;
	std::cin >> N;
	for (int i = 0; i < N; ++i)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 1)
		{
			int x;
			std::cin >> x;
			Signal.Rotate((x % 128 + 128) % 128);
		}
		else if (Operation == 2)
		{
			std::cout << std::uppercase << std::hex << Signal.LowBits() << std::dec << '\n';
		}
		else
		{
			int l;
			int r;
			std::cin >> l >> r;
			Signal.Flip(l, r);
		}
	}
}
