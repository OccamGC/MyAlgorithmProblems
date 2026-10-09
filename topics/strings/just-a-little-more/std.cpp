#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

class FEncore
{
public:
	explicit FEncore(std::string InitialText) : Initial(std::move(InitialText))
	{
		Lengths.push_back(Initial.size());
		for (int Version = 2; Version <= 70; ++Version)
		{
			const std::size_t Previous = Lengths.back();
			Lengths.push_back(Previous + (Previous + 4) / 5);
		}
	}

	void PrintVersion(int Version) const
	{
		PrintPrefix(Lengths[Version - 1]);
		std::cout << '\n';
	}

private:
	std::string Initial;
	std::vector<std::size_t> Lengths;

	void PrintPrefix(std::size_t Count) const
	{
		if (Count <= Initial.size())
		{
			std::cout.write(Initial.data(), static_cast<std::streamsize>(Count));
			return;
		}
		const auto Version = std::lower_bound(Lengths.begin(), Lengths.end(), Count);
		const std::size_t Previous = *(Version - 1);
		PrintPrefix(Previous);
		PrintPrefix(Count - Previous);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	std::string Initial;
	if (!(std::cin >> Initial))
	{
		return 0;
	}
	FEncore Encore(std::move(Initial));
	int Q;
	std::cin >> Q;
	for (int i = 0; i < Q; ++i)
	{
		int x;
		std::cin >> x;
		Encore.PrintVersion(x);
	}
}
