import cv2
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from lime import lime_image # type: ignore
import shap # type: ignore
import matplotlib # type: ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type: ignore
from skimage.segmentation import mark_boundaries # type: ignore
import os
from datetime import datetime, date, timedelta # type: ignore

#Class Names
output_classes = {0: "glioma", 1: "meningioma", 2: "notumor", 3: "pituitary"}
# Set the DPI for your target resolution
dpi = 300
# Height and Width
height_in_inches = 8
width_in_inches = height_in_inches  # Making a square image for simplicity

#Output paths
current_date = datetime.now().strftime("%Y-%m-%d")
saving_directory = f"{os.getcwd()}/output/{current_date}"
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
#Daving paths
processed_image_path = f"{saving_directory}/processed_image_{current_time}.png"
lime_segment_boundries_path = f"{saving_directory}/lime_segment_boundries_{current_time}.png"
lime_segment_output_path = f"{saving_directory}/lime_segment_output_{current_time}.png"
shap_output_path = f"{saving_directory}/shap_image_plot_{current_time}.png"
# Path for best model which is saved
print("Current path ", os.getcwd())
cnn_model = f"{os.getcwd()}/models/best_model.h5"
shap_cnn_model = f"{os.getcwd()}/models/shap_cnn_model.h5"
deblur_model_path = f"{os.getcwd()}/models/deblur_encoder.h5"
denoise_model_path = f"{os.getcwd()}/models/denoise_encoder.h5"

def denoise_and_deblur_images(image):
    autoencoder_deblur = load_model(deblur_model_path)
    autoencoder_denoise = load_model(denoise_model_path)
    denoised_images = autoencoder_denoise.predict(image)
    deblurred_images = autoencoder_deblur.predict(denoised_images)
    plt.figure(figsize=(width_in_inches, height_in_inches))
    plt.imshow(deblurred_images.squeeze())
    plt.axis('off')
    plt.savefig(processed_image_path)
    plt.clf()

def explain_lime_single_image(model, image):
    explainer = lime_image.LimeImageExplainer()
    # Explain prediction
    explanation = explainer.explain_instance(image.astype('double'), model.predict, top_labels=5, hide_color=0, num_samples=1000)

    # Get the label with the highest probability
    label = explanation.top_labels[0]

    # Show the explanation for the top label
    temp, mask = explanation.get_image_and_mask(label, positive_only=True, num_features=5, hide_rest=False)
    plt.figure(figsize=(width_in_inches, height_in_inches))
    display_img = mark_boundaries(temp / 2 + 0.5, mask)
    plt.imshow(display_img)
    plt.title(f'Explanation for Label {label}')
    plt.axis('off')
    plt.savefig(lime_segment_boundries_path)
    plt.clf()
    
    plt.figure(figsize=(width_in_inches, height_in_inches))
    ind =  explanation.top_labels[0]
    #Map each explanation weight to the corresponding superpixel
    dict_heatmap = dict(explanation.local_exp[ind])
    heatmap = np.vectorize(dict_heatmap.get)(explanation.segments)
    #Plot. The visualization makes more sense if a symmetrical colorbar is used.
    plt.imshow(heatmap, cmap = 'RdBu', vmin  = -heatmap.max(), vmax = heatmap.max())
    plt.colorbar()
    plt.savefig(lime_segment_output_path)

def f(x):
    model = load_model(shap_cnn_model)
    tmp = x.copy()
    return model(tmp)

# Resize each image in the test set
def resize_for_shap(img):
    resized_images_test = []
    if img.dtype == np.float64:
        img = (img * 255).astype(np.uint8)
    resized_img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_img_gray = np.expand_dims(resized_img_gray, axis=-1)
    resized_images_test.append(resized_img_gray)
    resized_images_test_np = np.array(resized_images_test)
    return resized_images_test_np

def expalin_shap_single_image(image):
    image = resize_for_shap(image)
    masker_blur = shap.maskers.Image("blur(200,200)", image[0].shape)
    explainer = shap.Explainer(f, masker_blur, output_names=list(range(4)))
    shap_values_ = explainer(np.array(image)[[0]], max_evals=10000, batch_size=50 )
    fig = shap.image_plot(shap_values_,labels = ['glioma', 'meningioma', 'notumor', 'pituitary'], show=False)
    plt.savefig(shap_output_path)


def pre_process_image(img_path):
    image_size = 200
    image = convert_binary_to_image(img_path)
    # image = cv2.imread(img_path,0) # load images in gray.
    image = cv2.bilateralFilter(image, 2, 50, 50) # remove images noise.
    image = cv2.applyColorMap(image, cv2.COLORMAP_BONE) # produce a pseudocolored image.
    image = cv2.resize(image, (image_size, image_size)) # resize images into 200*200.
    image = np.array(image) / 255.0
    return image

def convert_image_to_binary(img_path):
    # Open the file in binary read mode
    with open(img_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def removing_old_folders():
    saved_directory = f"{os.getcwd()}/output/{(datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')}"
    if os.path.isdir(saved_directory):
        os.rmdir(saved_directory)

def return_all_images(img_path):
    # removing_old_folders()
    # Reading img
    image = pre_process_image(img_path)
    # 
    if not os.path.exists(saving_directory):
        # If the directory doesn't exist, create it
        os.makedirs(saving_directory)
    # # # Load the model
    model = load_model(cnn_model)

    denoise_and_deblur_images(np.expand_dims(image, axis=0))
    explain_lime_single_image(model, image)
    expalin_shap_single_image(image)
    
    return { "processed_image_path": processed_image_path,
             "lime_segment_boundries":  lime_segment_boundries_path,
             "lime_segment":  lime_segment_output_path, 
             "shap_output": shap_output_path
            }

def do_basic_analysis(img_path):
    # Reading img
    image = pre_process_image(img_path)
    model = load_model(cnn_model)
    # # Prediction of class
    probabilities = model.predict(np.expand_dims(image,axis=0))
    predicted_class = np.argmax(probabilities)
    print(predicted_class)

    probabilities_dict = {}
    for i, prob in enumerate(np.asarray(probabilities[0])):
        probabilities_dict[output_classes.get(i)] = str(round(prob*100, 3))
    print(probabilities_dict)
    return { "predicted_class" : output_classes.get(predicted_class),
             "probabilities": probabilities_dict
            }


def convert_binary_to_image(binary_data):
    # Convert binary data to a NumPy array of unsigned integers
    image_array = np.frombuffer(binary_data, dtype=np.uint8)
    # Decode the array into an image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

if __name__ == "__main__":
    # Temp code
    # temp_img = "/Users/saicharan/Sai Charan/MS/Master_Project/models/Te-gl_0024.jpg"
    # print(return_all_images(temp))
    pass
    

