# Weather Forecast Application

A Python application that fetches and displays weather forecasts for multiple Canadian cities using the OpenWeatherMap API.

## Repository Structure

```
.
├── weather.py              # Main application code
├── test_weather.py         # Unit tests
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env                   # Environment variables (local only, not committed)
├── .gitignore            # Git ignore rules
└── .github/
    └── workflows/
        └── cicd.yml      # CI/CD pipeline configuration
```

## Prerequisites

- Python 3.11 or higher
- OpenWeatherMap API key (get one free at [openweathermap.org](https://openweathermap.org/api))
- Docker (optional, for containerized deployment)

## Local Development

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Set Up Environment

Create a `.env` file in the project root:

```bash
APPID=your_openweathermap_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python weather.py
```

This will display weather forecasts for Toronto, Kitchener, and Ottawa.

### 5. Run Tests

```bash
python -m unittest test_weather.py -v
```

## Docker Usage

### Build Docker Image Locally

```bash
docker build -t weather-app .
```

### Run Docker Container

```bash
docker run -e APPID=your_api_key_here weather-app
```

### Pull from Docker Hub

Pull the latest image from Docker Hub:

```bash
docker pull <your-dockerhub-username>/weather-app:latest
```

Run the pulled image:

```bash
docker run -e APPID=your_api_key_here <your-dockerhub-username>/weather-app:latest
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Stages

1. **Build** - Compiles and verifies Python code
2. **Test** - Runs unit tests with coverage reporting
3. **Docker Build** - Creates Docker image
4. **Security Scan** - Scans image for vulnerabilities using Trivy
5. **Publish** - Pushes Docker image to Docker Hub

### Testing the CI/CD Pipeline

#### Setup Required Secrets

Before running the pipeline, add these secrets to your GitHub repository:

1. Go to **Settings → Secrets and variables → Actions**
2. Add the following secrets:
   - `APPID` - Your OpenWeatherMap API key
   - `DOCKERHUB_USERNAME` - Your Docker Hub username
   - `DOCKERHUB_TOKEN` - Docker Hub access token

#### Trigger the Pipeline

The pipeline automatically runs on every push to the `main` branch:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

#### Monitor Pipeline Execution

1. Go to the **Actions** tab in your GitHub repository
2. Click on the latest workflow run
3. Monitor each job (Build, Test, Docker Build, Security Scan, Publish)
4. View logs for any failures

#### Simulate a Test Failure

To test that the pipeline catches errors:

1. Add a failing test to `test_weather.py`:

```python
def test_intentional_failure(self):
    """This test will fail intentionally"""
    self.assertEqual(1, 2, "Testing pipeline failure detection")
```

2. Commit and push:

```bash
git add test_weather.py
git commit -m "Test pipeline failure detection"
git push origin main
```

3. The pipeline will fail at the **Test** phase and prevent deployment

4. Remove the failing test and push again to see the pipeline succeed


Updating this project to work with Jenkins.