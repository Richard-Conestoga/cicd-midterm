pipeline {
    agent any

    environment {
        TEAM_EMAIL = 'rbiscazzi3530@conestogac.on.ca'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning GitHub repository...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Starting build process...'
                sh 'echo "Compiling source code..."'
                sh 'sleep 1'
                sh 'echo "Build complete."'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'echo "Test 1 passed"'
                sh 'echo "All tests succeeded!"'
            }
        }
    }

    post {
        success {
            echo '✅ Build and tests successful!'
            emailext (
                subject: "SUCCESS: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "Good news! The build and tests succeeded.\n\nCheck details here: ${env.BUILD_URL}",
                to: "${TEAM_EMAIL}"
            )
        }
        failure {
            echo '❌ Build or tests failed!'
            emailext (
                subject: "FAILURE: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "The build or tests failed. Check logs here: ${env.BUILD_URL}",
                to: "${TEAM_EMAIL}"
            )
        }
    }
}
