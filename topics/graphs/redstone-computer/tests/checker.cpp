#include <fstream>
#include <iostream>
#include <string>
#include <vector>

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
	int m;
	int k;
	if (!(Input >> n >> m >> k))
	{
		return 2;
	}
	std::string Token;
	const bool bImpossible = (Reference >> Token) && Token == "No";
	if (bImpossible)
	{
		if (!(Contestant >> Token) || Token != "No" || (Contestant >> Token))
		{
			return 1;
		}
		return 0;
	}
	std::vector<std::string> Values(n);
	for (std::string& Value : Values)
	{
		if (!(Contestant >> Value) || static_cast<int>(Value.size()) != k || Value.find_first_not_of("01") != std::string::npos)
		{
			return 1;
		}
	}
	if (Contestant >> Token)
	{
		return 1;
	}
	for (int i = 0; i < m; ++i)
	{
		int a;
		int b;
		char Operation;
		std::string Result;
		if (!(Input >> a >> Operation >> b >> Result))
		{
			return 2;
		}
		for (int j = 0; j < k; ++j)
		{
			const int s = Values[a - 1][j] - '0';
			const int t = Values[b - 1][j] - '0';
			const int Actual = Operation == '^' ? (s ^ t) : Operation == '&' ? (s & t) : (s | t);
			if (Actual != Result[j] - '0')
			{
				return 1;
			}
		}
	}
	return 0;
}
