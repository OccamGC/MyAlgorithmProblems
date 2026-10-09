// Problem setter's roots-of-unity reduction.
// Codex (GPT-6): ordered Vandermonde products via product trees and multipoint evaluation.
#include <iostream>
#include <vector>
#include "polynomial.hpp"

constexpr FInteger Modulus = 1004535809;
constexpr FInteger Root = 3;
using FArithmetic = FPolynomialArithmetic<Modulus, Root>;
using FSeries = std::vector<FInteger>;

struct FProductTree
{
	const FSeries& Points;
	std::vector<FSeries> Products;

	explicit FProductTree(const FSeries& InPoints) : Points(InPoints), Products(4 * InPoints.size())
	{
		Build(1, 0, static_cast<int>(Points.size()));
	}

	void Build(int Node, int Begin, int End)
	{
		if (End - Begin == 1)
		{
			Products[Node] = {(Modulus - Points[Begin]) % Modulus, 1};
			return;
		}
		int Middle = (Begin + End) / 2;
		Build(2 * Node, Begin, Middle);
		Build(2 * Node + 1, Middle, End);
		Products[Node] = FArithmetic::Multiply(Products[2 * Node], Products[2 * Node + 1], End - Begin + 1);
	}

	FInteger EvaluateProduct(const FSeries& Polynomial, int Node, int Begin, int End) const
	{
		if (End - Begin == 1)
		{
			FInteger Result = 0;
			for (int i = static_cast<int>(Polynomial.size()) - 1; i >= 0; --i)
			{
				Result = (Result * Points[Begin] + Polynomial[i]) % Modulus;
			}
			return Result;
		}
		FSeries Reduced = FArithmetic::Remainder(Polynomial, Products[Node]);
		int Middle = (Begin + End) / 2;
		return EvaluateProduct(Reduced, 2 * Node, Begin, Middle)
			* EvaluateProduct(Reduced, 2 * Node + 1, Middle, End) % Modulus;
	}

	FInteger Vandermonde(int Node, int Begin, int End) const
	{
		if (End - Begin == 1)
		{
			return 1;
		}
		int Middle = (Begin + End) / 2;
		FInteger Left = Vandermonde(2 * Node, Begin, Middle);
		FInteger Right = Vandermonde(2 * Node + 1, Middle, End);
		if (Left == 0 || Right == 0)
		{
			return 0;
		}
		FInteger Cross = EvaluateProduct(Products[2 * Node], 2 * Node + 1, Middle, End);
		return Left * Right % Modulus * Cross % Modulus;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int k;
	std::cin >> k;
	int n = 1 << k;
	std::vector<FSeries> a(n, FSeries(n));
	for (FSeries& Polynomial : a)
	{
		for (FInteger& Coefficient : Polynomial)
		{
			std::cin >> Coefficient;
		}
		Transform(Polynomial, false, Modulus, Root);
	}
	FSeries Result(n);
	FSeries Points(n);
	for (int t = 0; t < n; ++t)
	{
		for (int i = 0; i < n; ++i)
		{
			Points[i] = a[i][t];
		}
		FProductTree Tree(Points);
		Result[t] = Tree.Vandermonde(1, 0, n);
	}
	Transform(Result, true, Modulus, Root);
	for (int i = 0; i < n; ++i)
	{
		std::cout << Result[i] << (i + 1 == n ? '\n' : ' ');
	}
}
