
### Modiefied from [corkborg/wd14-tagger-standalone](https://github.com/corkborg/wd14-tagger-standalone). Credit to [corkborg](https://github.com/corkborg)

## 模型方式

因为模型文件超过github要求，所以拉取夏目之后需要单独下载模型包解压缩到项目根目录下。

默认模型是：WD14_ConvNeXTV2_v1。如果不想在命令行后面使用`--model`选项的话，直接下载这个默认模型就可以了。

| 模型名称                             | 下载链接                                                                              |
|----------------------------------|-----------------------------------------------------------------------------------|
| 全部模型                             | [百度网盘，提取码：8888](https://pan.baidu.com/s/1nX2rN3UpThURkUbaDS7tEQ?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/o9khTZJI#yuRmRzrxJO7IXUKszRwvWA9VJl_tImvXhnl3AMJpHbw) |
| WD14_ViT_v1                      | [百度网盘，提取码：8888](https://pan.baidu.com/s/1mbrl6ZH7V6GaOmSzffx0WQ?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/c0U3VYyQ#bh2c1IdIILZBdJxulyRCrq3Y8J-KyDr4Q_-jeS8QAkI)                                                                          |
| WD14_ViT_v2                      | [百度网盘，提取码：8888](https://pan.baidu.com/s/1h7faU4MSZlLVOfAGHAyxeA?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/MhUTgAqa#be7kQOzTIIQYg3nr0uy9A58LAELXUvfsLIjipM4N5yo)                                                                          |
| WD14_SwinV2_v1                   | [百度网盘，提取码：8888](https://pan.baidu.com/s/1h7faU4MSZlLVOfAGHAyxeA?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/94EQWabK#2iPOo_9cRwLyEW6sT-ndKKZCIHcIl_ZTllPB5R7BMPo)                                                                          |
| WD14_ConvNeXT_v1                 | [百度网盘，提取码：8888](https://pan.baidu.com/s/1bLs5uGy0RXGZbEdZYI3xjw?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/4w9TXJzA#1Xtpdi1Q5CjKiufPO6UN5cOSZ1z4C5dypf5CIuKj5Mg)                                                                          |
| WD14_ConvNeXT_v2                 | [百度网盘，提取码：8888](https://pan.baidu.com/s/1VlDW1yVynnF_crqtUEyLMQ?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/ksMlTSqR#4s4vck1v8OCSD9xhcAdUKXPPiwdiAzbmzoObxIq17xs)                                                                          |
| WD14_ConvNeXTV2_v1 (默认模型)        | [百度网盘，提取码：8888](https://pan.baidu.com/s/1NU7ICdpHhl1TECbeW9Icmg?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/AxkQhYha#o1Gb85MctHSurPp17vUYjVGp9jwECqtEbwgGJud7EtA)                                                                          |
| WD14_moat_tagger_v2              | [百度网盘，提取码：8888](https://pan.baidu.com/s/1TSLeV5Sc_2v53hquiRxC7w?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/kxtikA7K#SsjyR6Mb52MXWAbiwULKedA193Sj8OQ3BEfB-zUnDUE)                                                                          |
| ML-Danbooru_TResNet-D_6-30000    | [百度网盘，提取码：8888](https://pan.baidu.com/s/1d4doQle8SeDogQvvdDOpsg?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/ogVSDCCS#eL7zPCCWdWdXU7aM-0viY_fez7dc6IuuEpjPy1s9BGQ)                                                                          |
| ML-Danbooru_Caformer_dec-5-97527 | [百度网盘，提取码：8888](https://pan.baidu.com/s/1PpiEVjAAAGCVl-uoxFvZog?pwd=8888)         |
|                                  | [MEGA](https://mega.nz/file/kg0j2YKQ#mEWO1vVfDwFUvP46lFF60DhoBU_XyTGstR91iyS-HlQ)                                                                          |

 （提取码：）

## 安装方式

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 用法

```shell
用法: run.py [-h] (--dir DIR | --file FILE) [--threshold THRETHOLD] [--ext EXT]
              [--model {wd14-vit.v1,wd14-vit.v2,wd14-convnext.v1,wd14-convnext.v2,wd14-convnextv2.v1,wd14-swinv2-v1,wd-v1-4-moat-tagger.v2,mld-caformer.dec-5-97527,mld-tresnetd.6-30000}]

选项:
  -h, --help            显示此帮助消息并退出
  --dir DIR             对目录中的所有图像进行打标
  --file FILE           对文件进行打标
  --filetxt FILE        对文件进行打标并将结果写入同名txt文件
  --threshold THRETHOLD
                        打标值的阈值概率(默认为0.35)
  --ext EXT             如果是目录的情况，要为字幕文件添加的扩展名
  --model MODEL
                        用于打标的模型名称，具体模型名称参考下面的模型列表
                        这是一个可选参数，不写的话默认使用 wd14-convnext.v1 模型
```

## 目前支持的模型列表

```shell
wd14-vit.v1
wd14-vit.v2
wd14-convnext.v1
wd14-convnext.v2
wd14-convnextv2.v1
wd14-swinv2-v1
wd-v1-4-moat-tagger.v2
mld-caformer.dec-5-97527
mld-tresnetd.6-30000
```

## 例子

```shell
# 打标单个文件
python run.py --file image.jpg

# 打标单个文件并将tags保存到同目录内的同名txt文件中
python run.py --filetxt image.jpg

# 打标整个目录
python run.py --dir /Users/myname/Downloads/pictures

# 使用指定模型打标整个目录
python run.py --dir /Users/myname/Downloads/pictures --model wd14-vit.v1
```

## 其他

原项目支持 `mld-caformer.dec-5-97527` 和 `mld-tresnetd.6-30000`。这两个模型虽然我有包含在里面，但是我测试的打标只有一个`[`符号，所以不推荐用这两个模型。
其他模型均测试成功。
