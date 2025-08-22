const Transcript = ({ text }) => {
  return (
    <div className="transcript">
      <h2>Transcript</h2>
      <div className="transcript-content">
        {text}
      </div>
    </div>
  );
};

export default Transcript;