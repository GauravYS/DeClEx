 # DeClEx - Advanced Processing Pipeline for Critical Healthcare Application

## DeClEx Architecture 
The architecture consists of 1. **dedicated denoising and deblurring autoencoders** to mitigate noise and blur. We then compare our **CNN + Spatial Attention model** with state of the art architectures and highlight it's advantages. 
We provide explianability for the model's prediction using **Local Interpretable Model-Agnostic Explanations (LIME)** and **Shapley Additive Explanations(SHAP)**

![image](https://github.com/GauravYS/Job-Portal-Application/assets/116845183/8b9f00b6-4602-4d4a-a062-5a1efb641ffb)

## Dataset Information 
The data is sourced from https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset. It contains 4 classes and is used for classification tasks. 

## Loss curves for denoising and deblurring autoencoder
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/86023eab-9c25-4ea1-ab42-bd91e776297f)  ![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/1b3e91df-b89f-4b18-aabe-afc36624c81d)

## CNN + Spatial Attention 
### Spatial Attention Module
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
 ### Backend 
 We have created 3 different APIs,
1. /analyse - this API is used to get basic info like predicted class and the probabilities.
2. /complete_analysis -  this API performs all the setps involved in segmentaion of lime and shap values and responds with respective paths.
3. /images - this API will return the image, for this file: "" in a json body will contain the path provided by above api to get the images from the server.
Examples:
```
curl --location 'http://34.16.167.233:8000/complete_analysis' \
--form 'image=@"/Users/saicharan/Downloads/dataset/Testing/pituitary/Te-pi_0187.jpg"'

curl --location 'http://34.16.167.233:8000/analysis' \
--form 'image=@"/Users/saicharan/Downloads/dataset/Testing/pituitary/Te-pi_0187.jpg"'

curl --location 'http://34.16.167.233:8000/images' \
--header 'Content-Type: application/json' \
--data '{
    "file": "/home/saicharan19995/MasterProject/Brain_Tumor_Analysis/backend/output/2024-04-28/processed_image_20240428063628.png"
}'
```
### Frontend 
We used JavaScript, HTML and CSS for our frontend. 

### Hosting the application on GCP 
1. Create a Cloud Engine, with suffient memory, ideally you can use **c2-standard-4** machine type. CPU platform is **Intel Cascade Lake**. Make sure you have python-3.9 and above in the instance created.
2. Check python version using bellow command
``` 
python3 --version
```
3. Install git and clone the project.
``` 
sudo apt install git-all
sudo apt install git-lfs
```
4. Setup virual python env and activate it
```
sudo apt install python3-virtualenv
python3 -m virtualenv -p python3 venu
source venu/bin/activate
```
5. Install all requirements
```
pip3 install -r code/requirements.txt
```
6. We need 2 ports which needs to be accessed from external source, So in steps do that
```
Navigate to VPC network details
Select FIREWALLS
Add or edit anyone rule with
IPv4 ranges: 0.0.0.0/0 and ports tcp:3000, 8000
```
7. To run backend and front end.
```
sudo apt install npm
sudo npm install pm2 -g
pm2 start frontend/code/main.py --name brain_tumor --interpretor=python3
pm2 start backend/index.js --name brain_tumor_frontend
pm2 list # To view deployed services
```
8. To get the external ip which can be accessed by all services
```
curl ifconfig.me
```
9. Update the endpoint code in app.js to the new ip.

## Meet our team 
![image](https://github.com/GauravYS/Master-Project-Group-2/assets/116845183/a604f580-d6b2-41de-a2be-3d1eaf1c6d46)


 







