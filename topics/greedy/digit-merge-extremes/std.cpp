// Problem setter's greedy digit-pair selection. Codex (GPT-6): proof, boundary checks and portable implementation.

#include <algorithm>
#include <array>
#include <cstdio>
#include <iterator>
#include <map>
#include <string>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

class FInput
{
	char Buffer[1 << 16];
	int Position = 0;
	int Length = 0;
public:
	int Get()
	{
		if (Position == Length)
		{
			Length = static_cast<int>(std::fread(Buffer, 1, sizeof(Buffer), stdin));
			Position = 0;
			if (Length == 0)
			{
				return EOF;
			}
		}
		return Buffer[Position++];
	}
	int Read()
	{
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		bool bNegative = Character == '-';
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
		return static_cast<int>(bNegative ? -Value : Value);
	}
	std::string Token()
	{
		std::string Result;
		int Character = Get();
		while (Character <= ' ' && Character != EOF)
		{
			Character = Get();
		}
		while (Character > ' ' && Character != EOF)
		{
			Result.push_back(static_cast<char>(Character));
			Character = Get();
		}
		return Result;
	}
};

class FOutput
{
	char Buffer[1 << 16];
	int Length = 0;
public:
	void Put(char Character)
	{
		if (Length == static_cast<int>(sizeof(Buffer)))
		{
			Flush();
		}
		Buffer[Length++] = Character;
	}
	void Write(long long Value, char End = '\n')
	{
		if (Value < 0)
		{
			Put('-');
			Value = -Value;
		}
		char Digits[24];
		int Count = 0;
		do
		{
			Digits[Count++] = static_cast<char>('0' + Value % 10);
			Value /= 10;
		} while (Value > 0);
		while (Count > 0)
		{
			Put(Digits[--Count]);
		}
		Put(End);
	}
	void Flush()
	{
		std::fwrite(Buffer, 1, Length, stdout);
		Length = 0;
	}
	~FOutput()
	{
		Flush();
	}
};

void PrintMerge(const std::vector<int>& a, int k, int i, int j, FOutput& Output)
{
	int Sum = a[i] + a[j];
	bool bStarted = false;
	for (int p = 0; p < static_cast<int>(a.size()); ++p)
	{
		if (p == i && Sum < k)
		{
			continue;
		}
		int Value = p == i ? 1 : (p == j ? Sum % k : a[p]);
		if (!bStarted && Value == 0)
		{
			continue;
		}
		Output.Write(Value, p + 1 == static_cast<int>(a.size()) ? '\n' : ' ');
		bStarted = true;
	}
}

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int k = Input.Read();
	std::vector<int> a(n);
	for (int& Digit : a)
	{
		Digit = Input.Read();
	}
	int i = -1;
	int Maximum = a.back();
	for (int p = n - 2; p >= 0; --p)
	{
		if (a[p] + Maximum >= k)
		{
			i = p;
			break;
		}
		Maximum = std::max(Maximum, a[p]);
	}
	int j = 1;
	if (i == -1)
	{
		i = 0;
	}
	else
	{
		j = n - 1;
		while (a[i] + a[j] < k)
		{
			--j;
		}
		int FirstOne = n;
		int LastLarge = -1;
		for (int p = 0; p < n; ++p)
		{
			if (a[p] == 1 && FirstOne == n)
			{
				FirstOne = p;
			}
			if (a[p] == k - 1)
			{
				LastLarge = p;
			}
		}
		if (FirstOne < LastLarge && LastLarge > i)
		{
			i = FirstOne;
			j = LastLarge;
		}
	}
	PrintMerge(a, k, i, j, Output);
	if (a[1] == 0)
	{
		j = n - 1;
		while (a[0] + a[j] >= k)
		{
			--j;
		}
		if (j > 1)
		{
			PrintMerge(a, k, 0, j, Output);
			return 0;
		}
	}
	i = -1;
	int Minimum = a.back();
	for (int p = n - 3; p >= 0; --p)
	{
		if (a[p] > a[p + 1] && a[p] + Minimum < k)
		{
			i = p;
		}
		Minimum = std::min(Minimum, a[p + 1]);
	}
	if (i == -1)
	{
		Minimum = a.back();
		for (int p = n - 2; p >= 0; --p)
		{
			if (a[p] + Minimum < k)
			{
				i = p;
				break;
			}
			Minimum = std::min(Minimum, a[p]);
		}
	}
	j = 1;
	if (i == -1)
	{
		i = 0;
	}
	else
	{
		j = n - 1;
		while (a[i] + a[j] >= k)
		{
			--j;
		}
	}
	PrintMerge(a, k, i, j, Output);
}
