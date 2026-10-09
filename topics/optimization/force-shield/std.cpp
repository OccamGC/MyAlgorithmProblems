#include <algorithm>
#include <deque>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

struct FEvent
{
	int Left;
	int Right;
	int Start;
	int End;
	int Damage;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int r;
	int s;
	int a;
	int b;
	std::cin >> n >> m >> r >> s >> a >> b;
	std::vector<std::pair<int, int>> Buildings(n);
	int MinPosition = 1500;
	int MaxPosition = -1499;
	for (auto& Building : Buildings)
	{
		std::cin >> Building.first >> Building.second;
		MinPosition = std::min(MinPosition, Building.first);
		MaxPosition = std::max(MaxPosition, Building.first);
	}
	std::vector<FEvent> Events(a + b);
	int Horizon = 0;
	for (int i = 0; i < a + b; ++i)
	{
		FEvent& Event = Events[i];
		int Duration;
		std::cin >> Event.Left >> Event.Right >> Event.Start >> Duration >> Event.Damage;
		Event.End = Event.Start + Duration - 1;
		if (i >= a)
		{
			Event.Damage = -Event.Damage;
		}
		Horizon = std::max(Horizon, Event.End);
	}
	if (Horizon == 0)
	{
		std::cout << 0 << '\n';
		return 0;
	}
	int Width = MaxPosition - MinPosition + 1;
	int Stride = Horizon + 2;
	auto Index = [Stride](int x, int t)
	{
		return static_cast<std::size_t>(x) * Stride + t;
	};
	std::vector<int> Count(static_cast<std::size_t>(Width + 1) * Stride, 0);
	for (const auto& Building : Buildings)
	{
		if (Building.second <= Horizon)
		{
			++Count[Index(Building.first - MinPosition, Building.second)];
		}
	}
	std::vector<std::pair<int, int>>().swap(Buildings);
	std::vector<long long> Damage(Count.size(), 0);
	for (const FEvent& Event : Events)
	{
		int Left = std::max(Event.Left, MinPosition) - MinPosition;
		int Right = std::min(Event.Right, MaxPosition) - MinPosition;
		if (Left > Right)
		{
			continue;
		}
		Damage[Index(Left, Event.Start)] += Event.Damage;
		Damage[Index(Right + 1, Event.Start)] -= Event.Damage;
		Damage[Index(Left, Event.End + 1)] -= Event.Damage;
		Damage[Index(Right + 1, Event.End + 1)] += Event.Damage;
	}
	std::vector<FEvent>().swap(Events);
	// Recover the per-position, per-time net damage before prefixing time again.
	for (int x = 0; x < Width; ++x)
	{
		for (int t = 1; t <= Horizon; ++t)
		{
			Damage[Index(x, t)] += Damage[Index(x, t - 1)];
			if (x > 0)
			{
				Damage[Index(x, t)] += Damage[Index(x - 1, t)] - Damage[Index(x - 1, t - 1)];
			}
		}
	}
	long long Baseline = 0;
	for (int x = 0; x < Width; ++x)
	{
		for (int t = 1; t <= Horizon; ++t)
		{
			Count[Index(x, t)] += Count[Index(x, t - 1)];
			Baseline += static_cast<long long>(Count[Index(x, t)]) * Damage[Index(x, t)];
			Damage[Index(x, t)] += Damage[Index(x, t - 1)];
		}
	}
	std::vector<long long> Best(Horizon + 2, 0);
	std::vector<long long> Prefix(Width + 1, 0);
	for (int t = Horizon; t >= 1; --t)
	{
		int End = std::min(Horizon, t + r - 1);
		for (int x = 0; x < Width; ++x)
		{
			long long Gain = static_cast<long long>(Count[Index(x, t)]) *
				(Damage[Index(x, End)] - Damage[Index(x, t - 1)]);
			Prefix[x + 1] = Prefix[x] + Gain;
		}
		std::deque<int> Minimum;
		Minimum.push_back(0);
		long long Gain = 0;
		for (int Right = 1; Right <= Width; ++Right)
		{
			while (Minimum.front() < Right - (m + 1))
			{
				Minimum.pop_front();
			}
			Gain = std::max(Gain, Prefix[Right] - Prefix[Minimum.front()]);
			while (!Minimum.empty() && Prefix[Minimum.back()] >= Prefix[Right])
			{
				Minimum.pop_back();
			}
			Minimum.push_back(Right);
		}
		Best[t] = std::max(Best[t + 1], Gain + Best[std::min(Horizon + 1, t + r + s)]);
	}
	std::cout << Baseline - Best[1] << '\n';
}
