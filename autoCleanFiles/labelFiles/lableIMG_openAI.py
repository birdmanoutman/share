import glob
import os

import clip
import piexif
import torch
from PIL import Image, PngImagePlugin

"""目前只有JPG格式的能用"""


class ImageLabeler:
    def __init__(self, folder_path, labels, device):
        self.folder_path = folder_path
        self.labels = labels
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    @staticmethod
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

    def preprocess_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        # 假设你的模型需要的尺寸是224x224
        desired_size = 224
        image = self.center_crop(image, desired_size, desired_size)
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            alpha = image.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", image.size, (255, 255, 255) + (255,))  # 白色背景
            bg.paste(image, mask=alpha)
            image = bg.convert('RGB')

        # 应用模型特定的预处理
        image = self.preprocess(image).unsqueeze(0).to(device)
        return image

    def predict_label(self, image):
        # 用预处理后的图像和CLIP模型进行预测
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_inputs = torch.cat([clip.tokenize(label) for label in self.labels]).to(self.device)
            text_features = self.model.encode_text(text_inputs)
            similarities = image_features @ text_features.T
            similarities = torch.nn.functional.softmax(similarities, dim=-1)
            best_label_idx = similarities.squeeze().argmax().item()
            predicted_label = self.labels[best_label_idx]
        return predicted_label

    def label_images(self):
        # 获取文件夹中的所有支持图片格式
        supported_formats = ['jpg', 'jpeg', 'png']
        files = []
        for ext in supported_formats:
            files.extend(glob.glob(f"{self.folder_path}/*.{ext}"))
        # 对每个图片文件进行预测和添加元数据
        for image_path in files:
            image = self.preprocess_image(image_path)
            predicted_label = self.predict_label(image)
            self.add_metadata_to_image(image_path, predicted_label)
            print(f"Image: {image_path}, Predicted label: {predicted_label}")

    def add_metadata_to_image(self, image_path, label):
        # 根据文件扩展名确定处理方式
        file_extension = os.path.splitext(image_path)[-1].lower()
        if file_extension == '.jpg' or file_extension == '.jpeg':
            self.add_jpeg_label(image_path, label)
        elif file_extension == '.png':
            self.add_png_text_label(image_path, label)

        else:
            print(f"File format {file_extension} is not supported.")

    @staticmethod
    def add_jpeg_label(image_path, label):
        # 读取现有的EXIF数据或创建新的EXIF数据
        exif_dict = piexif.load(image_path) if os.path.exists(image_path) else {'Exif': {}, '0th': {}, '1st': {},
                                                                                'thumbnail': None}

        # 转换标签为适当的格式并加入到EXIF中的XPKeywords字段
        # 注意：这里假设标签是简单的文本字符串
        keywords = label.encode('utf-16le')
        exif_dict['0th'][piexif.ImageIFD.XPKeywords] = keywords

        # 写回EXIF数据到图片
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
        print(f"Label added to {image_path} (JPEG)")

    @staticmethod
    def add_png_text_label(image_path, label):
        image = Image.open(image_path)
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Label", label)
        image.save(image_path, pnginfo=metadata)
        print(f"Label added to {image_path} (PNG)")


# 主函数和使用示例
if __name__ == "__main__":
    folder_path = 'IMG'  # 修改为实际路径
    labels = ["object", "human", "scene", "diagram", "table"]  # 修改为你的标签
    device = "cuda" if torch.cuda.is_available() else "cpu"

    labeler = ImageLabeler(folder_path, labels, device)
    labeler.label_images()
