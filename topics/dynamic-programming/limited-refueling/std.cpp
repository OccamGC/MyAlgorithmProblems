// Codex (GPT-6): fuel-state dynamic programming with sliding minima, separately for cost and stop count.
#include <algorithm>
#include <deque>
#include <iostream>
#include <vector>

struct FStation
{
	int Position;
	long long Price;
	long long Stock;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int L;
	int R;
	std::cin >> N >> L >> R;
	int Capacity = R == -1 ? L : R;
	std::vector<FStation> Stations(N);
	for (FStation& Station : Stations)
	{
		std::cin >> Station.Position >> Station.Price >> Station.Stock;
	}
	std::sort(Stations.begin(), Stations.end(), [](const FStation& Left, const FStation& Right)
	{
		return Left.Position < Right.Position;
	});
	if (Stations.empty() || Stations.front().Position != 0)
	{
		Stations.insert(Stations.begin(), FStation{0, 0, 0});
	}
	Stations.push_back(FStation{L, 0, 0});
	constexpr long long Infinity = 4000000000000000000LL;
	constexpr int Unreachable = 1000000000;
	std::vector<long long> Cost(Capacity + 1, Infinity);
	std::vector<int> Stops(Capacity + 1, Unreachable);
	Cost[0] = 0;
	Stops[0] = 0;
	for (int i = 0; i + 1 < static_cast<int>(Stations.size()); ++i)
	{
		int Stock = static_cast<int>(std::min<long long>(Capacity, Stations[i].Stock));
		long long Price = Stations[i].Price;
		int Distance = Stations[i + 1].Position - Stations[i].Position;
		std::vector<long long> NextCost(Capacity + 1, Infinity);
		std::vector<int> NextStops(Capacity + 1, Unreachable);
		std::deque<int> CostQueue;
		std::deque<int> StopQueue;
		for (int Fuel = 0; Fuel <= Capacity; ++Fuel)
		{
			if (Cost[Fuel] != Infinity)
			{
				while (!CostQueue.empty() && Cost[CostQueue.back()] - Price * CostQueue.back() >= Cost[Fuel] - Price * Fuel)
				{
					CostQueue.pop_back();
				}
				CostQueue.push_back(Fuel);
			}
			if (Fuel > 0 && Stops[Fuel - 1] != Unreachable)
			{
				while (!StopQueue.empty() && Stops[StopQueue.back()] >= Stops[Fuel - 1])
				{
					StopQueue.pop_back();
				}
				StopQueue.push_back(Fuel - 1);
			}
			while (!CostQueue.empty() && CostQueue.front() < Fuel - Stock)
			{
				CostQueue.pop_front();
			}
			while (!StopQueue.empty() && StopQueue.front() < Fuel - Stock)
			{
				StopQueue.pop_front();
			}
			if (Fuel >= Distance)
			{
				if (!CostQueue.empty())
				{
					int Previous = CostQueue.front();
					NextCost[Fuel - Distance] = Cost[Previous] + Price * (Fuel - Previous);
				}
				NextStops[Fuel - Distance] = Stops[Fuel];
				if (!StopQueue.empty())
				{
					NextStops[Fuel - Distance] = std::min(NextStops[Fuel - Distance], Stops[StopQueue.front()] + 1);
				}
			}
		}
		Cost.swap(NextCost);
		Stops.swap(NextStops);
	}
	long long MinimumCost = *std::min_element(Cost.begin(), Cost.end());
	int MinimumStops = *std::min_element(Stops.begin(), Stops.end());
	std::cout << (MinimumCost == Infinity ? -1 : MinimumCost) << '\n';
	std::cout << (MinimumStops == Unreachable ? -1 : MinimumStops) << '\n';
}
