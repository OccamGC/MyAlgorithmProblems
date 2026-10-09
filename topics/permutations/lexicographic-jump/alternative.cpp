// Codex (GPT-6): Lehmer digits, mixed-radix addition, and Fenwick order-statistic decoding.
#include <iostream>
#include <vector>
class FFenwick
{
private:
	std::vector<int> Tree;
public:
	explicit FFenwick(int n) : Tree(n + 1)
	{
	}
	void Add(int i, int Delta)
	{
		for (; i < static_cast<int>(Tree.size()); i += i & -i)
		{
			Tree[i] += Delta;
		}
	}
	int Sum(int i) const
	{
		int Result = 0;
		for (; i; i -= i & -i)
		{
			Result += Tree[i];
		}
		return Result;
	}
	int Select(int Rank) const
	{
		int Position = 0;
		int Step = 1;
		while (Step < static_cast<int>(Tree.size()))
		{
			Step <<= 1;
		}
		for (; Step; Step >>= 1)
		{
			int Next = Position + Step;
			if (Next < static_cast<int>(Tree.size()) && Tree[Next] < Rank)
			{
				Position = Next;
				Rank -= Tree[Next];
			}
		}
		return Position + 1;
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T--)
	{
		int n;
		long long Carry;
		std::cin >> n >> Carry;
		std::vector<int> a(n);
		std::vector<int> Digit(n);
		for (int& Value : a)
		{
			std::cin >> Value;
		}
		FFenwick Counts(n);
		for (int i = n - 1; i >= 0; --i)
		{
			Digit[i] = Counts.Sum(a[i] - 1);
			Counts.Add(a[i], 1);
			long long Total = Digit[i] + Carry;
			Digit[i] = static_cast<int>(Total % (n - i));
			Carry = Total / (n - i);
		}
		for (int i = 0; i < n; ++i)
		{
			int Value = Counts.Select(Digit[i] + 1);
			Counts.Add(Value, -1);
			std::cout << Value << (i + 1 == n ? '\n' : ' ');
		}
	}
}
