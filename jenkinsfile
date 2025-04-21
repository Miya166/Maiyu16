pipeline {
    agent any

    environment {
        IMAGE_NAME = 'pinhub-app'
        CONTAINER_NAME = 'pinhub-container'
        PORT = '5000'
    }

    stages {
        stage('Verify Files') {
            steps {
                echo 'Verifying the contents of the workspace...'
                sh 'ls -l'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image for PinHub...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                echo 'Stopping existing PinHub container (if any)...'
                sh 'docker stop $CONTAINER_NAME || true'
            }
        }

        stage('Remove Old Container') {
            steps {
                echo 'Removing old PinHub container (if any)...'
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }

        stage('Run New Container') {
            steps {
                echo 'Starting new PinHub container...'
                sh 'docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }

        stage('List Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo 'PinHub pipeline execution completed!'
        }
    }
}
