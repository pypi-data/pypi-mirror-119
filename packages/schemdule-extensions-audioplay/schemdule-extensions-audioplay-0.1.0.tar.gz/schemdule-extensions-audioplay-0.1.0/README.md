# schemdule-extensions-audioplay

[![Schemdule](https://socialify.git.ci/StardustDL/schemdule/image?description=1&font=Bitter&forks=1&issues=1&language=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Light)](https://github.com/StardustDL/schemdule)

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/v/schemdule-extensions-audioplay.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-audioplay/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-audioplay)](https://pepy.tech/project/schemdule-extensions-audioplay)

A audio player extension for 
[Schemdule](https://github.com/StardustDL/schemdule).

- Platform ![](https://img.shields.io/badge/Linux-yes-success?logo=linux) ![](https://img.shields.io/badge/Windows-yes-success?logo=windows) ![](https://img.shields.io/badge/MacOS-yes-success?logo=apple) ![](https://img.shields.io/badge/BSD-yes-success?logo=freebsd)
- Python ![](https://img.shields.io/pypi/implementation/schemdule-extensions-audioplay.svg?logo=pypi) ![](https://img.shields.io/pypi/pyversions/schemdule-extensions-audioplay.svg?logo=pypi) ![](https://img.shields.io/pypi/wheel/schemdule-extensions-audioplay.svg?logo=pypi)
- [All extensions](https://pypi.org/search/?q=schemdule)

## Install

Install dependencies:

```sh
# Install dependencies on Linux (only)
sudo apt-get install -y python3-dev libasound2-dev

# Install ffmpeg
choco install ffmpeg        # Windows
apt-get install -y ffmpeg   # Linux
brew install ffmpeg         # MacOS
```

Use pip:

```sh
pip install schemdule-extensions-audioplay
```

Or use pipx:

```sh
pipx inject schemdule schemdule-extensions-audioplay

# Upgrade
pipx upgrade schemdule --include-injected
```

Check if the extension installed:

```sh
schemdule ext
```

## Usage

This extension provide a `AudioPlayerPrompter` and add the following extension methods on `PrompterBuilder` and `PayloadBuilder`.

```python
class PrompterBuilder:
    def useAudioPlayer(self: PrompterBuilder, endSpace: Optional[timedelta] = None, final: bool = False) -> PrompterBuilder:
        """
        endSpace: Stop audio before next event, default 10 seconds. The empty space leads to the next event outdated.
        """
        ...

class PayloadBuilder:
    def useAudio(self, files: Iterable[str]) -> "PayloadBuilder":
        ...
```

Use the extension in the schema script.

```python
# schema.py
ext("audioplay")

at(..., payloads().useAudio(["file1"]))

prompter.useAudioPlayer()
```

