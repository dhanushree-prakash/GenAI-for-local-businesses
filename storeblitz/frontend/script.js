document.getElementById("contentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    business_name: document.getElementById("business_name").value,
    category: document.getElementById("category").value,
    content_type: document.getElementById("content_type").value,
    language: document.getElementById("language").value,
    detail: document.getElementById("detail").value,
  };

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "⏳ Generating content...";
  resultDiv.classList.remove("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const json = await response.json();

    if (json.content) {
      resultDiv.innerHTML = `<strong>✅ Generated Content:</strong><br><br>${json.content}`;
    } else {
      resultDiv.innerHTML = `❌ Error: ${json.error || "Something went wrong."}`;
    }
  } catch (err) {
    resultDiv.innerHTML = `❌ Request failed: ${err.message}`;
  }
});
