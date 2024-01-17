# Simple image manipulation
supports resizing, masking and make it grayscale

# How to use
describe the jobs in `config/jobs.json` file

this file can contain multiple jobs and they are processed in the order specified by the JSON array

### jobs.json
#### keys
- `path`: (mandatory) directory containing image files.
- `name`: (optional) substring of file name. if it's null, then it means all file in `path`
- `extensions`: (mandatory) image extensions to be processed. multiple extensions can be specified.
- `backup`: (optional) backup original file. `true` or `false`
- `resize`: (optional) resize ratio. a floating point real number.
- `regions`: (optional) masking regions. multiple regions can be specified.
- `grayscale`: (optional) change image color to grayscale. `true` or `false`
- `rotate`: (optional) rotate image clockwise `90`, `180` or `270` degree.
- `flip`: (optional) flip image. `horizontal`(x axis), `vertical`(y axis) or `all`(x and y axises)

```json
// example of jobs.json
[
    {
        "path": "/home/mypath/images/",
        "name": "image-",
        "extensions": ["jpg"],
        "backup": true,
        "resize": null,
        "regions": [[[0,0], [10,0], [10,10], [0,10]]],
        "grayscale": true,
        "rotate": 90,
        "flip": "vertical"
    }
]
```