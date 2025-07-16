pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'stock_data'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your-username/your-stock-repo.git', branch: 'main'
            }
        }

        stage('Build and Run') {
            steps {
                script {
                    echo 'Building and running the containers...'
                    sh 'docker-compose down -v || true'
                    sh 'docker-compose build'
                    sh 'docker-compose up --abort-on-container-exit --exit-code-from fetcher'
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Cleaning up containers and volumes...'
                sh 'docker-compose down -v'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo '✅ Stock fetch succeeded!'
        }
        failure {
            echo '❌ Stock fetch failed. Check logs above.'
        }
    }
}
