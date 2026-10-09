// Codex (GPT-6): fixed-length sliding windows with two ordered multisets.
// The standard balanced-partition method lets answers stream in required order.
#include <iostream>
#include <iterator>
#include <set>
#include <vector>

struct FPartition
{
	std::multiset<long long> Lower;
	std::multiset<long long> Upper;
	long long UpperSum = 0;

	void Add(long long Value)
	{
		Lower.insert(Value);
	}

	void Remove(long long Value)
	{
		auto Found = Lower.find(Value);
		if (Found != Lower.end())
		{
			Lower.erase(Found);
		}
		else
		{
			Upper.erase(Upper.find(Value));
			UpperSum -= Value;
		}
	}

	void Balance(int LowerSize)
	{
		while (static_cast<int>(Lower.size()) > LowerSize)
		{
			auto Found = std::prev(Lower.end());
			UpperSum += *Found;
			Upper.insert(*Found);
			Lower.erase(Found);
		}
		while (static_cast<int>(Lower.size()) < LowerSize)
		{
			auto Found = Upper.begin();
			UpperSum -= *Found;
			Lower.insert(*Found);
			Upper.erase(Found);
		}
		while (!Lower.empty() && !Upper.empty() && *Lower.rbegin() > *Upper.begin())
		{
			auto Low = std::prev(Lower.end());
			auto High = Upper.begin();
			long long LowValue = *Low;
			long long HighValue = *High;
			Lower.erase(Low);
			Upper.erase(High);
			Lower.insert(HighValue);
			Upper.insert(LowValue);
			UpperSum += LowValue - HighValue;
		}
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<long long> a(n);
	for (long long& Value : a)
	{
		std::cin >> Value;
	}
	for (int Length = 1; Length <= n; ++Length)
	{
		FPartition Partition;
		for (int i = 0; i < Length; ++i)
		{
			Partition.Add(a[i]);
		}
		for (int l = 0; l + Length <= n; ++l)
		{
			if (l > 0)
			{
				Partition.Remove(a[l - 1]);
				Partition.Add(a[l + Length - 1]);
			}

			Partition.Balance((Length + 1) / 2);
			long long Answer = Length % 2 == 1
				? 2 * *Partition.Lower.rbegin() : *Partition.Lower.rbegin() + *Partition.Upper.begin();
			std::cout << Answer << '\n';

		}
	}
}
