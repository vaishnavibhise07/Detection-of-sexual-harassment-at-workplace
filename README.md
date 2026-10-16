Detection of harassment

This web application is a prototype designed to monitor webcam frames and identify potential distress indicators using Computer Vision and Deep Learning techniques. It uses DeepFace to analyze two facial attributes:

- **Gender**
- **Emotion**

Based on the detected emotion, the system assigns a rule-based risk score and triggers evidence capture when a high-risk condition is identified.

### Working Process

**1. Live Camera Monitoring**

OpenCV captures video frames from the webcam, which are analyzed using DeepFace to identify facial attributes and dominant emotions.

**2. Risk Assessment**

The system assigns a high-risk score for detected emotions such as Angry, Fear, or Sad, and a low-risk score for other emotions.

**3. Evidence Capture and Storage**

When the risk score exceeds the configured threshold, the system captures an image and stores incident details, including the timestamp, emotion, gender, and risk score, in an SQLite database.

**4. Monitoring Dashboard**

A web interface displays live detection results, risk indicators, and an HR dashboard prototype for reviewing incident evidence.

### Technologies Used

- **Python & FastAPI:** Backend development and API endpoints.
- **OpenCV:** Webcam capture and video streaming.
- **DeepFace:** Facial gender and emotion analysis.
- **SQLite & SQLAlchemy:** Incident data storage and database operations.
- **HTML, JavaScript & Tailwind CSS:** Monitoring interface and dashboard.

### Key Features and Outcomes

- Real-time webcam monitoring and facial attribute analysis.
- Rule-based risk scoring and high-risk alerts.
- Automatic evidence image capture and incident logging.
- Database-backed incident storage.
- Web-based monitoring interface and HR dashboard prototype.

### Project Background

The project explores the integration of Computer Vision, facial attribute analysis, backend APIs, and database management in a workplace safety monitoring workflow. It is a proof of concept; facial emotion alone cannot establish whether harassment has occurred, and further development is required for reliable real-world use.
