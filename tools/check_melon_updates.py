"""Compile a harness to check every incremental vertex update against fresh flow."""
import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = r'''
#include <queue>
#include <random>
#include <stdexcept>

int FreshFlow(const FMatching& State)
{
	const int Count = State.p + State.q + 2;
	const int Source = Count - 2;
	const int Sink = Count - 1;
	std::vector<std::vector<int>> Capacity(Count, std::vector<int>(Count));
	for (int u = 0; u < State.p; ++u)
	{
		Capacity[Source][u] = State.bLeftActive[u];
		for (int v : State.Edges[u])
		{
			Capacity[u][State.p + v] = 1;
		}
	}
	for (int v = 0; v < State.q; ++v)
	{
		Capacity[State.p + v][Sink] = State.bRightActive[v];
	}
	int Flow = 0;
	while (true)
	{
		std::vector<int> Parent(Count, -1);
		std::queue<int> Queue;
		Parent[Source] = Source;
		Queue.push(Source);
		while (!Queue.empty())
		{
			const int u = Queue.front();
			Queue.pop();
			for (int v = 0; v < Count; ++v)
			{
				if (Capacity[u][v] > 0 && Parent[v] == -1)
				{
					Parent[v] = u;
					Queue.push(v);
				}
			}
		}
		if (Parent[Sink] == -1)
		{
			return Flow;
		}
		for (int v = Sink; v != Source; v = Parent[v])
		{
			--Capacity[Parent[v]][v];
			++Capacity[v][Parent[v]];
		}
		++Flow;
	}
}

int main()
{
	std::mt19937 Random(2026092910);
	int Checks = 0;
	for (int Test = 0; Test < 250; ++Test)
	{
		const int p = 1 + Random() % 8;
		const int q = 1 + Random() % 8;
		std::vector<std::vector<int>> Edges(p);
		for (auto& Row : Edges)
		{
			for (int v = 0; v < q; ++v)
			{
				if (Random() % 2 && Row.size() < 4)
				{
					Row.push_back(v);
				}
			}
		}
		FMatching State(p, q, Edges);
		for (int Step = 0; Step < 200; ++Step)
		{
			if (Random() % 2)
			{
				const int u = Random() % p;
				State.ChangeLeft(u, !State.bLeftActive[u]);
			}
			else
			{
				const int v = Random() % q;
				State.ChangeRight(v, !State.bRightActive[v]);
			}
			if (State.Size != FreshFlow(State))
			{
				throw std::runtime_error("incremental size differs from fresh maximum flow");
			}
			int Actual = 0;
			for (int u = 0; u < p; ++u)
			{
				const int v = State.LeftMatch[u];
				if (v != -1)
				{
					if (!State.bLeftActive[u] || !State.bRightActive[v] || State.RightMatch[v] != u ||
						std::find(Edges[u].begin(), Edges[u].end(), v) == Edges[u].end())
					{
						throw std::runtime_error("invalid matching edge");
					}
					++Actual;
				}
			}
			if (Actual != State.Size)
			{
				throw std::runtime_error("incorrect stored size");
			}
			for (int v = 0; v < q; ++v)
			{
				const int u = State.RightMatch[v];
				if (u != -1 && State.LeftMatch[u] != v)
				{
					throw std::runtime_error("inconsistent reverse matching");
				}
			}
			++Checks;
		}
	}
	std::cout << Checks << " vertex updates matched fresh maximum flow\n";
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    implementation = (ROOT/'topics/graphs/melon-planting-2/std.cpp').read_text(encoding='utf-8')
    matching_class = implementation.split('int main()')[0]
    path = ROOT/'build/check_melon_updates.cpp'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(matching_class+HARNESS, encoding='utf-8', newline='\n')
    executable = path.with_suffix('.exe' if os.name == 'nt' else '')
    subprocess.run([args.compiler, '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic',
                    str(path), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)


if __name__ == '__main__':
    main()
