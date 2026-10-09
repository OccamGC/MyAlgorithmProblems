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

int AxisDimension(long long LeftA, long long RightA, long long LeftB, long long RightB)
{
	long long WidthA = RightA - LeftA;
	long long WidthB = RightB - LeftB;
	long long TwiceCenterDistance = std::abs(LeftA + RightA - LeftB - RightB);
	long long WidthSum = WidthA + WidthB;
	if (TwiceCenterDistance > WidthSum)
	{
		return -1;
	}
	return WidthA > 0 && WidthB > 0 && TwiceCenterDistance < WidthSum ? 1 : 0;
}

int Classify(FRectangle A, FRectangle B)
{
	int X = AxisDimension(A.Left, A.Right, B.Left, B.Right);
	int Y = AxisDimension(A.Bottom, A.Top, B.Bottom, B.Top);
	return X < 0 || Y < 0 ? -1 : X + Y;
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
