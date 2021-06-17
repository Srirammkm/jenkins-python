pipeline {
  environment {
    REGION = "ap-southeast-1"
    CLUSTER = "development-cluster"
    registry = "srirammk18/flask-dev"
    registryCredential = 'dockerhub_id'
    dockerImage = ''
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
          apt install -y unzip
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip awscliv2.zip
          ./aws/install
          '''
      }
    }
    stage('Install kubectl and update kube-config file') {
      steps {
        sh '''
            curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl
            chmod +x ./kubectl
            mv ./kubectl /usr/local/bin/kubectl
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
