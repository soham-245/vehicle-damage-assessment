function CarSelector({ carModel, setCarModel, carModels }) {
  return (
    <div style={{ marginTop: "15px" }}>
      <p>Select Car Model:</p>
      <select
        value={carModel}
        onChange={(e) => setCarModel(e.target.value)}
        style={{ width: "100%", padding: "5px" }}
      >
        <option value="">-- Select --</option>

        {carModels.map((model, index) => (
          <option key={index} value={model.toLowerCase()}>
            {model}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CarSelector;