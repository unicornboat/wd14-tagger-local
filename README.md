
### Modiefied from [corkborg/wd14-tagger-standalone](https://github.com/corkborg/wd14-tagger-standalone). Credit to [corkborg](https://github.com/corkborg)

## 安装方式

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 用法

```
用法: run.py [-h] (--dir DIR | --file FILE) [--threshold THRETHOLD] [--ext EXT]
              [--model {wd14-vit.v1,wd14-vit.v2,wd14-convnext.v1,wd14-convnext.v2,wd14-convnextv2.v1,wd14-swinv2-v1,wd-v1-4-moat-tagger.v2,mld-caformer.dec-5-97527,mld-tresnetd.6-30000}]

选项:
  -h, --help            显示此帮助消息并退出
  --dir DIR             对目录中的所有图像进行打标
  --file FILE           对文件进行打标
  --threshold THRETHOLD
                        打标值的阈值概率(默认为0.35)
  --ext EXT             如果是目录的情况，要为字幕文件添加的扩展名
  --model MODEL
                        用于打标的模型名称，具体模型名称参考下面的模型列表
                        这是一个可选参数，不写的话默认使用 wd14-convnext.v1 模型
```

## 目前支持的模型列表

```
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

```
# 打标单个文件
python run.py --file image.jpg

# 打标整个目录
python run.py --dir /Users/myname/Downloads/pictures

# 使用指定模型打标整个目录
python run.py --dir /Users/myname/Downloads/pictures --model wd14-vit.v1
```

## 其他

原项目支持 `mld-caformer.dec-5-97527` 和 `mld-tresnetd.6-30000`。这两个模型虽然我有包含在里面，但是我测试的打标只有一个`[`符号，所以不推荐用这两个模型。
其他模型均测试成功。
