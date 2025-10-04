# csv-vod-slicer
CLI extension for Auto-Editor that converts CSVs to editor ready EDL timelines.

For more info on Auto-Editor, see https://github.com/WyattBlue/auto-editor

## Linux (Ubuntu)
### Setup
#### Make a directory for task automation scripts and utlities.
```
mkdir Utility && cd Utility
```

#### Make a virtual environment to keep things clean (and avoid OS conflicts)
```
python3 -m venv env
```

#### Activate the virtual environment
```
source env/bin/activate
```

#### Install Auto-Editor
```
python3 -m pip install auto-editor
```

#### Clone this repo
```
git clone https://github.com/trackpantsu/csv-vod-slicer.git && cd csv-vod-slicer

```

### Runbook
#### Slice a VOD:
```
python3 ./csv-vod-slicer.py -c 00-00-00-EDL.csv -i 00-00-00.mp4 -0 00-00-00 -r 60
```
This will create a 60 FPS Resolve Timeline for each EDL category listed in the CSV as well as a VOD timeline that aggregates all categories (except for X, which is reserved as an exclusion catergory for mishaps).

Example output:
```
00-00-00-A
00-00-00-B
00-00-00-C
00-00-00-vod
```
Required Arguments:

`-c` - path to CSV with edit instructions

`-i` - path to source video file

`-o` - filename prefix for generated edits, EDL label characters and extensions will be appended to output

`-r` - the framerate needs to be accurate to properly time the frame cuts from auto-editor. double check this value if cuts are out of sync


#### Export Options: `-h`
defaults to `resolve`, but also supports `final-cut-pro`,`shotcut`,`clip-sequence`
```
python3 ./csv-vod-slicer.py -c 00-00-00-EDL.csv -i 00-00-00.mp4 -0 00-00-00 -r 60 -e shotcut
```

#### Focus Mode: `-f`
ignore all EDL label character codes that are not THIS value, helpful when fixing CSVs after edits have been generated.
```
python3 ./csv-vod-slicer.py -c 00-00-00-EDL.csv -i 00-00-00.mp4 -0 00-00-00 -r 60 -f B
```
Expected output is `00-00-00-B` only

#### List all options: `-h`
```
python3 ./csv-vod-slicer.py -h
```
