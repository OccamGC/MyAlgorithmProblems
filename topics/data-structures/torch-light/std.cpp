#include <algorithm>
#include <cstdio>
#include <vector>

class FInput
{
	char Buffer[1 << 16];
	std::size_t Position = 0;
	std::size_t Length = 0;

	int Get()
	{
		if (Position == Length)
		{
			Length = std::fread(Buffer, 1, sizeof(Buffer), stdin);
			Position = 0;
			if (Length == 0)
			{
				return EOF;
			}
		}
		return Buffer[Position++];
	}

public:
	long long Read()
	{
		int Character = Get();
		while (Character != EOF && Character <= ' ')
		{
			Character = Get();
		}
		const bool bNegative = Character == '-';
		if (bNegative)
		{
			Character = Get();
		}
		long long Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return bNegative ? -Value : Value;
	}
};

struct FParityGrid
{
	int FirstU;
	int FirstV;
	int Rows;
	int Columns;
	std::vector<long long> Difference;

	FParityGrid(int n, int m, int Parity)
	{
		FirstU = Parity;
		FirstV = -(m - 1);
		if ((FirstV - Parity) % 2 != 0)
		{
			++FirstV;
		}
		Rows = n + m - 2 < FirstU ? 0 : (n + m - 2 - FirstU) / 2 + 1;
		Columns = n - 1 < FirstV ? 0 : (n - 1 - FirstV) / 2 + 1;
		Difference.resize(static_cast<std::size_t>(Rows + 1) * (Columns + 1));
	}

	long long& At(int i, int j)
	{
		return Difference[static_cast<std::size_t>(i) * (Columns + 1) + j];
	}

	void Add(int u, int v, int Radius, long long Value)
	{
		if (Radius == 0 || Rows == 0 || Columns == 0)
		{
			return;
		}
		const int LowU = std::max(FirstU, u - Radius + 1);
		const int HighU = std::min(FirstU + 2 * (Rows - 1), u + Radius - 1);
		const int LowV = std::max(FirstV, v - Radius + 1);
		const int HighV = std::min(FirstV + 2 * (Columns - 1), v + Radius - 1);
		if (LowU > HighU || LowV > HighV)
		{
			return;
		}
		const int a = (LowU - FirstU + 1) / 2;
		const int b = (HighU - FirstU) / 2;
		const int c = (LowV - FirstV + 1) / 2;
		const int d = (HighV - FirstV) / 2;
		if (a > b || c > d)
		{
			return;
		}
		At(a, c) += Value;
		At(b + 1, c) -= Value;
		At(a, d + 1) -= Value;
		At(b + 1, d + 1) += Value;
	}

	void Accumulate()
	{
		for (int i = 0; i < Rows; ++i)
		{
			long long RowSum = 0;
			for (int j = 0; j < Columns; ++j)
			{
				RowSum += At(i, j);
				At(i, j) = RowSum + (i == 0 ? 0 : At(i - 1, j));
			}
		}
	}

	long long Get(int u, int v)
	{
		return At((u - FirstU) / 2, (v - FirstV) / 2);
	}
};

int main()
{
	FInput Input;
	const int n = static_cast<int>(Input.Read());
	const int m = static_cast<int>(Input.Read());
	FParityGrid Even(n, m, 0);
	FParityGrid Odd(n, m, 1);
	for (int x = 0; x < n; ++x)
	{
		for (int y = 0; y < m; ++y)
		{
			const long long Light = Input.Read();
			const int Radius = static_cast<int>(Input.Read());
			if (Light != 0)
			{
				Even.Add(x + y, x - y, Radius, Light);
				Odd.Add(x + y, x - y, Radius, Light);
			}
		}
	}
	Even.Accumulate();
	Odd.Accumulate();
	int Answer = 0;
	for (int x = 0; x < n; ++x)
	{
		for (int y = 0; y < m; ++y)
		{
			const long long Threshold = Input.Read();
			const long long Brightness = ((x + y) & 1) ? Odd.Get(x + y, x - y) : Even.Get(x + y, x - y);
			Answer += Brightness <= Threshold;
		}
	}
	std::printf("%d\n", Answer);
	return 0;
}
