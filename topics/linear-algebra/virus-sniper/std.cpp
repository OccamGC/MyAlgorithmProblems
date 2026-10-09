#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using FValue = std::int64_t;
using FPolynomial = std::vector<FValue>;
using FMatrix = std::vector<FPolynomial>;
constexpr FValue Mod = 1000000009;

FValue Power(FValue Base, FValue Exponent)
{
	FValue Result = 1;
	while (Exponent > 0)
	{
		if (Exponent % 2 != 0)
		{
			Result = Result * Base % Mod;
		}
		Base = Base * Base % Mod;
		Exponent /= 2;
	}
	return Result;
}

FMatrix Multiply(const FMatrix& Left, const FMatrix& Right)
{
	int d = static_cast<int>(Left.size());
	FMatrix Result(d, FPolynomial(d, 0));
	for (int i = 0; i < d; ++i)
	{
		for (int k = 0; k < d; ++k)
		{
			for (int j = 0; j < d; ++j)
			{
				Result[i][j] = (Result[i][j] + Left[i][k] * Right[k][j]) % Mod;
			}
		}
	}
	return Result;
}

FPolynomial MultiplyPolynomial(const FPolynomial& Left, const FPolynomial& Right,
	const FPolynomial& Reduction)
{
	int d = static_cast<int>(Left.size());
	FPolynomial Product(2 * d - 1, 0);
	for (int i = 0; i < d; ++i)
	{
		for (int j = 0; j < d; ++j)
		{
			Product[i + j] = (Product[i + j] + Left[i] * Right[j]) % Mod;
		}
	}
	for (int i = 2 * d - 2; i >= d; --i)
	{
		for (int j = 0; j < d; ++j)
		{
			Product[i - d + j] = (Product[i - d + j] + Product[i] * Reduction[j]) % Mod;
		}
	}
	Product.resize(d);
	return Product;
}

std::vector<int> BinaryDigits(std::string Decimal)
{
	std::vector<int> Bits;
	while (!Decimal.empty())
	{
		int Carry = 0;
		std::string Quotient;
		for (char Digit : Decimal)
		{
			int Value = Carry * 10 + Digit - '0';
			if (!Quotient.empty() || Value / 2 != 0)
			{
				Quotient.push_back(static_cast<char>('0' + Value / 2));
			}
			Carry = Value % 2;
		}
		Bits.push_back(Carry);
		Decimal = Quotient;
	}
	return Bits;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int A;
	int B;
	int N;
	int M;
	int Q;
	int K;
	std::cin >> A >> B >> N >> M >> Q >> K;
	std::vector<FPolynomial> Initial(A + 2, FPolynomial(B + 2, 0));
	for (int i = 0; i < Q; ++i)
	{
		int x1;
		int y1;
		int x2;
		int y2;
		FValue C;
		std::cin >> x1 >> y1 >> x2 >> y2 >> C;
		Initial[x1][y1] += C;
		Initial[x2 + 1][y1] -= C;
		Initial[x1][y2 + 1] -= C;
		Initial[x2 + 1][y2 + 1] += C;
	}
	for (int x = 1; x <= A; ++x)
	{
		for (int y = 1; y <= B; ++y)
		{
			Initial[x][y] += Initial[x - 1][y] + Initial[x][y - 1] - Initial[x - 1][y - 1];
		}
	}
	int d = N * M;
	FMatrix Transition(d, FPolynomial(d, 0));
	const std::array<int, 5> dx = {0, -1, 1, 0, 0};
	const std::array<int, 5> dy = {0, 0, 0, -1, 1};
	for (int i = 0; i < d; ++i)
	{
		Transition[i][i] = 1;
		for (int j = 0; j < 5; ++j)
		{
			FValue a;
			FValue b;
			std::cin >> a >> b;
			int x = i / M + dx[j];
			int y = i % M + dy[j];
			if (0 <= x && x < N && 0 <= y && y < M)
			{
				int Target = x * M + y;
				Transition[i][Target] = (Transition[i][Target] + a * Power(b, Mod - 2)) % Mod;
			}
		}
	}
	FMatrix Identity(d, FPolynomial(d, 0));
	for (int i = 0; i < d; ++i)
	{
		Identity[i][i] = 1;
	}
	std::vector<FMatrix> Powers = {Identity};
	FPolynomial Trace(d + 1, 0);
	for (int k = 1; k <= d; ++k)
	{
		Powers.push_back(Multiply(Powers.back(), Transition));
		for (int i = 0; i < d; ++i)
		{
			Trace[k] = (Trace[k] + Powers.back()[i][i]) % Mod;
		}
	}
	// Characteristic polynomial: x^d + Coefficient[1] x^(d-1) + ... .
	FPolynomial Coefficient(d + 1, 0);
	Coefficient[0] = 1;
	for (int k = 1; k <= d; ++k)
	{
		FValue Sum = 0;
		for (int j = 1; j <= k; ++j)
		{
			Sum = (Sum + Coefficient[k - j] * Trace[j]) % Mod;
		}
		Coefficient[k] = (Mod - Sum) * Power(k, Mod - 2) % Mod;
	}
	FPolynomial Reduction(d, 0);
	for (int j = 0; j < d; ++j)
	{
		Reduction[j] = (Mod - Coefficient[d - j]) % Mod;
	}
	FPolynomial x(d, 0);
	if (d == 1)
	{
		x[0] = Reduction[0];
	}
	else
	{
		x[1] = 1;
	}
	std::vector<FPolynomial> BinaryPowers = {x};
	int OriginX = 1;
	int OriginY = 1;
	for (int Query = 0; Query < K; ++Query)
	{
		std::string T;
		std::cin >> T;
		std::vector<int> Bits = BinaryDigits(T);
		while (BinaryPowers.size() < Bits.size())
		{
			BinaryPowers.push_back(MultiplyPolynomial(BinaryPowers.back(), BinaryPowers.back(), Reduction));
		}
		FPolynomial Remainder(d, 0);
		Remainder[0] = 1;
		for (std::size_t i = 0; i < Bits.size(); ++i)
		{
			if (Bits[i] != 0)
			{
				Remainder = MultiplyPolynomial(Remainder, BinaryPowers[i], Reduction);
			}
		}
		FPolynomial Answer(d, 0);
		for (int i = 0; i < d; ++i)
		{
			FValue Value = Initial[OriginX + i / M][OriginY + i % M] % Mod;
			for (int k = 0; k < d; ++k)
			{
				FValue Weight = Value * Remainder[k] % Mod;
				for (int j = 0; j < d; ++j)
				{
					Answer[j] = (Answer[j] + Weight * Powers[k][i][j]) % Mod;
				}
			}
		}
		FValue Sum = 0;
		for (int j = 0; j < d; ++j)
		{
			std::cout << Answer[j] << (j + 1 == d ? '\n' : ' ');
			Sum += Answer[j];
		}
		OriginX = static_cast<int>(Sum % (A - N + 1)) + 1;
		OriginY = static_cast<int>(Sum * 7 % (B - M + 1)) + 1;
	}
}
