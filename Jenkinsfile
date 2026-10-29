pipeline {
    agent any

    environment {
        IMAGE = 'vasanth45/visitor-app'
        TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt pytest
                    python -m pytest
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
            }
        }

        stage('Push image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push $IMAGE:$TAG
                        docker push $IMAGE:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        sed -i "s|image: .*/visitor-app:.*|image: $IMAGE:$TAG|" k8s/web.yaml
                        kubectl apply -f k8s/redis.yaml
                        kubectl apply -f k8s/web.yaml
                        kubectl rollout status deployment/visitor-app --timeout=120s
                    '''
                }
            }
        }
    }

    post {
        success { echo "Deployed $IMAGE:$TAG" }
        failure { echo 'Pipeline failed. Check the stage that is red.' }
        always  { sh 'docker logout || true' }
    }
}
