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
                echo 'Verifying workspace contents...'
                sh 'ls -l'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
            }
        }

        stage('Remove Old Container') {
            steps {
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }

        stage('Running Containers') {
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
