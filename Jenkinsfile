pipeline {
  environment {
    REGION = "ap-southeast-1"
    CLUSTER = "production-cluster"
    registry = "srirammk18/flask-prod"
    registryCredential = 'dockerhub_id'
    dockerImage = ''
  }
  tools {
    docker 'docker'
  }
  agent any 
  stages {
    stage('Build with Docker') {
      steps {
        script {
        dockerImage = docker.build registry + ":final"
        }
      }
    }
    stage('Push the image to ICR') {
      steps {
        script {
          docker.withRegistry( '', registryCredential ) {
          dockerImage.push()
          }
        }
      }
    }
    stage('Install AWS Cloud CLI') {
      steps {
        sh '''
          sudo apt install -y unzip
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip awscliv2.zip
          sudo ./aws/install
          '''
      }
    }
    stage('Install kubectl and update kube-config file') {
      steps {
        sh '''
            curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl
            chmod +x ./kubectl
            sudo mv ./kubectl /usr/local/bin/kubectl
            kubectl version --client
            aws eks --region ${REGION} update-kubeconfig --name ${CLUSTER}
            '''
      }
    }
    stage('Deploy to EKS') {
      steps {
        sh '''
            kubectl apply -f deployment.yml
           '''
      }
    }
  }
}
