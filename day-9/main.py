from dataclasses import dataclass
from collections.abc import Sequence, Mapping
from copy import deepcopy


@dataclass
class FileEntry:
    id: int
    size: int
    freespace: int
    filePos: int = -1

    def __hash__(self):
        return hash((self.id, self.size, self.freespace))


with open("./day-9/input.txt", "r") as input_file:
    data = input_file.read().strip()
    files: Sequence[FileEntry] = list()
    for idx in range(len(data) // 2 + 1):
        i = idx * 2
        size = int(data[i])
        freespace = int(data[i + 1]) if i < len(data) - 2 else 0
        file = FileEntry(idx, size, freespace)
        files.append(file)
    files2 = deepcopy(files)


def find_free_block(startIdx: int):
    currentFileIdx = startIdx
    while currentFileIdx < len(files):
        currentFile = files[currentFileIdx]
        if currentFile.freespace > 0:
            return currentFileIdx
        currentFileIdx += 1


# part 1
currentFileIdx = 0
while True:
    targetFileIdx = find_free_block(currentFileIdx)
    if targetFileIdx == len(files) - 1:
        break
    targetFile = files[targetFileIdx]
    lastFile = files[-1]

    movedBlocks = min(targetFile.freespace, lastFile.size)
    lastFile.size -= movedBlocks
    movedFreeSpace = targetFile.freespace - movedBlocks
    newFile = FileEntry(lastFile.id, movedBlocks, movedFreeSpace)
    targetFile.freespace = 0
    files = [*files[: targetFileIdx + 1], newFile, *files[targetFileIdx + 1 :]]
    if lastFile.size == 0:
        files = files[:-1]


def calcOutput(files):
    total1 = 0
    bStart = 0
    for entry in files:
        for _ in range(entry.size):
            total1 += entry.id * bStart
            bStart += 1
        bStart += entry.freespace
    return total1


def printSpace(files):
    print(
        "".join([str(entry.id) * entry.size + "." * entry.freespace for entry in files])
    )


total1 = calcOutput(files)
print(f"{total1=}")

# part 2

# printSpace(files2)

targetLastFile = len(files2) - 1
lowestFileId = len(files2)
while targetLastFile > 0:
    lastFile = files2[targetLastFile]
    if lastFile.id >= lowestFileId:
        targetLastFile -= 1
        continue
    lowestFileId = lastFile.id

    moved = False
    for targetFileIdx, targetFile in enumerate(files2[:targetLastFile]):
        if targetFile.freespace < lastFile.size:
            continue

        movedFreeSpace = targetFile.freespace - lastFile.size
        newFile = FileEntry(lastFile.id, lastFile.size, movedFreeSpace)
        targetFile.freespace = 0
        prefix = files2[: targetFileIdx + 1]
        midfix = files2[targetFileIdx + 1 : targetLastFile]
        newOpenFile = FileEntry(-1, 0, lastFile.size + lastFile.freespace)
        suffix = files2[targetLastFile + 1 :]
        files2 = [*prefix, newFile, *midfix, newOpenFile, *suffix]
        # printSpace(files2)
        moved = True
        break

    if not moved:
        targetLastFile -= 1


total2 = calcOutput(files2)
print(f"{total2=}")
