pipeline {
    agent any

    environment {
        IMAGE_NAME = 'pinhub-app'
        CONTAINER_NAME = 'pinhub-container'
        PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out the latest code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image for PinHub...'
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running PinHub container...'
                sh "docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests for PinHub container...'
                // Add any commands to test your app, e.g., curl or integration tests
                sh "curl http://localhost:${PORT}/health"  // Assuming you have a health endpoint
            }
        }
    }

    post {
        always {
            echo 'PinHub pipeline execution completed!'
        }
    }
}
