// Codex (GPT-6): Hopcroft partition refinement for obstacle-trace equivalence.
// The absorbing obstacle is a separate rejecting state.
#include <algorithm>
#include <numeric>
#include <vector>
#include "buffered-input.hpp"

int main()
{
	FInput Input;
	int n = Input.Read();
	int k = Input.Read();
	int States = n + 1;
	std::vector<int> Head(States * k, -1);
	std::vector<int> Next(States * k);
	for (int u = 0; u <= n; ++u)
	{
		for (int Letter = 0; Letter < k; ++Letter)
		{
			int v = u == 0 ? 0 : Input.Read();
			int Edge = u * k + Letter;
			int Key = v * k + Letter;
			Next[Edge] = Head[Key];
			Head[Key] = Edge;
		}
	}
	std::vector<int> Order(States);
	std::iota(Order.begin(), Order.end(), 0);
	std::vector<int> Position = Order;
	std::vector<int> Block(States, 1);
	Block[0] = 0;
	std::vector<int> Left(States + 1);
	std::vector<int> Right(States + 1);
	std::vector<int> Count(States + 1);
	Left[0] = 0;
	Right[0] = 1;
	Left[1] = 1;
	Right[1] = States;
	int Blocks = 2;
	std::vector<int> Queue(1, 0);
	std::vector<int> Snapshot;
	std::vector<int> Touched;
	for (std::size_t At = 0; At < Queue.size(); ++At)
	{
		int Splitter = Queue[At];
		Snapshot.assign(Order.begin() + Left[Splitter], Order.begin() + Right[Splitter]);
		for (int Letter = 0; Letter < k; ++Letter)
		{
			Touched.clear();
			for (int v : Snapshot)
			{
				for (int Edge = Head[v * k + Letter]; Edge != -1; Edge = Next[Edge])
				{
					int u = Edge / k;
					int b = Block[u];
					if (Count[b] == 0)
					{
						Touched.push_back(b);
					}
					int Destination = Left[b] + Count[b]++;
					int Other = Order[Destination];
					std::swap(Order[Position[u]], Order[Destination]);
					Position[Other] = Position[u];
					Position[u] = Destination;
				}
			}
			for (int b : Touched)
			{
				int Size = Right[b] - Left[b];
				int Marked = Count[b];
				Count[b] = 0;
				if (Marked == Size)
				{
					continue;
				}
				int Added = Blocks++;
				// Keep the larger half's identity, always queue the new smaller half.
				if (Marked <= Size - Marked)
				{
					Left[Added] = Left[b];
					Right[Added] = Left[b] + Marked;
					Left[b] += Marked;
				}
				else
				{
					Left[Added] = Left[b] + Marked;
					Right[Added] = Right[b];
					Right[b] = Left[Added];
				}
				for (int i = Left[Added]; i < Right[Added]; ++i)
				{
					Block[Order[i]] = Added;
				}
				Queue.push_back(Added);
			}
		}
	}
	std::printf("%d\n", Blocks - 1);
}
