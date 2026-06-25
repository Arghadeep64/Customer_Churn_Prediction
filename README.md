# Customer Churn Prediction

A machine learning application to predict customer churn using Flask and Dash dashboard.

## Overview

This project aims to predict which customers are likely to churn (leave the service) using machine learning models. The application provides an interactive dashboard for visualizing predictions and model performance metrics.

## Features

- Customer churn prediction using ML models
- Interactive Dash dashboard for visualization
- Database integration for storing predictions
- Data preprocessing pipeline
- Model training and evaluation
- Batch prediction capability

## Project Structure

```
Customer_Churn_Prediction/
├── app.py                  # Main Flask/Dash application
├── requirements.txt        # Python dependencies
├── database/              # Database related files
├── dataset/               # Data files
├── models/                # ML model files
├── dashboard/             # Dash dashboard components
├── assets/                # CSS and static files
├── reports/               # Generated reports and charts
├── utils/                 # Helper functions
└── screenshots/           # Project screenshots
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure database connection in `utils/config.py`
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

Access the dashboard at `http://localhost:8050`

## Model Performance

- Accuracy: [To be updated]
- Precision: [To be updated]
- Recall: [To be updated]
- F1-Score: [To be updated]

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

MIT License
