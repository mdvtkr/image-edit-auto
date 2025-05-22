from pathlib import Path
import subprocess
import json

with open('config/video.jobs.json', 'rt') as f:
    jobs = json.load(f)


def run_command(command):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command)
        
    # Print stdout and stderr
    print("--- STDOUT ---")
    print(result.stdout)
    print("--- STDERR ---")
    print(result.stderr)

    return result

# TODO create m3u8 with segment folder
#find . -type f -name "*.mp4" -print0 | xargs -0 -I{} bash -c 'ffmpeg -i "$1" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -hls_segment_filename "segments/${1%.*}_%03d.ts" -hls_base_url "segments/" -f hls "${1%.*}.m3u8"' _ {}
def edit_video(input_file, output_file, crop_filter, start, end, m3u8):
    if start or end or crop_filter:
        command = [
            "ffmpeg",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "copy"
        ]
        if start:
            command.extend(["-ss", start])
        if end:
            command.extend(["-to", end])
        if crop_filter:
            command.extend(["-vf", f'crop={crop_filter}'])
        command.append(str(output_file))
        result = run_command(command)
        if result.returncode != 0:
            print(f"Error occurred while processing {output_file}")
            return

    if m3u8:    # create m3u8 using result of previous command
        command = [
            "ffmpeg",
            "-i", str(output_file),
            "-codec:", "copy",
            "-start_number", "0",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls",
            str(output_file.with_suffix(".m3u8"))
        ]
        result = run_command(command)
        if result.returncode != 0:
            print(f"Error occurred while generating m3u8 for {output_file}")
               

for job in jobs:
    input_path = Path(job['source_path']).expanduser()

    if 'output_path' in job.keys():
        output_path = Path(job['output_path']).expanduser()
    else:
        output_path = input_path       
    output_path.mkdir(parents=True, exist_ok=True)

    input_file = input_path/job['file']
    crop_filter = job['crop'] if 'crop' in job.keys() else None
    m3u8 = job['m3u8'] if 'm3u8' in job.keys() else None

    print(f'input path: {input_path}')
    print(f'output path: {output_path}')
    print(f'input file: {input_file}')
    print(f'crop filter: {crop_filter}')
    print(f'm3u8: {m3u8}')

    if 'split' not in job.keys():
        edit_video(input_file, input_path/f'{Path(job["file"]).stem}_edited.mp4', crop_filter, None, None, m3u8)
    else:
        for split in job['split']:
            edit_video(input_file, output_path/(split['title'] + ".mp4"), crop_filter, split['time'][0], split['time'][1], m3u8)