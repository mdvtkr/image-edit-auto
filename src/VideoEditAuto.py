from pathlib import Path
import subprocess
import json

with open('config/video.jobs.json', 'rt') as f:
    jobs = json.load(f)


for job in jobs:
    input_path = Path(job['source_path']).expanduser()

    if 'output_path' in job.keys():
        output_path = Path(job['output_path']).expanduser()
    else:
        output_path = input_path       
    output_path.mkdir(parents=True, exist_ok=True)

    input_file = input_path/job['file']
    crop_filter = job['crop']

    print(f'input path: {input_path}')
    print(f'output path: {output_path}')
    print(f'input file: {input_file}')
    print(f'crop filter: {crop_filter}')

    for split in job['split']:
        output_file = output_path/(split['title'] + ".mp4")

        command = [
            "ffmpeg",
            "-i", str(input_file),
            "-vf", f'crop={crop_filter}',
            "-ss", split['time'][0],
            "-to", split['time'][1],
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "copy",
            str(output_file)
        ]

        print(f"Running: {' '.join(command)}")

        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print stdout and stderr
        print("--- STDOUT ---")
        print(result.stdout)
        print("--- STDERR ---")
        print(result.stderr)

        # Check if the command was successful
        if result.returncode != 0:
            print(f"Error occurred while processing {output_file}")