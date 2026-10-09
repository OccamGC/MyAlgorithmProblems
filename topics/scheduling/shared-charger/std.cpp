// Setter: deadline histogram and binary search. GPT-6: boundary/overflow fixes, implementation.

#include <algorithm>
#include <iostream>
#include <vector>
using FInt = long long;
struct FDevice
{
	FInt Initial;
	FInt Drain;
};

bool Feasible(const std::vector<FDevice>& Devices, int m, FInt Power)
{
	std::vector<int> Deadlines(m);
	int Total = 0;
	for (const FDevice& Device : Devices)
	{
		FInt Energy = Device.Initial;
		while (Energy < Device.Drain * m)
		{
			int Deadline = static_cast<int>(Energy / Device.Drain);
			if (++Total > m || ++Deadlines[Deadline] > Deadline + 1)
			{
				return false;
			}
			Energy += Power;
		}
	}
	Total = 0;
	for (int Time = 0; Time < m; ++Time)
	{
		Total += Deadlines[Time];
		if (Total > Time + 1)
		{
			return false;
		}
	}
	return true;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<FInt> Initial(n);
	for (FInt& Value : Initial)
	{
		std::cin >> Value;
	}
	std::vector<FDevice> Devices;
	FInt High = 0;
	for (int i = 0; i < n; ++i)
	{
		FInt Drain;
		std::cin >> Drain;
		FInt Deficit = Drain * m - Initial[i];
		if (Deficit > 0)
		{
			Devices.push_back({Initial[i], Drain});
			High = std::max(High, Deficit);
		}
	}
	if (!Feasible(Devices, m, High))
	{
		std::cout << -1 << '\n';
		return 0;
	}
	FInt Low = 0;
	while (Low < High)
	{
		FInt Middle = Low + (High - Low) / 2;
		if (Feasible(Devices, m, Middle))
		{
			High = Middle;
		}
		else
		{
			Low = Middle + 1;
		}
	}
	std::cout << Low << '\n';
}
