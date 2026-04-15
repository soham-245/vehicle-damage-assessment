import { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import CarSelector from "./components/CarSelector";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [carModel, setCarModel] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const carModels = ["Swift", "i20", "Creta"];

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);

    if (file) {
      setPreview(URL.createObjectURL(file));
    }
  };

const handleSubmit = async () => {
  if (!image || !carModel) {
    alert("Please upload image and select car model");
    return;
  }

  setLoading(true);
  setResults(null);

  try {
    const formData = new FormData();
    formData.append("file", image);
    formData.append("car_model", carModel);

    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setResults(data.results);
  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong");
  }

  setLoading(false);
};

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Vehicle Damage Assessment</h1>

        <ImageUpload
          handleImageChange={handleImageChange}
          preview={preview}
        />

        <CarSelector
          carModel={carModel}
          setCarModel={setCarModel}
          carModels={carModels}
        />

        <button
          style={{
            ...styles.button,
            backgroundColor: loading ? "#999" : "#007bff",
            cursor: loading ? "not-allowed" : "pointer",
          }}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        <ResultDisplay results={results} loading={loading} />
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
  },
  card: {
    backgroundColor: "white",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
    width: "400px",
  },
  title: {
    textAlign: "center",
    margin: "0 0 20px 0",
    color: "#000",
  },
  button: {
    marginTop: "20px",
    width: "100%",
    padding: "10px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
};

export default App;