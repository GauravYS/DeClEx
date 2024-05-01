let uploadedFile = null;
let count = 0;
endpoint = "http://34.16.167.233:8000/";

function uploadImage() {
  const imageInput = document.getElementById("imageInput");
  uploadedFile = imageInput.files[0];

  if (uploadedFile) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const uploadedImage = document.getElementById("uploadedImage");
      uploadedImage.src = event.target.result;
      uploadedImage.style.display = "block";
    };
    reader.readAsDataURL(uploadedFile);
  }
}

async function analyzeImage() {
  if (!uploadedFile) {
    console.error("Please upload an image first.");
    return;
  }

  document.getElementById("loadingSpinner").style.display = "block"; // Show loading spinner

  const formData = new FormData();
  formData.append("image", uploadedFile);

  try {
    const response = await fetch(endpoint+ "complete_analysis", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      console.log("Analysis result:", jsonResponse);
      // const predicted_class = jsonResponse.predicted_class;

      // document.querySelector(
      //   ".predicted"
      // ).innerText = `Predicted : ${predicted_class}`;

      await displayAnalysisResult(jsonResponse.processed_image_path);
      await displayAnalysisResult(jsonResponse.lime_segment_boundries);
      await displayAnalysisResult(jsonResponse.lime_segment);
      await displayAnalysisResult(jsonResponse.shap_output);
      document.getElementById("loadingSpinner").style.display = "none"; // Hide loading spinner
    } else {
      console.error("Failed to analyze image:", response.status);
      document.getElementById("loadingSpinner").style.display = "none"; // Hide loading spinner
    }
  } catch (error) {
    console.error("Error analyzing image:", error);
    document.getElementById("loadingSpinner").style.display = "none"; // Hide loading spinner
  }
}

async function displayAnalysisResult(resultPath) {
  const explain = [
    "Processed Images - The images are deblurred as well as denoised",
    "Lime Segmentation - This will allow clinicians to focus on the most influential areas of the Brain MRI. ",
    "LIME Heatmaps - This gives a detailed representation of tumor presence/absence by color-coding different areas. Dark Blue represents high importance and dark red represents low importantce areas repectively.",
    "SHAP- This method takes into account the most imprtant superpixels while generating a prediction.",
  ];
  let newDiv = document.createElement("div");
  newDiv.classList.add("result-item");

  try {
    const response = await fetch(endpoint + "images", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ file: resultPath }),
    });
    if (response.ok) {
      const imageData = await response.blob();
      const imageUrl = URL.createObjectURL(imageData);
      const resultContainer = document.getElementById("analysisResult");

      let newImg = document.createElement("img");
      let newExplain = document.createElement("p");
      newExplain.innerText = explain[count]; // Use the current count value
      count = (count + 1) % explain.length; // Increment and reset the count as necessary

      newImg.src = imageUrl;
      newImg.alt = "Analysis Result";
      newDiv.appendChild(newImg);
      newDiv.appendChild(newExplain);

      // Append the new div to the container
      resultContainer.appendChild(newDiv);
    } else {
      console.error("Failed to fetch image:", response.status);
    }
  } catch (error) {
    console.error("Error fetching image:", error);
  }
}

//  **************** POP UP ********************************
async function detailedAnalysis() {
  if (!uploadedFile) {
    console.error("Please upload an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", uploadedFile);

  try {
    const response = await fetch(endpoint + "analyse", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const jsonResponse = await response.json();

      // Set the predicted class text
      document.querySelector(
        ".predicted"
      ).innerText = `Predicted: ${jsonResponse.predicted_class}`;

      // Populate the probabilities table
      const probabilities = jsonResponse.probabilities;
      const tableBody = document
        .getElementById("probabilitiesTable")
        .getElementsByTagName("tbody")[0];
      tableBody.innerHTML = ""; // Clear previous entries

      Object.keys(probabilities).forEach((key) => {
        let row = tableBody.insertRow();
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        cell1.textContent = key;
        cell2.textContent = `${probabilities[key]}%`;
      });

      // Display the popup
      document.getElementById("predictionPopup").style.display = "block";
    } else {
      console.error("API call failed with status: ", response.status);
    }
  } catch (error) {
    console.error("Error while fetching prediction:", error);
    document.getElementById("loadingSpinner").style.display = "none"; // Hide loading spinner
  }
}

function closePopup() {
  document.getElementById("predictionPopup").style.display = "none";
}
