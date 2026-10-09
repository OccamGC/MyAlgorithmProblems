#include <algorithm>
#include <iostream>
#include <limits>
#include <queue>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int a;
	int b;
	int p;
	int k;
	int t;
	std::cin >> a >> b >> p >> k >> t;
	std::vector<int> Effect(k);
	for (int& Value : Effect)
	{
		std::cin >> Value;
	}
	std::vector<int> Negative(p);
	std::vector<int> Positive(p);
	for (int i = 0; i < p; ++i)
	{
		for (int j = 0; j < k; ++j)
		{
			int Count;
			std::cin >> Count;
			Negative[i] += std::min(0, Count * Effect[j]);
			Positive[i] += std::max(0, Count * Effect[j]);
		}
	}
	std::vector<int> Flocks(p);
	std::vector<int> Chests;
	std::vector<bool> Blocked(a * b);
	int Start = 0;
	for (int i = 0; i < a * b; ++i)
	{
		std::string Cell;
		std::cin >> Cell;
		if (Cell == "B")
		{
			Blocked[i] = true;
		}
		else if (Cell == "S")
		{
			Start = i;
		}
		else if (Cell == "C")
		{
			Chests.push_back(i);
		}
		else if (Cell != "E")
		{
			Flocks[std::stoi(Cell)] = i;
		}
	}
	std::vector<int> Points = Flocks;
	Points.insert(Points.end(), Chests.begin(), Chests.end());
	Points.push_back(Start);
	const int PointCount = static_cast<int>(Points.size());
	std::vector<std::vector<int>> Distance(PointCount, std::vector<int>(PointCount));
	const int dx[] = {-1, 1, 0, 0};
	const int dy[] = {0, 0, -1, 1};
	for (int i = 0; i < PointCount; ++i)
	{
		std::vector<int> Steps(a * b, -1);
		std::queue<int> Queue;
		Steps[Points[i]] = 0;
		Queue.push(Points[i]);
		while (!Queue.empty())
		{
			const int u = Queue.front();
			Queue.pop();
			for (int d = 0; d < 4; ++d)
			{
				const int x = u / b + dx[d];
				const int y = u % b + dy[d];
				if (x < 0 || x >= a || y < 0 || y >= b)
				{
					continue;
				}
				const int v = x * b + y;
				if (!Blocked[v] && Steps[v] == -1)
				{
					Steps[v] = Steps[u] + 1;
					Queue.push(v);
				}
			}
		}
		for (int j = 0; j < PointCount; ++j)
		{
			Distance[i][j] = Steps[Points[j]];
		}
	}
	std::vector<int> Power(p + 1, 1);
	for (int i = 1; i <= p; ++i)
	{
		Power[i] = Power[i - 1] * 3;
	}
	const int Masks = 1 << p;
	std::vector<int> Code(Masks);
	std::vector<int> NegativeSum(Masks);
	std::vector<int> PositiveSum(Masks);
	for (int Mask = 1; Mask < Masks; ++Mask)
	{
		for (int i = 0; i < p; ++i)
		{
			if (Mask >> i & 1)
			{
				const int Rest = Mask ^ (1 << i);
				Code[Mask] = Code[Rest] + Power[i];
				NegativeSum[Mask] = NegativeSum[Rest] + Negative[i];
				PositiveSum[Mask] = PositiveSum[Rest] + Positive[i];
				break;
			}
		}
	}
	const long long Infinity = std::numeric_limits<long long>::max() / 4;
	std::vector<long long> Dp(Power[p] * p, Infinity);
	for (int i = 0; i < p; ++i)
	{
		Dp[2 * Power[i] * p + i] = 1LL * t * Distance.back()[i];
	}
	long long Answer = Infinity;
	for (int Mask = 1; Mask < Masks; ++Mask)
	{
		const int UnloadedTime = std::max(1, t + NegativeSum[Mask]);
		for (int Carried = Mask; Carried != 0; Carried = (Carried - 1) & Mask)
		{
			const int State = Code[Mask] + Code[Carried];
			const int StepTime = std::max(1, t + NegativeSum[Mask] + PositiveSum[Carried]);
			for (int u = 0; u < p; ++u)
			{
				const long long Current = Dp[State * p + u];
				if (Current == Infinity)
				{
					continue;
				}
				if (Mask == Masks - 1)
				{
					for (int Chest = p; Chest + 1 < PointCount; ++Chest)
					{
						Answer = std::min(Answer, Current + 1LL * Distance[u][Chest] * StepTime);
					}
				}
				for (int v = 0; v < p; ++v)
				{
					if (Mask >> v & 1)
					{
						continue;
					}
					const int DirectState = State + 2 * Power[v];
					long long& Direct = Dp[DirectState * p + v];
					Direct = std::min(Direct, Current + 1LL * Distance[u][v] * StepTime);
					const int UnloadedState = Code[Mask] + 2 * Power[v];
					long long& Unloaded = Dp[UnloadedState * p + v];
					for (int Chest = p; Chest + 1 < PointCount; ++Chest)
					{
						const long long Cost = 1LL * Distance[u][Chest] * StepTime + 1LL * Distance[Chest][v] * UnloadedTime;
						Unloaded = std::min(Unloaded, Current + Cost);
					}
				}
			}
		}
	}
	std::cout << Answer << '\n';
}
