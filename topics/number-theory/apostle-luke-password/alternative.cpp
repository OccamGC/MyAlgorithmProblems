// Codex (GPT-6): sieve prime divisors, then sieve the arithmetic progression by modular inverses.
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>
using Integer = long long;

Integer Inverse(Integer a, Integer Mod)
{
	Integer b = Mod;
	Integer x = 1;
	Integer y = 0;
	while (b)
	{
		Integer Quotient = a / b;
		Integer Next = a - Quotient * b;
		a = b;
		b = Next;
		Next = x - Quotient * y;
		x = y;
		y = Next;
	}
	return (x % Mod + Mod) % Mod;
}

int main()
{
	int N;
	Integer G;
	Integer k;
	Integer b;
	std::cin >> N >> G >> k >> b;
	Integer First = k * G + b;
	Integer Maximum = First + k * (N - 1);
	Integer Limit = static_cast<Integer>(std::sqrt(static_cast<long double>(Maximum)));
	while ((Limit + 1) * (Limit + 1) <= Maximum)
	{
		++Limit;
	}
	while (Limit * Limit > Maximum)
	{
		--Limit;
	}
	std::vector<bool> Sieve(Limit + 1, true);
	std::vector<bool> Composite(N);
	for (Integer q = 2; q <= Limit; ++q)
	{
		if (!Sieve[q])
		{
			continue;
		}
		for (Integer Multiple = q * q; Multiple <= Limit; Multiple += q)
		{
			Sieve[Multiple] = false;
		}
		if (k % q == 0)
		{
			if (First % q == 0)
			{
				for (int i = 0; i < N; ++i)
				{
					if (First + i * k != q)
					{
						Composite[i] = true;
					}
				}
			}
		}
		else
		{
			Integer Start = (q - First % q) % q * Inverse(k % q, q) % q;
			for (Integer i = Start; i < N; i += q)
			{
				if (First + i * k != q)
				{
					Composite[i] = true;
				}
			}
		}
	}
	int Answer = 0;
	for (int i = 0; i < N; ++i)
	{
		Integer Value = First + i * k;
		Answer += Value == 1 || (Value >= 2 && !Composite[i]);
		std::cout << Answer << '\n';
	}
}
