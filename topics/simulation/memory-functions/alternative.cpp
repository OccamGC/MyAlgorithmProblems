// Problem setter's solution: checked flat-memory simulation. Codex (GPT-6): portable atomic updates and safe address arithmetic.
#include <algorithm>
#include <iostream>
#include <vector>

class FMemory
{
private:
	std::vector<int> Data;
public:
	explicit FMemory(const std::vector<int>& Initial) : Data(Initial)
	{
	}
	int Size() const
	{
		return static_cast<int>(Data.size());
	}
	int Read(int Position) const
	{
		return Data[Position];
	}
	void Fill(int Left, int Right, int Value)
	{
		std::fill(Data.begin() + Left, Data.begin() + Right, Value);
	}
	int FirstZero(int Position) const
	{
		while (Position < Size() && Data[Position] != 0)
		{
			++Position;
		}
		return Position;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Start(n + 1);
	for (int i = 0; i < n; ++i)
	{
		int Length;
		std::cin >> Length;
		Start[i + 1] = Start[i] + Length;
	}
	std::vector<int> Initial(Start[n]);
	for (int& Value : Initial)
	{
		std::cin >> Value;
	}
	FMemory Memory(Initial);
	auto InArray = [&](int Array, long long Left, long long End)
	{
		return Start[Array] <= Left && End <= Start[Array + 1];
	};
	int k;
	std::cin >> k;
	while (k--)
	{
		int Operation;
		int Array;
		long long Offset;
		std::cin >> Operation >> Array >> Offset;
		long long Begin = Start[Array] + Offset;
		if (Operation == 0)
		{
			int Value;
			long long Count;
			std::cin >> Value >> Count;
			if (Count == 0)
			{
				std::cout << "true\n";
				continue;
			}
			long long End = Begin + Count;
			if (Begin < 0 || End > Memory.Size())
			{
				std::cout << "overflow\n";
				continue;
			}
			bool bWarning = !InArray(Array, Begin, End);
			Memory.Fill(static_cast<int>(Begin), static_cast<int>(End), Value);
			std::cout << (bWarning ? "wtrue\n" : "true\n");
			continue;
		}
		int DestinationArray = 0;
		long long Destination = 0;
		if (Operation == 1)
		{
			std::cin >> DestinationArray >> Offset;
			Destination = Start[DestinationArray] + Offset;
		}
		if (Begin < 0 || Begin >= Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		int Zero = Memory.FirstZero(static_cast<int>(Begin));
		if (Zero == Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		long long Count = Zero - Begin + 1;
		bool bWarning = !InArray(Array, Begin, Zero + 1);
		if (Operation == 2)
		{
			std::cout << (bWarning ? "w" : "") << Count - 1 << '\n';
			continue;
		}
		long long End = Destination + Count;
		if (Destination < 0 || End > Memory.Size())
		{
			std::cout << "overflow\n";
			continue;
		}
		if (std::max(Begin, Destination) < std::min(Begin + Count, End))
		{
			std::cout << "overwrite\n";
			continue;
		}
		bWarning = bWarning || !InArray(DestinationArray, Destination, End);
		Memory.Fill(static_cast<int>(Destination), static_cast<int>(End - 1), 1);
		Memory.Fill(static_cast<int>(End - 1), static_cast<int>(End), 0);
		std::cout << (bWarning ? "wtrue\n" : "true\n");
	}
}
