pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                dir('lesson_31') {
                    bat 'python --version'
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                    bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            steps {
                dir('lesson_31') {
                    bat 'if not exist reports mkdir reports'
                    bat 'venv\\Scripts\\python -m pytest --junitxml=reports\\test-results.xml'
                }
            }
        }
    }

    post {
        always {
            junit 'lesson_31/reports/test-results.xml'
        }
    }
}