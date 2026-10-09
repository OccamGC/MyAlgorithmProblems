// Problem setter's top-edge method.
// Codex (GPT-6): portable implementation, complete degeneracy classification.

#include <algorithm>
#include <cstdlib>
#include <iostream>

struct FRectangle
{
	long long Left;
	long long Bottom;
	long long Right;
	long long Top;
};

FRectangle ReadRectangle()
{
	FRectangle Result;
	std::cin >> Result.Left >> Result.Bottom >> Result.Right >> Result.Top;
	if (Result.Left > Result.Right)
	{
		std::swap(Result.Left, Result.Right);
	}
	if (Result.Bottom > Result.Top)
	{
		std::swap(Result.Bottom, Result.Top);
	}
	return Result;
}

int Classify(FRectangle A, FRectangle B)
{
	if (A.Top < B.Top)
	{
		std::swap(A, B);
	}
	if (B.Top < A.Bottom || A.Right < B.Left || B.Right < A.Left)
	{
		return -1;
	}
	bool bPositiveX = std::max(A.Left, B.Left) < std::min(A.Right, B.Right);
	bool bPositiveY = B.Top > A.Bottom && B.Top > B.Bottom;
	return static_cast<int>(bPositiveX) + static_cast<int>(bPositiveY);
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T-- > 0)
	{
		FRectangle A = ReadRectangle();
		FRectangle B = ReadRectangle();
		int Dimension = Classify(A, B);

		const char* Names[] = {"None", "Point", "Edge", "Area"};
		std::cout << Names[Dimension + 1] << '\n';
	}
}
