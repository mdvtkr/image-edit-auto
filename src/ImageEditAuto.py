from pathlib import Path
import json
import shutil
import cv2
import numpy as np
import unicodedata

MANDATORY = ["path", "extensions"]
OPTIONAL = ["name",  "backup", "resize", "regions", "grayscale", "rotate", "flip", "crop"]

with open('config/jobs.json', 'rt') as f:
    jobs = json.load(f)

for job in jobs:
    def validate_key(json):
        man = [k for k in MANDATORY if k not in json.keys()]
        if len(man) > 0:
            print(f'mandatory value missing: {",".join(man)}')
            return man
        for k in OPTIONAL:
            if k not in json.keys():
                json[k] = None

    if validate_key(job):
        print(json.dumps(job, indent=2, ensure_ascii=False))
        print('this job is skipped...')
        continue

    root = Path(job['path'])
    if job['backup']:
        for i in range(1, 1000000000):
            backup = root/f'backup_{i}'
            if not backup.exists():
                break
        backup.mkdir(mode=0o754, exist_ok=True)
        
    for file in root.iterdir():
        print(str(file))
        if file.is_dir():
            print('  pass: directory')
            continue
        elif not job['name']:
            if any(v in file.suffix for v in job['extensions']):
                pass
            else:
                print(f'  pass: extension({file.suffix}) not matching')
                continue
        elif not (unicodedata.normalize('NFC', job['name']) in unicodedata.normalize('NFC', file.name) and any(v in file.suffix for v in job['extensions'])):
            print(f'  pass: name not matching')
            continue

        if job['backup']:
            shutil.copyfile(file, backup/file.name)

        im = cv2.imread(str(file.absolute()), 1)
        if job['regions']:
            for region in job['regions']:
                # create a polygons using all outer corners of the ROI
                print(f'  masking {region}')
                external_poly = np.array( [[region]], dtype=np.int32 )
                cv2.fillPoly(im, external_poly, (0,0,0) )
        
        if job['resize']:
            print(f'  resize {job["resize"]}')
            im = cv2.resize(im, (0,0), fx=job['resize'], fy=job['resize'], interpolation=cv2.INTER_LANCZOS4)

        if job['grayscale']:
            print('  grayscale')
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
        if job['crop']:
            print('   crop')
            im = im[job['crop'][1]:job['crop'][3], job['crop'][0]:job['crop'][2]]

        if job['rotate']:
            print(f'  rotate {job["rotate"]} clockwise')
            code = None
            if job['rotate'] == 90:
                code = cv2.ROTATE_90_CLOCKWISE
            elif job['rotate'] == 180:
                code = cv2.ROTATE_180
            elif job['rotate'] == 270:
                code = cv2.ROTATE_90_COUNTERCLOCKWISE
            else:
                print('    not supported degree')

            if code != None:
                im = cv2.rotate(im, code)

        if job['flip']:
            print(f'  flip {job["flip"]}')
            code = None
            if job['flip'] == 'vertical':
                code = 1
            elif job['flip'] == 'horizontal':
                code = 0
            elif job['flip'] == 'all':
                code = -1
            else:
                print('    not supported flip option')
                
            if code != None:
                im = cv2.flip(im, code)

        cv2.imwrite(str(file.absolute()), im)





    