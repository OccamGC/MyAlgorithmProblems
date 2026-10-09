// Problem setter's earliest-deadline simulation; GPT-6: monotone bucket implementation.

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
	std::vector<int> Head(m, -1);
	std::vector<int> Next(Devices.size(), -1);
	std::vector<FInt> Energy;
	for (int i = 0; i < static_cast<int>(Devices.size()); ++i)
	{
		Energy.push_back(Devices[i].Initial);
		int Deadline = static_cast<int>(Energy[i] / Devices[i].Drain);
		Next[i] = Head[Deadline];
		Head[Deadline] = i;
	}
	int Earliest = 0;
	for (int Time = 0; Time <= m; ++Time)
	{
		while (Earliest < m && Head[Earliest] == -1)
		{
			++Earliest;
		}
		if (Earliest == m)
		{
			return true;
		}
		if (Earliest < Time)
		{
			return false;
		}
		int i = Head[Earliest];
		Head[Earliest] = Next[i];
		Energy[i] += Power;
		if (Energy[i] < Devices[i].Drain * m)
		{
			int Deadline = static_cast<int>(Energy[i] / Devices[i].Drain);
			Next[i] = Head[Deadline];
			Head[Deadline] = i;
		}
	}
	return false;
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
