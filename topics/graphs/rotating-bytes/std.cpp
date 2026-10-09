// Problem setter's reverse character BFS, stable binary partition and ordered predecessor edges. Codex (GPT-6): proof, dynamically sized storage and portable implementation.

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

struct FChunk
{
	std::array<char, 5> Text{};
	unsigned char Length = 0;
	unsigned char Position = 0;
	bool bStart = false;
	bool bSeen = false;
	int From = 0;
};

struct FEdge
{
	int Destination;
	int Next;
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int m = Input.Read();
	int k = Input.Read();
	std::vector<FChunk> Chunks(n + m + 1);
	auto ReadChunk = [&](int Index)
	{
		std::string Text = Input.Token();
		Chunks[Index].Length = static_cast<unsigned char>(Text.size());
		std::copy(Text.begin(), Text.end(), Chunks[Index].Text.begin());
	};
	for (int u = 1; u <= n; ++u)
	{
		ReadChunk(u);
	}
	for (int i = 0; i < k; ++i)
	{
		Chunks[Input.Read()].bStart = true;
	}
	std::vector<int> Head(n + m + 1, -1);
	std::vector<FEdge> Edges;
	Edges.reserve(2 * m);
	auto Add = [&](int u, int v)
	{
		Edges.push_back({v, Head[u]});
		Head[u] = static_cast<int>(Edges.size()) - 1;
	};
	{
		std::vector<int> BySource(n + 1, -1);
		std::vector<int> Next(m);
		std::vector<int> Destination(m);
		for (int e = 0; e < m; ++e)
		{
			int u = Input.Read();
			Destination[e] = Input.Read();
			Next[e] = BySource[u];
			BySource[u] = e;
			ReadChunk(n + e + 1);
		}
		for (int u = n; u >= 1; --u)
		{
			for (int e = BySource[u]; e != -1; e = Next[e])
			{
				Add(Destination[e], n + e + 1);
				Add(n + e + 1, u);
			}
		}
	}
	std::array<std::array<std::vector<int>, 2>, 2> Queues;
	auto Push = [&](int Layer, int u)
	{
		FChunk& Chunk = Chunks[u];
		int Bit = Chunk.Text[Chunk.Length - Chunk.Position - 1] - '0';
		Queues[Layer][Bit].push_back(u);
		Chunk.bSeen = true;
	};
	int Layer = 0;
	Push(Layer, 1);
	while (!Queues[Layer][0].empty() || !Queues[Layer][1].empty())
	{
		for (int Bit = 0; Bit < 2; ++Bit)
		{
			for (int u : Queues[Layer][Bit])
			{
				FChunk& Chunk = Chunks[u];
				if (++Chunk.Position < Chunk.Length)
				{
					Push(Layer ^ 1, u);
				}
				else if (Chunk.bStart)
				{
					for (int v = u; v != 0; v = Chunks[v].From)
					{
						for (int j = 0; j < Chunks[v].Length; ++j)
						{
							Output.Put(Chunks[v].Text[j]);
							}
					}
					Output.Put('\n');
					for (int v = u; v != 0; v = Chunks[v].From)
					{
						if (v <= n)
						{
							Output.Write(v, v == 1 ? '\n' : ' ');
						}
					}
					return 0;
				}
				else
				{
					for (int e = Head[u]; e != -1; e = Edges[e].Next)
					{
						int v = Edges[e].Destination;
						if (!Chunks[v].bSeen)
						{
							Chunks[v].From = u;
							Push(Layer ^ 1, v);
						}
					}
				}
			}
			Queues[Layer][Bit].clear();
		}
		Layer ^= 1;
	}
}
