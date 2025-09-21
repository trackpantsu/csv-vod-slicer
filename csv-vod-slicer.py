#
# CLI extension for auto-editor that converts CSVs to editor ready EDL timelines
# Requires Auto-Editor - https://github.com/WyattBlue/auto-editor
#
import csv
import argparse
import pathlib
import subprocess

parser = argparse.ArgumentParser(
    prog="trackpantsu/csv-vod-slicer",
    description="CSV/EDL interface for Auto-Editor",
    #    epilog="TBD",
)
parser.add_argument(
    "-c",
    "--csv",
    type=pathlib.Path,
    required=True,
    help="path to CSV with edit instructions, see --style if extending or adapting this script to another EDL format",
)
parser.add_argument(
    "-i", "--input", required=True, type=pathlib.Path, help="path to source video file"
)
parser.add_argument(
    "-o",
    "--output",
    required=True,
    help="filename prefix for generated edits, EDL label characters and extensions will be appended to output",
)
parser.add_argument(
    "-r",
    "--rate",
    required=True,
    help="the framerate needs to be accurate to properly time the frame cuts from auto-editor. double check this value if cuts are out of sync",
)
parser.add_argument(
    "-e",
    "--export",
    default="resolve",
    choices=["resolve", "final-cut-pro", "shotcut", "clip-sequence"],
    help="video editing platform that will be used to process generated edits",
)
parser.add_argument(
    "-s",
    "--style",
    default="TEDL",
    help="specify CSV header format for edit instructions, any non-default value will use first row as headers until additional formats are added",
)
parser.add_argument(
    "-f",
    "--focus",
    default="none",
    type=str,
    help="ignore all EDL label character codes that are not THIS value, helpful when fixing CSVs after edits have been generated",
)

args = parser.parse_args()

csv_path = args.csv
input_path = args.input
output_path = args.output
export_format = args.export
edl_style = args.style
focus = args.focus
input_rate = args.rate

if edl_style == "TEDL":
    edl = [
        "StartH",
        "StartM",
        "StartS",
        "EndH",
        "EndM",
        "EndS",
        "TCStart",
        "TCEnd",
        "Comment",
        "Label",
        "TCDuration",
        "FrameStart",
        "FrameEnd",
    ]

else:  # add more formats here if needed
    edl = None  # when fieldnames are None, the first row of the CSV become fieldnames

splits = []
ordlist = []
vodlist = []

with open(csv_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=edl)
    if focus == "none":
        for row in reader:
            label = row.get("Label", "Z")
            if len(row.get("Label", "Z")) == 0:
                label = "Z"
            if ord(label) in range(65, 88):
                splits.append((row["Label"], (row["FrameStart"], row["FrameEnd"])))
                ordlist.append(ord(row["Label"]))
            if not row.get("Label", "Z") == "X":
                vodlist.append((row["Label"], (row["FrameStart"], row["FrameEnd"])))
    else:
        for row in reader:
            label = row.get("Label", "Z")
            if len(row.get("Label", "Z")) == 0:
                label = "Z"
            if ord(label) == ord(focus):
                splits.append((row["Label"], (row["FrameStart"], row["FrameEnd"])))
                ordlist.append(ord(row["Label"]))
# build command string
# "0,f1" " " "f2,f3"
cmd = " ".join(
    [
        "auto-editor",
        str(input_path),
        "-o",
        str(output_path) + "-vod",
        "-fps " + str(input_rate),
        "--export",
        export_format,
        "--cut-out 0,",
    ]
)

if focus == "none":
    framelist = []
    frameout = ""
    end = "end"

    for vod in vodlist:
        framelist.append(vod[1])

    for frame in framelist:
        frameout += "".join([str(frame[0]), " ", str(frame[1]), ","])

    exec = cmd + frameout + end
    subprocess.call(exec, shell=True)

ordlist = set(ordlist)
for ord in ordlist:
    framelist = []
    print(chr(ord))
    for i in splits:
        if i[0] == chr(ord):
            framelist.append((i[1]))
    # build command string
    # "0,f1" " " "f2,f3"
    cmd = " ".join(
        [
            "auto-editor",
            str(input_path),
            "-o",
            str(output_path) + "-" + chr(ord),
            "-fps " + str(input_rate),
            "--export",
            export_format,
            "--cut-out 0,",
        ]
    )
    frameout = ""
    end = "end"
    for frame in framelist:
        frameout += "".join([str(frame[0]), " ", str(frame[1]), ","])

    exec = cmd + frameout + end
    subprocess.call(exec, shell=True)
