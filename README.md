# new_knowledge

**crawl_cnn.py** 用于爬取原始网页数据

**analysis.py** 用于使用GPT总结网页内容及过滤
 
**show.html** 用于展示图片及网页内容



**CNN_Data_Collection/download_EUQA_img.py** 用于下载图像数据，可以设置下载数量

**CNN_Data_Collection/clip_k_means_filter_img.py** 用于clip+k-means过滤离群点图像

**CNN Data Collection Pipeline**

1. 用得到的url，去解析下载得到news data [使用CNN_Data_Collection/extract_cnn.py]  
2. clean news data，例如：content中有CNN - 和content为空的情况 [使用CNN_Data_Collection/clean_content.py]  
3. clean imgs，把图像数量=0和>5的数据删除 [使用CNN_Data_Collection/delete_img.py]  
4. 每条数据的imgs，根据url，把图像下载到本地 [使用CNN_Data_Collection/download_img.py]  
5. 每条数据的imgs，选取第一张img，作为training img [使用CNN_Data_Collection/extract_1_img.py]  
6. 给每条数据增加index [使用CNN_Data_Collection/add_index.py]  
**7. 使用title和content，生成summary和entity（使用api） [使用CNN_Data_Collection/summary.py]**
8. 给summary的开头，加上timestamp [使用CNN_Data_Collection/time.py + add_time.py]  
**9. 使用entity和summary，生成QA（使用api） [使用CNN_Data_Collection/question_generation.py]**  
10. 根据生成的QA中的entity和upper word下载图像 [使用CNN_Data_Collection/download_EUQA_img.py]  
11. 使用clip和k-means去剔除离群点图像 [使用CNN_Data_Collection/clip_k_means_filter_img.py]  



