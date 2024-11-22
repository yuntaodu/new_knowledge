# new_knowledge

**crawl_cnn.py** 用于爬取原始网页数据

**analysis.py** 用于使用GPT总结网页内容及过滤
 
**show.html** 用于展示图片及网页内容


**CNN_Data_Collection/download_EUQA_img.py** 用于下载图像数据，可以设置下载数量

data example
[
  "EUQA": {
      "EUQA1": {
          "Entity1": "Sydney",
          "Upper1": "City",
          "Question1": "In which city did the terrorist act occur, as shown in the image?",
          "Answer1": "Sydney"
      }
  }
]




**CNN_Data_Collection/clip_k_means_filter_img.py** 用于clip+k-means过滤离群点图像
