// Problem setter's solution: doubly linked ring and shortest-direction moves.
// Codex (GPT-6): portable implementation and explicit empty-ring invariants.
#include <array>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::array<int, 2>> Link(n + m + 1);
	for (int i = 1; i <= n; ++i)
	{
		Link[i] = {i == n ? 1 : i + 1, i == 1 ? n : i - 1};
	}
	int Size = n;
	int LastId = n;
	int Current = 1;
	for (int i = 0; i < m; ++i)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 0 && Size > 0)
		{
			int Next = Link[Current][0];
			int Previous = Link[Current][1];
			Link[Previous][0] = Next;
			Link[Next][1] = Previous;
			--Size;
			Current = Size == 0 ? 0 : Next;
		}
		else if (Operation == 1)
		{
			++LastId;
			if (Size == 0)
			{
				Current = LastId;
				Link[Current] = {Current, Current};
			}
			else
			{
				int Next = Link[Current][0];
				Link[LastId] = {Next, Current};
				Link[Current][0] = LastId;
				Link[Next][1] = LastId;
			}
			++Size;
		}
		else if (Operation == 2 || Operation == 3)
		{
			int x;
			std::cin >> x;
			if (Size == 0)
			{
				continue;
			}
			int Steps = (x % Size + Size) % Size;
			int Direction = Operation - 2;
			if (Size - Steps < Steps)
			{
				Steps = Size - Steps;
				Direction ^= 1;
			}
			while (Steps-- > 0)
			{
				Current = Link[Current][Direction];
			}
		}
		else if (Operation == 4)
		{
			std::cout << (Size == 0 ? -1 : Current) << '\n';
		}
	}
}
