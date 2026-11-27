// Slope sweep. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
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
	// Left of every breakpoint, every passenger's distance has slope -1.
	std::vector<std::pair<FInt64, int>> Events;
	for (FInt64 Position : PassengerPositions)
	{
		for (int i = 0; i < N; ++i)
		{
			Events.emplace_back(2 * (Position - DoorOffsets[i]), 2);
			if (i > 0)
			{
				Events.emplace_back(2 * Position - DoorOffsets[i - 1] - DoorOffsets[i], -2);
			}
		}
	}
	Events.emplace_back(LastStart, 0);
	std::sort(Events.begin(), Events.end());
	FInt64 Slope = -M;
	FInt64 Previous = 0;
	FInt64 Total = BestTotal;
	for (auto [Position, Change] : Events)
	{
		if (Position > LastStart)
		{
			break;
		}
		if (Position >= 0)
		{
			Total += Slope * (Position - Previous);
			if (Total > BestTotal)
			{
				BestTotal = Total;
				BestStart = Position;
			}
			Previous = Position;
		}
		Slope += Change;
	}
	PrintHalf(BestStart);
	std::cout << ' ';
	PrintHalf(BestTotal);
	std::cout << '\n';
}
