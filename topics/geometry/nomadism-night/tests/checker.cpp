#include "../mst.hpp"

#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
	if (argc != 4)
	{
		std::cerr << "Usage: checker input reference contestant\n";
		return 2;
	}
	std::ifstream Input(argv[1]);
	std::ifstream Reference(argv[2]);
	std::ifstream Contestant(argv[3]);
	if (!Input || !Reference || !Contestant)
	{
		return 2;
	}
	int n;
	if (!(Input >> n) || n < 1 || n > 400000)
	{
		return 2;
	}
	std::vector<FPoint> Points(n);
	for (int i = 0; i < n; ++i)
	{
		if (!(Input >> Points[i].x >> Points[i].y)
			|| Points[i].x < -10000 || Points[i].x > 10000
			|| Points[i].y < -10000 || Points[i].y > 10000)
		{
			return 2;
		}
		Points[i].Id = i;
	}
	std::string Extra;
	if (Input >> Extra)
	{
		return 2;
	}
	std::vector<bool> Visited(n, false);
	int Previous = -1;
	std::int64_t Cost = 0;
	for (int i = 0; i <= n; ++i)
	{
		int Vertex;
		if (!(Contestant >> Vertex) || Vertex < 1 || Vertex > n)
		{
			return 1;
		}
		--Vertex;
		if ((i == 0 || i == n) && Vertex != 0)
		{
			return 1;
		}
		if (i < n)
		{
			if (Visited[Vertex])
			{
				return 1;
			}
			Visited[Vertex] = true;
		}
		if (Previous != -1)
		{
			Cost += Distance(Points[Previous], Points[Vertex]);
		}
		Previous = Vertex;
	}
	if (Contestant >> Extra)
	{
		return 1;
	}
	try
	{
		// The baseline is recomputed from the input. The reference file contains
		// a tour, never an assumed optimum or a length read from its first token.
		const std::int64_t M = BuildMinimumSpanningTree(Points).Weight;
		if (1000 * Cost > 2001 * M + 1)
		{
			std::cerr << "Tour exceeds 2.001 M + 0.001\n";
			return 1;
		}
	}
	catch (const std::exception& Error)
	{
		std::cerr << Error.what() << '\n';
		return 2;
	}
	return 0;
}
