# AMC Cropping Tool

Author: Nikhil Reji

Crops AMC files to descired length based on provided fps, start, and end whole seconds. Works through command line.

For asf/amc v1.1 standard.

## features:
-   Crop AMC file based on seconds.
-   Save to new parsed AMC file.
-   Thorough validation of all arguments.
-   Soft mode: Will not override existing files.
-   Command line driven.

## Dependencies:
-   [AsfAmc-Parser](https://pypi.org/project/asfamc-parser/)
-   Python 3.6 +

## Compatability
Only tested on Windows 10.

## Example

Example working directory the programm will execute in.

- Documents
  - test.amc
  - cropped
    - README.md

In an open command line in the prefered working directory:
```cmd
    python -m amccrop -i test -o testcropped -fps 30 -s 2 -e 5
```

where:
    -m  :   tells python to find installed module.
    -i  :   input amc relative filepath including filename, excluding format.
    -o  :   output amc relative file path including filename, excluding format.
    -fps    :   frame rate per second 
    -s  :   start seconds, whole integer.
    -e  :   end seconds, whole integer.