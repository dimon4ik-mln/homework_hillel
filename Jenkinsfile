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
                bat 'python --version'
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'venv\\Scripts\\pytest --junitxml=reports\\test-results.xml'
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/test-results.xml', allowEmptyResults: false
            step([$class: 'Mailer',
                notifyEveryUnstableBuild: true,
                recipients: 'InsertYour@Mail.Here',
                sendToIndividuals: false])
        }
    }
}