from PIL import Image
import os

# 输入和输出文件夹路径
input_folder = 'resource/support_card'
output_folder = 'resource/cut'

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有 PNG 图片
for filename in os.listdir(input_folder):
    if filename.endswith('.png'):
        # 打开图片
        img = Image.open(os.path.join(input_folder, filename))
        
        # 确保图片尺寸为 70x70
        if img.size == (70, 70):
            # 裁剪图片
            cropped_img = img.crop((0, 0, 70, 50))
            
            # 保存裁剪后的图片到输出文件夹
            cropped_img.save(os.path.join(output_folder, filename))
        else:
            print(f"Image {filename} is not 70x70, skipping.")

print("All images have been processed.")
