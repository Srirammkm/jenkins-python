pipeline {
  environment {
    REGION = "ap-southeast-1"
    CLUSTER = "production-cluster"
    registry = "srirammk18/flask-prod"
    registryCredential = 'dockerhub_id'
    dockerImage = ''
  }
  agent any //{ label 'worker01' }  
  stages {
    stage('Build with Docker') {
      steps {
        script {
          dockerImage = docker.build registry +":${BUILD_NUMBER}"
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
            kubectl apply -f service.yml
           '''
      }
    }
  }
}
