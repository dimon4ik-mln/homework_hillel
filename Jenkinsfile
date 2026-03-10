pipeline {
    agent any

    environment {
        BASE_URL = 'http://127.0.0.1:5000'
    }

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

        stage('Start API') {
            steps {
                dir('lesson_31') {
                    bat 'start /B venv\\Scripts\\python cars_app.py'
                    bat 'timeout /t 5 /nobreak'
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