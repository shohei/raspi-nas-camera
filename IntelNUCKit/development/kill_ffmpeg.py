import commands,os

def kill_ffmpeg():
    _, output = commands.getstatusoutput("ps aux | grep -E 'ffmpeg' | awk '{print $2}'")
    pids = output.split('\n')
    for pid in pids:
        cmd = "sudo kill -9 "+pid
        print(cmd)
        os.system(cmd)

kill_ffmpeg()
