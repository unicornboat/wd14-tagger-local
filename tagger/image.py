from PIL import Image

def resize_image(resize_mode, im, width, height, upscaler_name=None):
    """
    使用指定的 resize_mode、width 和 height 来调整图像大小。

    参数:
        resize_mode: 调整图像大小时要使用的模式。
            0: 将图像调整为指定的宽度和高度。
            1: 调整图像大小以填充指定的宽度和高度,保持长宽比,然后将图像居中,多余部分裁剪。
            2: 调整图像大小以适应指定的宽度和高度,保持长宽比,然后将图像居中,用图像数据填充空白部分。
        im: 要调整大小的图像。
        width: 调整图像宽度到指定值。
        height: 调整图像高度到指定值。
        upscaler_name: 要使用的上采样器的名称。如果未提供,则默认为opts.upscaler_for_img2img。
    """

    def resize(im, w, h):
        return im.resize((w, h), resample=Image.LANCZOS)

    if resize_mode == 0:
        res = resize(im, width, height)

    elif resize_mode == 1:
        ratio = width / height
        src_ratio = im.width / im.height

        src_w = width if ratio > src_ratio else im.width * height // im.height
        src_h = height if ratio <= src_ratio else im.height * width // im.width

        resized = resize(im, src_w, src_h)
        res = Image.new("RGB", (width, height))
        res.paste(resized, box=(width // 2 - src_w // 2, height // 2 - src_h // 2))

    else:
        ratio = width / height
        src_ratio = im.width / im.height

        src_w = width if ratio < src_ratio else im.width * height // im.height
        src_h = height if ratio >= src_ratio else im.height * width // im.width

        resized = resize(im, src_w, src_h)
        res = Image.new("RGB", (width, height))
        res.paste(resized, box=(width // 2 - src_w // 2, height // 2 - src_h // 2))

        if ratio < src_ratio:
            fill_height = height // 2 - src_h // 2
            if fill_height > 0:
                res.paste(resized.resize((width, fill_height), box=(0, 0, width, 0)), box=(0, 0))
                res.paste(resized.resize((width, fill_height), box=(0, resized.height, width, resized.height)), box=(0, fill_height + src_h))
        elif ratio > src_ratio:
            fill_width = width // 2 - src_w // 2
            if fill_width > 0:
                res.paste(resized.resize((fill_width, height), box=(0, 0, 0, height)), box=(0, 0))
                res.paste(resized.resize((fill_width, height), box=(resized.width, 0, resized.width, height)), box=(fill_width + src_w, 0))

    return res
