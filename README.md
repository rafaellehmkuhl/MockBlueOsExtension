# Mock BlueOS Extension

A sample BlueOS extension demonstrating basic functionality. This extension provides a simple user interface and WebSocket API for communication.

## Features

- RESTful API endpoints
- WebSocket for real-time communication
- Modern web interface
- Status monitoring

## Installation

This extension can be installed from the BlueOS Extensions Bazaar.

## Manual Installation

If you want to install this extension manually:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MockBlueOsExtension.git
   ```

2. Build the Docker image:
   ```bash
   docker build -t yourusername/mock-blueos-extension:latest .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 yourusername/mock-blueos-extension:latest
   ```

## Development

### Prerequisites

- Docker
- Python 3.9+
- Node.js (optional, for advanced frontend development)

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MockBlueOsExtension.git
   cd MockBlueOsExtension
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend for development:
   ```bash
   python -m src.backend.main
   ```

4. Access the web interface at http://localhost:8000/frontend/

## Extension Structure

- `src/backend/` - Python backend code
- `src/frontend/` - Web frontend (HTML, CSS, JavaScript)
- `Dockerfile` - Docker configuration with extension metadata
- `requirements.txt` - Python dependencies

## API Documentation

### REST API

- `GET /` - Basic API information
- `GET /status` - Get extension status

### WebSocket API

Connect to `/ws` for real-time communication.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please file an issue on the GitHub repository.