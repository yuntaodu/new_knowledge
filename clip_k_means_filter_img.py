import json
import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sklearn.cluster import KMeans
import numpy as np
import re
from tqdm import tqdm
import matplotlib.pyplot as plt


model = CLIPModel.from_pretrained("/home/jiangkailin/datacheckpoint/checkpoint/clip-vit-large-patch14-336")
processor = CLIPProcessor.from_pretrained("/home/jiangkailin/datacheckpoint/checkpoint/clip-vit-large-patch14-336")

def extract_features(image_path):
    """提取单张图像的特征。"""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs).cpu().numpy()
    return features.flatten()

def find_closest_image_in_largest_cluster(features, num_clusters=3):
    """进行K-means聚类，找到数量最多的类别，并返回该类别中距离中心最近的图像索引。"""
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(features)
    
    
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    largest_cluster = labels[np.argmax(counts)]
    
    
    cluster_indices = np.where(kmeans.labels_ == largest_cluster)[0]
    cluster_center = kmeans.cluster_centers_[largest_cluster]
    distances = np.linalg.norm(features[cluster_indices] - cluster_center, axis=1)
    closest_index = cluster_indices[np.argmin(distances)]
    
    return closest_index, kmeans

def extract_cnn_id(clip_img_path):
    match = re.search(r'CNN_EUQA_(\d+)', clip_img_path[0])
    if match:
        return match.group(1)
    return None


root_folder = "/home/jiangkailin/project/New_Knowledge/CNN_EUQA"
output_folder = "/home/jiangkailin/project/New_Knowledge/CNN_EUQA_clusters3"
json_file = "/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o_index.json"
os.makedirs(output_folder, exist_ok=True)

with open(json_file, "r") as f:
    data = json.load(f)


for cnn_folder in tqdm(os.listdir(root_folder), desc="Processing CNN folders"):
    cnn_path = os.path.join(root_folder, cnn_folder)
    if os.path.isdir(cnn_path):
        
        for euqa_folder in tqdm(os.listdir(cnn_path), desc=f"Processing {cnn_folder}", leave=False):
            euqa_path = os.path.join(cnn_path, euqa_folder)
            if os.path.isdir(euqa_path):
                
                image_paths = [os.path.join(euqa_path, img) for img in os.listdir(euqa_path) if img.endswith('.jpg')]
                features = np.array([extract_features(img_path) for img_path in tqdm(image_paths, desc=f"Extracting features for {euqa_folder}", leave=False)])

                
                closest_index, kmeans = find_closest_image_in_largest_cluster(features)
                clip_img = image_paths[closest_index]

                cnn_id = int(extract_cnn_id([clip_img])) - 1

                if euqa_folder in data[cnn_id]["EUQA"]:
                    data[cnn_id]["EUQA"][euqa_folder]["Clip"] = clip_img
                else:
                    print(f"Warning: {euqa_folder} not found in JSON structure.")

                
                plt.figure(figsize=(8, 6))
                plt.scatter(features[:, 0], features[:, 1], c=kmeans.labels_, cmap='viridis', marker='o', s=30, label="Images")
                plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x', s=100, label="Cluster Center")
                plt.scatter(features[closest_index, 0], features[closest_index, 1], c='blue', marker='*', s=150, label="Closest Image")
                plt.title(f"Clustering Result for {cnn_folder}/{euqa_folder}")
                plt.xlabel("Feature Dimension 1")
                plt.ylabel("Feature Dimension 2")
                plt.legend()

                
                output_path = os.path.join(output_folder, f"{cnn_folder}_{euqa_folder}_cluster.png")
                plt.savefig(output_path)
                plt.close()


with open("/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o_clip_imgs3.json", "w") as f:
    json.dump(data, f, indent=4)

print("更新后的JSON文件已保存为 'EUQA_mini_2_4o_clip_imgs2.json'")








