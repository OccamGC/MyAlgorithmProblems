// Problem setter's solution: rotations and interval masks on a 128-bit word.
// Codex (GPT-6): portable two-word C++17 implementation with valid shift counts.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>

struct FSignal
{
	std::uint64_t Low = 0;
	std::uint64_t High = 0;

	static std::uint64_t Prefix(int Count)
	{
		if (Count == 64)
		{
			return ~std::uint64_t{0};
		}
		return (std::uint64_t{1} << Count) - 1;
	}

	void Rotate(int Shift)
	{
		if (Shift >= 64)
		{
			std::swap(Low, High);
			Shift -= 64;
		}
		if (Shift != 0)
		{
			const std::uint64_t OldLow = Low;
			Low = (Low >> Shift) | (High << (64 - Shift));
			High = (High >> Shift) | (OldLow << (64 - Shift));
		}
	}

	void Flip(int l, int r)
	{
		if (l < 64)
		{
			Low ^= Prefix(std::min(r + 1, 64)) ^ Prefix(l);
		}
		if (r >= 64)
		{
			High ^= Prefix(r - 63) ^ Prefix(std::max(l - 64, 0));
		}
	}

	unsigned int LowBits() const
	{
		return static_cast<unsigned int>(Low & 65535);
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
