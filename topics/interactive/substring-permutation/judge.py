"""Portable local interactor. Hidden input: n, then the hidden permutation.

Run: python judge.py --input hidden.in --program ./std [--transcript trace.json]
The solver receives only n and answers to its queries. Wall time includes pipe
communication and this Python judge. On Windows, also records solver peak memory.
"""
import argparse,ctypes,json,os,queue,subprocess,threading,time
from pathlib import Path

def read_hidden(text):
    a=list(map(int,text.split()))
    if not a or not 1<=a[0]<=120 or len(a)!=a[0]+1 or set(a[1:])!=set(range(1,a[0]+1)):
        raise ValueError('invalid hidden permutation')
    return a[1:]

def lcs_length(hidden,query_values):
    position={v:i for i,v in enumerate(hidden)};previous=-2;run=best=0
    for v in query_values:
        current=position[v];run=run+1 if current==previous+1 else 1
        previous=current;best=max(best,run)
    return best

def peak_memory(process):
    if os.name!='nt':return None
    class Counters(ctypes.Structure):
        _fields_=[('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)]+[(name,ctypes.c_size_t) for name in ['peak','working','paged_peak','paged','nonpaged_peak','nonpaged','pagefile','pagefile_peak','private']]
    value=Counters();value.cb=ctypes.sizeof(value)
    if not ctypes.windll.psapi.GetProcessMemoryInfo(int(process._handle),ctypes.byref(value),value.cb):raise ctypes.WinError()
    return value.peak

def run(program,hidden,timeout=30):
    read_hidden(str(len(hidden))+'\n'+' '.join(map(str,hidden)))
    start=time.perf_counter();deadline=start+timeout;lines=queue.Queue();trace=[];count=0
    with subprocess.Popen([str(Path(program).resolve())],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='ascii',bufsize=1) as process:
        def reader():
            try:
                while True:
                    line=process.stdout.readline(4097)
                    lines.put(line)
                    if not line or len(line)>4096:break
            except Exception as error:lines.put(error)
        thread=threading.Thread(target=reader,daemon=True);thread.start()
        try:
            process.stdin.write(str(len(hidden))+'\n');process.stdin.flush()
            while True:
                remaining=deadline-time.perf_counter()
                if remaining<=0:raise ValueError('interaction timed out')
                try:line=lines.get(timeout=remaining)
                except queue.Empty as error:raise ValueError('interaction timed out; flush each query') from error
                if not isinstance(line,str) or not line or len(line)>4096:raise ValueError('missing or oversized protocol line')
                tokens=line.split()
                if not tokens:raise ValueError('empty protocol line')
                if tokens[0]=='?':
                    numbers=list(map(int,tokens[1:]))
                    if len(numbers)<2 or not 1<=numbers[0]<=100 or len(numbers)!=numbers[0]+1 or any(not 1<=v<=len(hidden) for v in numbers[1:]):raise ValueError('invalid query')
                    count+=1
                    if count>800:raise ValueError('too many queries')
                    reply=lcs_length(hidden,numbers[1:]);trace.append({'query':numbers[1:],'reply':reply})
                    process.stdin.write(str(reply)+'\n');process.stdin.flush()
                elif tokens[0]=='!':
                    if list(map(int,tokens[1:]))!=hidden:raise ValueError('wrong final permutation')
                    process.stdin.close()
                    process.wait(timeout=max(.01,deadline-time.perf_counter()))
                    thread.join(timeout=max(.01,deadline-time.perf_counter()))
                    if thread.is_alive() or process.returncode!=0:raise ValueError('solver failed to exit successfully')
                    while not lines.empty():
                        extra=lines.get_nowait()
                        if not isinstance(extra,str) or extra.strip():raise ValueError('extra output after final answer')
                    return {'queries':count,'seconds':time.perf_counter()-start,'peak_working_set_bytes':peak_memory(process),'trace':trace,'answer':hidden}
                else:raise ValueError('expected ? or !')
        finally:
            if process.poll() is None:process.kill();process.wait()
            thread.join(timeout=1)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--program',type=Path,required=True)
    parser.add_argument('--transcript',type=Path);parser.add_argument('--timeout',type=float,default=30)
    args=parser.parse_args()
    try:result=run(args.program,read_hidden(args.input.read_text('utf-8')),args.timeout)
    except (ValueError,OSError,subprocess.TimeoutExpired) as error:parser.exit(1,str(error)+'\n')
    if args.transcript:args.transcript.write_text(json.dumps(result,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['trace','answer']}))
if __name__=='__main__':main()
