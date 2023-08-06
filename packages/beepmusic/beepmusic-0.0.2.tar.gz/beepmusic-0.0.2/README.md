# BeepMusic

使用计算机提示音播放乐谱。

Play music using computer beep prompt tone.

## Prerequisite

- windows system
- python >= 3.6

## Install

```cmd
pip install beepmusic
```

## Quick Start

Run command in cmd or powershell:

```cmd
python -m beepmusic [BMCFile]
```

## BMC File

BMC File is a file type that specify name, tone, speed and melody of a sone
Since I am not a professional musician, BMC file is simple and crude. However,
it supports comments! :)

Please check the example file 'joy.bmc'.

## Notes

The `Beep()` function latency is high, so the rhythm won't be precise. Please
set bpm lower than 150.
