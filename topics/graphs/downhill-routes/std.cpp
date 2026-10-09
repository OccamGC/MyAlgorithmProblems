#include <algorithm>
#include <array>
#include <cstdio>
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
		int Value = 0;
		while (Character >= '0' && Character <= '9')
		{
			Value = Value * 10 + Character - '0';
			Character = Get();
		}
		return bNegative ? -Value : Value;
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

constexpr int Modulus = 998246353;

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	std::vector<int> Height(n);
	std::vector<int> InDegree(n);
	std::vector<int> Ways(n, 1);
	std::vector<std::vector<int>> Edges(n);
	for (int& Value : Height)
	{
		Value = Input.Read();
	}
	for (int i = 0; i < m; ++i)
	{
		int u = Input.Read() - 1;
		int v = Input.Read() - 1;
		if (Height[u] < Height[v])
		{
			std::swap(u, v);
		}
		if (Height[u] > Height[v])
		{
			Edges[u].push_back(v);
			++InDegree[v];
		}
	}
	std::vector<int> Queue;
	Queue.reserve(n);
	for (int i = 0; i < n; ++i)
	{
		if (InDegree[i] == 0)
		{
			Queue.push_back(i);
		}
	}
	for (std::size_t Index = 0; Index < Queue.size(); ++Index)
	{
		int u = Queue[Index];
		for (int v : Edges[u])
		{
			Ways[v] += Ways[u];
			if (Ways[v] >= Modulus)
			{
				Ways[v] -= Modulus;
			}
			if (--InDegree[v] == 0)
			{
				Queue.push_back(v);
			}
		}
	}
	int Answer = 0;
	for (int Value : Ways)
	{
		Answer += Value;
		if (Answer >= Modulus)
		{
			Answer -= Modulus;
		}
	}
	Output.Write(Answer);
}
