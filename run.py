import sys
from tagger.interrogator import Interrogator, WaifuDiffusionInterrogator
from PIL import Image
from pathlib import Path
import argparse

from tagger.interrogators import interrogators

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dir', help='对目录中的所有图像进行打标')
group.add_argument('--file', help='对文件进行打标')
group.add_argument('--filetxt', help='对文件进行打标并将结果写入同名txt文件')

parser.add_argument(
    '--threshold',
    type=float,
    default=0.35,
    help='打标值的阈值概率 (默认为0.35)')
parser.add_argument(
    '--ext',
    default='.txt',
    help='如果是目录的情况，要为打标文件添加的扩展名')
parser.add_argument(
    '--model',
    default='wd14-convnextv2.v1',
    choices=list(interrogators.keys()),
    help='用于打标的模型名称')

args = parser.parse_args()

# 读取要使用的interrogator
interrogator = interrogators[args.model]

def image_interrogate(image_path: Path):
    """
    从图像路径进行打标
    """
    im = Image.open(image_path)
    result = interrogator.interrogate(im)
    return Interrogator.postprocess_tags(result[1], threshold=args.threshold)

if args.dir:
    d = Path(args.dir)
    for f in d.iterdir():
        if not f.is_file() or f.suffix not in ['.png', '.jpg', '.webp']:
            continue
        image_path = Path(f)
        print('processing:', image_path)
        tags = image_interrogate(image_path)
        tags_str = ", ".join(tags.keys())
        with open(f.parent / f"{f.stem}{args.ext}", "w") as fp:
            fp.write(tags_str)

if args.file:
    tags = image_interrogate(Path(args.file))
    print()
    tags_str = ", ".join(tags.keys())
    print(tags_str)

if args.filetxt:
    tags = image_interrogate(Path(args.filetxt))
    tags_str = ", ".join(tags.keys())
    with open(Path(args.filetxt).parent / f"{Path(args.filetxt).stem}{args.ext}", "w") as fp:
        fp.write(tags_str)
