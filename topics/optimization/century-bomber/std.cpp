#include <algorithm>
#include <cstdio>

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
	for (int i = 0; i < q; ++i)
	{
		const int l = Read() - 1;
		const int r = Read();
		const int Length = std::min(r - l, m);
		for (int j = 0; j < Length; ++j)
		{
			OffsetSum[j] += a[l + j];
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
