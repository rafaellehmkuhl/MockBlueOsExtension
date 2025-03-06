// DOM Elements
const statusLight = document.getElementById('status-light');
const statusText = document.getElementById('status-text');
const actionButton = document.getElementById('action-button');
const refreshButton = document.getElementById('refresh-button');
const messageInput = document.getElementById('message-input');
const sendMessageButton = document.getElementById('send-message');
const messageLog = document.getElementById('message-log');

// WebSocket Connection
let socket = null;
let connected = false;

// API Base URL - adjust if needed
const API_BASE_URL = window.location.origin;

// Initialize the application
window.addEventListener('DOMContentLoaded', () => {
    init();
});

// Initialize function
async function init() {
    // Check status
    await checkStatus();

    // Set up event listeners
    setupEventListeners();

    // Connect to WebSocket
    connectWebSocket();
}

// Check the extension status
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();

        if (data.status === 'running') {
            updateStatus(true, 'Extension is running');
        } else {
            updateStatus(false, 'Extension is not running');
        }
    } catch (error) {
        console.error('Error checking status:', error);
        updateStatus(false, 'Error connecting to extension');
    }
}

// Update the status indicator
function updateStatus(isOnline, message) {
    statusLight.className = 'status-light ' + (isOnline ? 'online' : 'offline');
    statusText.textContent = message;
}

// Set up event listeners
function setupEventListeners() {
    // Action button
    actionButton.addEventListener('click', async () => {
        addToLog('Performing action...', 'sent');

        try {
            const response = await fetch(`${API_BASE_URL}/`);
            const data = await response.json();
            addToLog(`Response: ${data.message}`, 'received');
        } catch (error) {
            console.error('Error performing action:', error);
            addToLog(`Error: ${error.message}`, 'received');
        }
    });

    // Refresh button
    refreshButton.addEventListener('click', () => {
        checkStatus();
    });

    // Send message button
    sendMessageButton.addEventListener('click', () => {
        sendMessage();
    });

    // Allow Enter key to send messages
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
}

// Connect to WebSocket
function connectWebSocket() {
    // Replace with your WebSocket URL
    const wsUrl = `ws://${window.location.host}/ws`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        connected = true;
        addToLog('WebSocket connected', 'received');
    };

    socket.onmessage = (event) => {
        addToLog(`Received: ${event.data}`, 'received');
    };

    socket.onclose = () => {
        connected = false;
        addToLog('WebSocket disconnected', 'received');

        // Try to reconnect after a delay
        setTimeout(() => {
            connectWebSocket();
        }, 5000);
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        addToLog('WebSocket error', 'received');
    };
}

// Send a message via WebSocket
function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    if (connected && socket) {
        socket.send(message);
        addToLog(`Sent: ${message}`, 'sent');
        messageInput.value = '';
    } else {
        addToLog('Cannot send message: WebSocket not connected', 'received');
    }
}

// Add a message to the log
function addToLog(message, type) {
    const logEntry = document.createElement('div');
    logEntry.className = `log-message ${type}`;

    const timestamp = new Date().toLocaleTimeString();
    logEntry.textContent = `[${timestamp}] ${message}`;

    messageLog.appendChild(logEntry);

    // Scroll to bottom
    messageLog.scrollTop = messageLog.scrollHeight;
}