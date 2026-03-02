const form = document.getElementById("tumorForm");
const resultDiv = document.getElementById("result");
const resultText = document.getElementById("resultText");
const previewImage = document.getElementById("previewImage");

const nameInput = document.getElementById("name");
const ageInput = document.getElementById("age");
const mriImageInput = document.getElementById("mriImage");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!mriImageInput.files[0]) {
    alert("Please select an MRI image.");
    return;
  }

  const formData = new FormData();
  formData.append("name", nameInput.value);
  formData.append("age", ageInput.value);
  formData.append("mri_image", mriImageInput.files[0]);

  // Show preview
  previewImage.src = URL.createObjectURL(mriImageInput.files[0]);

  resultDiv.classList.remove("hidden");
  resultText.textContent = "Analyzing image...";

  try {
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(errText || "Server error");
    }

    const data = await response.json();

    if (data.error) {
      resultText.textContent = "❌ Error: " + data.error;
      return;
    }

    const conf = typeof data.confidence === "number" ? data.confidence : null;

// Backend returns: tumor_detected (0 or 1) and confidence
const hasTumor = data.tumor_detected === 1;

if (hasTumor) {
  resultText.textContent = `⚠️ Tumor Detected (confidence: ${(data.confidence * 100).toFixed(1)}%)`;
} else {
  resultText.textContent = `✅ No Tumor Detected `;
}
  
  } catch (err) {
    console.error(err);
    resultText.textContent = "❌ Request failed: " + err.message;
  }
});
