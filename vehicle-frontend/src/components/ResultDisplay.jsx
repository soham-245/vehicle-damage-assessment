function ResultDisplay({ results, loading }) {
  if (loading) {
    return (
      <div style={{ marginTop: "20px" }}>
        <h3>Results</h3>
        <p>Analyzing image...</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div style={{ marginTop: "20px" }}>
        <h3>Results</h3>
        <p>No results yet</p>
      </div>
    );
  }

  const totalCost = results.reduce((sum, item) => sum + item.cost, 0);

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Results</h3>

      {results.map((item, index) => (
        <div key={index} style={{ marginBottom: "15px" }}>

          <img
            src={`data:image/jpeg;base64,${item.image}`}
            alt="crop"
            style={{
              width: "100%",
              maxHeight: "150px",
              objectFit: "contain",
              borderRadius: "8px"
            }}
          />

          <div>
            {item.part} → {item.severity} → {item.action} → ₹{item.cost}
          </div>

        </div>
      ))}

      <hr />

      <strong>Total: ₹{totalCost}</strong>
    </div>
  );
}

export default ResultDisplay;