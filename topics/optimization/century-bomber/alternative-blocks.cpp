// Block aggregation. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdio>
#include <cmath>
#include <vector>

int Read()
{
	int Character = std::getchar();
	while (Character != EOF && Character <= ' ')
	{
		Character = std::getchar();
	}
	int Value = 0;
	while (Character >= '0' && Character <= '9')
	{
		Value = Value * 10 + Character - '0';
		Character = std::getchar();
	}
	return Value;
}

void Write(long long Value, char Separator)
{
	char Buffer[32];
	int Length = 0;
	do
	{
		Buffer[Length++] = static_cast<char>('0' + Value % 10);
		Value /= 10;
	}
	while (Value != 0);
	std::reverse(Buffer, Buffer + Length);
	Buffer[Length++] = Separator;
	std::fwrite(Buffer, 1, Length, stdout);
}

int main()
{
	const int n = Read();
	const int m = Read();
	const int k = Read();
	const int q = Read();
	int a[2000];
	int Positions[2000];
	long long OffsetSum[2000] = {};
	long long Answer[2000] = {};
	for (int i = 0; i < n; ++i)
	{
		a[i] = Read();
	}
	for (int i = 0; i < k; ++i)
	{
		Positions[i] = Read() - 1;
	}
	const int h = std::min(n, m);
	const int Width = std::max(1, static_cast<int>(std::sqrt(h)));
	std::vector<std::vector<int>> Counts(h / Width, std::vector<int>(n));
	for (int i = 0; i < q; ++i)
	{
		const int l = Read() - 1;
		const int r = Read();
		const int Length = std::min(r - l, m);
		for (int Block = 0; Block < Length / Width; ++Block)
		{
			++Counts[Block][l];
		}
		for (int j = Length / Width * Width; j < Length; ++j)
		{
			OffsetSum[j] += a[l + j];
		}
	}
	for (int Block = 0; Block < h / Width; ++Block)
	{
		for (int l = 0; l < n; ++l)
		{
			int Count = Counts[Block][l];
			if (Count > 0)
			{
				for (int j = Block * Width; j < (Block + 1) * Width; ++j)
				{
					OffsetSum[j] += static_cast<long long>(Count) * a[l + j];
				}
			}
		}
	}
	for (int i = 0; i < k; ++i)
	{
		for (int j = 0; j < n && Positions[i] + j < m; ++j)
		{
			Answer[Positions[i] + j] += OffsetSum[j];
		}
	}
	for (int i = 0; i < m; ++i)
	{
		Write(Answer[i], i + 1 == m ? '\n' : ' ');
	}
	return 0;
}
