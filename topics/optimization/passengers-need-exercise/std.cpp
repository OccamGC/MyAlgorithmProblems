#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using FInt64 = std::int64_t;

static FInt64 Evaluate(FInt64 TwiceStart, const std::vector<FInt64>& PassengerPositions,
	const std::vector<FInt64>& DoorOffsets)
{
	FInt64 Total = 0;
	std::size_t DoorIndex = 0;
	for (FInt64 Position : PassengerPositions)
	{
		while (DoorIndex + 1 < DoorOffsets.size()
			&& std::abs(TwiceStart + 2 * DoorOffsets[DoorIndex + 1] - 2 * Position)
				< std::abs(TwiceStart + 2 * DoorOffsets[DoorIndex] - 2 * Position))
		{
			++DoorIndex;
		}
		Total += std::abs(TwiceStart + 2 * DoorOffsets[DoorIndex] - 2 * Position);
	}
	return Total;
}

static void PrintHalf(FInt64 TwiceValue)
{
	std::cout << TwiceValue / 2 << (TwiceValue % 2 == 0 ? ".0" : ".5");
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	FInt64 L;
	int M;
	int N;
	if (!(std::cin >> L >> M))
	{
		return 0;
	}
	std::vector<FInt64> PassengerPositions(M);
	for (FInt64& Position : PassengerPositions)
	{
		std::cin >> Position;
	}
	std::cin >> N;
	std::vector<FInt64> DoorOffsets(N, 0);
	for (int i = 1; i < N; ++i)
	{
		std::cin >> DoorOffsets[i];
	}

	const FInt64 LastStart = 2 * (L - DoorOffsets.back());
	FInt64 BestStart = 0;
	FInt64 BestTotal = Evaluate(0, PassengerPositions, DoorOffsets);
	auto Consider = [&](FInt64 Candidate)
	{
		if (Candidate < 0 || Candidate > LastStart)
		{
			return;
		}
		FInt64 Value = Evaluate(Candidate, PassengerPositions, DoorOffsets);
		if (Value > BestTotal || (Value == BestTotal && Candidate < BestStart))
		{
			BestTotal = Value;
			BestStart = Candidate;
		}
	};

	Consider(LastStart);
	for (FInt64 Position : PassengerPositions)
	{
		for (int i = 1; i < N; ++i)
		{
			Consider(2 * Position - DoorOffsets[i - 1] - DoorOffsets[i]);
		}
	}
	PrintHalf(BestStart);
	std::cout << ' ';
	PrintHalf(BestTotal);
	std::cout << '\n';
}
