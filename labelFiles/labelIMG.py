import glob
import os

import clip
import piexif
import torch
from PIL import Image, PngImagePlugin


def add_metadata_to_image(image_path, label):
    # 根据文件扩展名确定处理方式
    file_extension = os.path.splitext(image_path)[-1].lower()

    if file_extension == '.jpg' or file_extension == '.jpeg':
        add_jpeg_label(image_path, label)
    elif file_extension == '.png':
        add_png_text_label(image_path, label)

    else:
        print(f"File format {file_extension} is not supported.")


def add_jpeg_label(image_path, label):
    exif_dict = {"Exif": {piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(label)}}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)
    print(f"Label added to {image_path} (JPEG)")


def add_png_text_label(image_path, label):
    image = Image.open(image_path)
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Label", label)
    image.save(image_path, pnginfo=metadata)
    print(f"Label added to {image_path} (PNG)")


# 测试代码
if __name__ == "__main__":
    # 设定标签和图像文件路径
    label = "Example Label"
    images_folder = "path/to/your/images/folder"
    images = [os.path.join(images_folder, f) for f in os.listdir(images_folder) if
              f.endswith(('.jpg', '.jpeg', '.png'))]

    for image_path in images:
        add_metadata_to_image(image_path, label)


# 前面的函数保持不变，这里只展示修改后的main部分

def main(folder_path):
    # 加载CLIP模型
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    # 定义英文标签（如需要中文标签，请替换为中文）
    labels = ["object", "human", "scene", "diagram", "table"]
    text_inputs = torch.cat([clip.tokenize(label) for label in labels]).to(device)

    # 获取所有支持的图片文件
    supported_formats = ['jpg', 'png', 'webp']
    files = []
    for ext in supported_formats:
        files.extend(glob.glob(f"{folder_path}/*.{ext}"))

    # 对每张图片进行预测
    for image_path in files:
        image = preprocess_image(image_path, preprocess)
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_inputs)
            similarities = image_features @ text_features.T
            similarities = torch.nn.functional.softmax(similarities, dim=-1)
            best_label_idx = similarities.squeeze().argmax().item()
            predicted_label = labels[best_label_idx]

        print(f"Image: {image_path}, Predicted label: {predicted_label}")


def center_crop(image, new_width, new_height):
    # 计算需要裁剪的宽度和高度
    width, height = image.size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    # 中心裁剪图像
    image = image.crop((left, top, right, bottom))
    return image


# 用预处理函数来处理图像，并进行中心裁剪
def preprocess_image(image_path, preprocess):
    image = Image.open(image_path).convert("RGB")

    # 假设你的模型需要的尺寸是224x224
    desired_size = 224
    image = center_crop(image, desired_size, desired_size)
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", image.size, (255, 255, 255) + (255,))  # 白色背景
        bg.paste(image, mask=alpha)
        image = bg.convert('RGB')

    # 应用模型特定的预处理
    image = preprocess(image).unsqueeze(0).to(device)
    return image


# 加载CLIP模型
device = "cuda" if torch.cuda.is_available() else "cpu"

if __name__ == "__main__":
    # 定义你想要分类图片的文件夹路径
    folder_path = 'IMG'
    main(folder_path)
