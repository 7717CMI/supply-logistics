# 🚀 Supply Logistics Dashboard

A modern, interactive dashboard for freight logistics analytics built with Plotly Dash.

## 🌟 Features

- **Modern Light Theme** - Professional glass morphism design
- **Interactive Charts** - Equipment distribution, rate analysis, geographic insights
- **Real-time Data** - Live freight load analytics
- **Responsive Design** - Works on all devices
- **Production Ready** - Deployed on Render.com

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
python app.py
```
Dashboard will be available at: http://localhost:8050

### Deploy on Render.com
1. Connect this repository to Render
2. Deploy using the included `render.yaml` configuration
3. Your dashboard will be live automatically

## 📊 Dashboard Sections

- **Key Metrics** - Total loads, average rates, distances, equipment types
- **Equipment Analysis** - Interactive pie chart showing equipment distribution
- **Rate Distribution** - Histogram of freight rates
- **Geographic Insights** - Load origins by state
- **Correlation Analysis** - Distance vs rate scatter plot
- **Data Table** - Detailed load information with sorting and pagination

## 🛠️ Technical Stack

- **Python 3.11.9**
- **Plotly Dash** - Interactive web applications
- **Dash Bootstrap Components** - Modern UI components
- **Gunicorn** - Production WSGI server

## 📁 Project Structure

```
├── app.py              # Main dashboard application
├── nextload.json       # Sample freight data
├── requirements.txt    # Python dependencies
├── render.yaml        # Render.com deployment config
├── Procfile           # Process configuration
├── runtime.txt        # Python version
└── README.md          # This file
```

## 🎯 Live Demo

Deployed dashboard: [Your Render URL]

## 📝 License

This project is open source and available under the MIT License.