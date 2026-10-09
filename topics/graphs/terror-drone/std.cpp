#include <algorithm>
#include <array>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct FStep
{
	int Cell;
	int Axis;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	const int Size = n * m;
	std::vector<std::string> Grid(n);
	for (std::string& Row : Grid)
	{
		std::cin >> Row;
	}
	const std::array<int, 8> dx = {-1, 1, 0, 0, -1, 1, -1, 1};
	const std::array<int, 8> dy = {0, 0, -1, 1, -1, 1, 1, -1};
	std::vector<std::vector<FStep>> Neighbors(Size);
	for (int u = 0; u < Size; ++u)
	{
		for (int d = 0; d < 8; ++d)
		{
			int x = u / m + dx[d];
			int y = u % m + dy[d];
			if (0 <= x && x < n && 0 <= y && y < m)
			{
				Neighbors[u].push_back({x * m + y, d / 2});
			}
		}
	}
	std::vector<int> Component(Size, 0);
	int ComponentCount = 0;
	for (int u = 0; u < Size; ++u)
	{
		if (Grid[u / m][u % m] != 'B' || Component[u] != 0)
		{
			continue;
		}
		std::queue<int> Queue;
		Queue.push(u);
		Component[u] = ++ComponentCount;
		while (!Queue.empty())
		{
			int v = Queue.front();
			Queue.pop();
			for (const FStep& Step : Neighbors[v])
			{
				int w = Step.Cell;
				if (Step.Axis < 2 && Grid[w / m][w % m] == 'B' && Component[w] == 0)
				{
					Component[w] = ComponentCount;
					Queue.push(w);
				}
			}
		}
	}
	const int Infinity = Size * 4 + 1;
	std::vector<int> Answer(Size, Infinity);
	std::vector<bool> Reachable(Size, false);
	for (int Bomb = 0; Bomb <= ComponentCount; ++Bomb)
	{
		auto IsOpen = [&](int Cell)
		{
			return Component[Cell] == 0 || Component[Cell] == Bomb;
		};
		std::vector<int> Distance(Size * 4, -1);
		std::vector<bool> Visited(Size, false);
		std::queue<int> Queue;
		std::queue<int> Flood;
		for (int u = 0; u < Size; ++u)
		{
			if (Grid[u / m][u % m] == 'T')
			{
				Visited[u] = true;
				Flood.push(u);
				for (int Axis = 0; Axis < 4; ++Axis)
				{
					Distance[u * 4 + Axis] = 0;
					Queue.push(u * 4 + Axis);
				}
			}
		}
		while (!Flood.empty())
		{
			int u = Flood.front();
			Flood.pop();
			Reachable[u] = true;
			for (const FStep& Step : Neighbors[u])
			{
				if (IsOpen(Step.Cell) && !Visited[Step.Cell])
				{
					Visited[Step.Cell] = true;
					Flood.push(Step.Cell);
				}
			}
		}
		while (!Queue.empty())
		{
			int State = Queue.front();
			Queue.pop();
			int u = State / 4;
			Answer[u] = std::min(Answer[u], Distance[State]);
			for (const FStep& Step : Neighbors[u])
			{
				int Next = Step.Cell * 4 + Step.Axis;
				if (Step.Axis != State % 4 && IsOpen(Step.Cell) && Distance[Next] == -1)
				{
					Distance[Next] = Distance[State] + 1;
					Queue.push(Next);
				}
			}
		}
	}
	for (int u = 0; u < Size; ++u)
	{
		if (Grid[u / m][u % m] == 'S')
		{
			std::cout << (Answer[u] != Infinity ? Answer[u] : (Reachable[u] ? -2 : -1)) << '\n';
		}
	}
}
