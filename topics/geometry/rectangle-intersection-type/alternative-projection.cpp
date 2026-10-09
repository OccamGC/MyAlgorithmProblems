// Methods in the setter's teaching notes: interval projections / center distances.
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
	long long Left = std::max(A.Left, B.Left);
	long long Right = std::min(A.Right, B.Right);
	long long Bottom = std::max(A.Bottom, B.Bottom);
	long long Top = std::min(A.Top, B.Top);
	if (Left > Right || Bottom > Top)
	{
		return -1;
	}
	return static_cast<int>(Left < Right) + static_cast<int>(Bottom < Top);
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
