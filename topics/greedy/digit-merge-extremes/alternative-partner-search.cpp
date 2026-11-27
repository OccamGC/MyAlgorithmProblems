// Left-position enumeration and segment tree. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdio>
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

// A merged number has at most five pieces. Start = -1 denotes one literal digit.
struct FPiece
{
	int Start;
	int Length;
	int Digit;
};
struct FCandidate
{
	std::vector<FPiece> Pieces;
	int Length = 0;
};

int main()
{
	FInput Input;
	FOutput Output;
	int n = Input.Read();
	int k = Input.Read();
	std::vector<int> Digits(n);
	for (int& Digit : Digits)
	{
		Digit = Input.Read();
	}
	std::vector<int> Nonzero(n + 1, n);
	std::vector<int> RunEnd(n);
	for (int i = n - 1; i >= 0; --i)
	{
		Nonzero[i] = Digits[i] ? i : Nonzero[i + 1];
		RunEnd[i] = i + 1 < n && Digits[i] == Digits[i + 1] ? RunEnd[i + 1] : i;
	}
	int Base = 1;
	while (Base < n)
	{
		Base *= 2;
	}
	std::vector<int> Low(2 * Base, k);
	std::vector<int> High(2 * Base, -1);
	for (int i = 0; i < n; ++i)
	{
		Low[Base + i] = High[Base + i] = Digits[i];
	}
	for (int i = Base - 1; i > 0; --i)
	{
		Low[i] = std::min(Low[2 * i], Low[2 * i + 1]);
		High[i] = std::max(High[2 * i], High[2 * i + 1]);
	}
	auto Partner = [&](auto&& Self, int Node, int l, int r, int Begin, int Bound,
		bool bCarry, bool bFirst) -> int
	{
		if (r <= Begin || (bCarry ? High[Node] < Bound : Low[Node] >= Bound))
		{
			return -1;
		}
		if (r - l == 1)
		{
			return l;
		}
		int Mid = (l + r) / 2;
		auto Visit = [&](bool bRight)
		{
			return Self(Self, 2 * Node + bRight, bRight ? Mid : l, bRight ? r : Mid,
				Begin, Bound, bCarry, bFirst);
		};
		int j = Visit(!bFirst);
		return j >= 0 ? j : Visit(bFirst);
	};
	auto Make = [&](int i, int j, bool bCarry)
	{
		FCandidate Result;
		auto Append = [&](int Start, int Length, int Digit)
		{
			if (Result.Length == 0 && Start >= 0)
			{
				int Skip = std::min(Nonzero[Start] - Start, Length);
				Start += Skip;
				Length -= Skip;
			}
			if (Length > 0 && (Result.Length || Start >= 0 || Digit))
			{
				Result.Pieces.push_back({Start, Length, Digit});
				Result.Length += Length;
			}
		};
		Append(0, i, 0);
		if (bCarry)
		{
			Append(-1, 1, 1);
		}
		Append(i + 1, j - i - 1, 0);
		Append(-1, 1, (Digits[i] + Digits[j]) % k);
		Append(j + 1, n - j - 1, 0);
		return Result;
	};
	auto Compare = [&](const FCandidate& a, const FCandidate& b)
	{
		if (a.Length != b.Length)
		{
			return a.Length - b.Length;
		}
		std::size_t i = 0;
		std::size_t j = 0;
		int x = 0;
		int y = 0;
		while (i < a.Pieces.size())
		{
			FPiece p = a.Pieces[i];
			FPiece q = b.Pieces[j];
			int Take = std::min(p.Length - x, q.Length - y);
			int Skip = 0;
			if (p.Start >= 0 && q.Start >= 0)
			{
				int u = p.Start + x;
				int v = q.Start + y;
				// At equal output length, source positions differ by at most one deletion.
				int Small = std::min(u, v);
				Skip = u == v ? Take : std::min(Take, RunEnd[Small] - Small);
			}
			if (Skip < Take)
			{
				int Left = p.Start < 0 ? p.Digit : Digits[p.Start + x + Skip];
				int Right = q.Start < 0 ? q.Digit : Digits[q.Start + y + Skip];
				if (Left != Right)
				{
					return Left - Right;
				}
				++Skip;
			}
			x += Skip;
			y += Skip;
			if (x == p.Length)
			{
				x = 0;
				++i;
			}
			if (y == q.Length)
			{
				y = 0;
				++j;
			}
		}
		return 0;
	};
	for (bool bMaximum : {true, false})
	{
		FCandidate Best;
		for (int i = 0; i + 1 < n; ++i)
		{
			for (bool bCarry : {false, true})
			{
				int j = Partner(Partner, 1, 0, Base, i + 1, k - Digits[i], bCarry, bCarry != bMaximum);
				if (j < 0)
				{
					continue;
				}
				auto Trial = Make(i, j, bCarry);
				int Order = Compare(Trial, Best);
				if (Best.Length == 0 || (bMaximum ? Order > 0 : Order < 0))
				{
					Best = std::move(Trial);
				}
			}
		}
		int Written = 0;
		for (auto Piece : Best.Pieces)
		{
			for (int j = 0; j < Piece.Length; ++j)
			{
				Output.Write(Piece.Start < 0 ? Piece.Digit : Digits[Piece.Start + j],
					++Written == Best.Length ? '\n' : ' ');
			}
		}
	}
}
