// Setter: repeated-pivot substring queries and binary search for neighbors.
// GPT-6: endpoint growth, explicit protocol, safe sizing, and query-bound proof.
#pragma once
#include <algorithm>
#include <deque>
#include <numeric>
#include <vector>
template<class FAsk>
std::vector<int> RecoverPermutation(int n, FAsk Ask)
{
	if (n == 1)
	{
		return {1};
	}
	std::vector<int> Candidates(n - 1);
	std::iota(Candidates.begin(), Candidates.end(), 2);
	// At least one of the two neighbors of 1 is in this candidate set.
	while (Candidates.size() > 1)
	{
		int Half = std::min(49, static_cast<int>(Candidates.size()) / 2);
		std::vector<int> Query{1};
		for (int i = 0; i < Half; ++i)
		{
			Query.push_back(Candidates[i]);
			Query.push_back(1);
		}
		if (Ask(Query) >= 2)
		{
			Candidates.resize(Half);
		}
		else
		{
			Candidates.erase(Candidates.begin(), Candidates.begin() + Half);
		}
	}
	int Neighbor = Candidates[0];
	std::deque<int> Chain;
	if (Ask(std::vector<int>{1, Neighbor}) == 2)
	{
		Chain = {1, Neighbor};
	}
	else
	{
		Chain = {Neighbor, 1};
	}
	std::vector<bool> Used(n + 1, false);
	Used[1] = true;
	Used[Neighbor] = true;
	bool bRight = true;
	while (static_cast<int>(Chain.size()) < n)
	{
		Candidates.clear();
		for (int Value = 1; Value <= n; ++Value)
		{
			if (!Used[Value])
			{
				Candidates.push_back(Value);
			}
		}
		int Endpoint = bRight ? Chain.back() : Chain.front();
		bool bExists = false;
		while (!Candidates.empty() && (!bExists || Candidates.size() > 1))
		{
			int Half = std::min(50, (static_cast<int>(Candidates.size()) + (bExists ? 0 : 1)) / 2);
			std::vector<int> Query;
			for (int i = 0; i < Half; ++i)
			{
				Query.push_back(bRight ? Endpoint : Candidates[i]);
				Query.push_back(bRight ? Candidates[i] : Endpoint);
			}
			if (Ask(Query) >= 2)
			{
				Candidates.resize(Half);
				bExists = true;
			}
			else
			{
				Candidates.erase(Candidates.begin(), Candidates.begin() + Half);
			}
		}
		if (Candidates.empty())
		{
			bRight = false;
		}
		else
		{
			int Value = Candidates[0];
			Used[Value] = true;
			if (bRight)
			{
				Chain.push_back(Value);
			}
			else
			{
				Chain.push_front(Value);
			}
		}
	}
	return std::vector<int>(Chain.begin(), Chain.end());
}
