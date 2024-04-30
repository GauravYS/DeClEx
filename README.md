 # DeClEx - Advanced Processing Pipeline for Critical Healthcare Application

## DeClEx Architecture 
The architecture consists of 1. **dedicated denoising and deblurring autoencoders** to mitigate noise and blur. We then compare our CNN + Spatial Attention model with state of the art architectures and highlight it's advantages. 
We provide explianability for the model's prediction using **Local Interpretable Model-Agnostic Explanations (LIME)** and **Shapley Additive Explanations(SHAP)**

![image](https://github.com/GauravYS/Job-Portal-Application/assets/116845183/8b9f00b6-4602-4d4a-a062-5a1efb641ffb)

## Dataset Information 
The data is sourced from https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset. It contains 4 classes and is used for classification tasks. 

## Loss curves for denoising and deblurring autoencoder
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/86023eab-9c25-4ea1-ab42-bd91e776297f)  ![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/1b3e91df-b89f-4b18-aabe-afc36624c81d)

## CNN + Spatial Attention 
### Spatial Attention Module ]
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/bd08bbe2-595b-4f35-90aa-ab17ed3e9897)

### Final integrated architecture 
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/71931ebf-8b26-484b-8ddf-5edfaff2da12)

**Benefits** - Comparable accuracy to state-of-the-art pretrained models while being **3x** faster in terms of train time. 

## Explainable AI methodologies 
### Local Interpretable Model-Agnostic Explanations (LIME)
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/429c1d59-6b92-4cc8-b315-d461f67af729)
### Shapley Additive Explanations (SHAP)
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/6c97b4f9-d485-4dc6-8a2e-d018a83ee042)

## DeClEx Web Application 
 **Project Link** - http://34.16.167.233:3000/

 







