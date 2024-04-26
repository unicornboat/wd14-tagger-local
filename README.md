
### Modiefied from [corkborg/wd14-tagger-standalone](https://github.com/corkborg/wd14-tagger-standalone). Credit to [corkborg](https://github.com/corkborg)

## 下载方式

因为模型文件超过github要求，所以拉取夏目之后需要单独下载模型包解压缩到项目根目录下。

模型文件打包的MD5验证：`21731ce7838c2a8fe93d988e406bc6bc`

[百度网盘，提取码：8888](https://pan.baidu.com/s/1Cp7lMWkt_13I4LOiKZdO7Q?pwd=8888)

[MEGA](https://mega.nz/file/8p0BTLwL#yuRmRzrxJO7IXUKszRwvWA9VJl_tImvXhnl3AMJpHbw)

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
