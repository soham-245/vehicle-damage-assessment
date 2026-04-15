function ImageUpload({ handleImageChange, preview }) {
  return (
    <div style={{ marginTop: "15px" }}>
      <p>Upload Image:</p>
      <input type="file" onChange={handleImageChange} />

      {preview && (
        <div style={{ marginTop: "10px" }}>
          <p>Preview:</p>
          <img
            src={preview}
            alt="preview"
            style={{
              width: "100%",
              maxHeight: "200px",
              objectFit: "contain",
              borderRadius: "8px",
            }}
          />
        </div>
      )}
    </div>
  );
}

export default ImageUpload;