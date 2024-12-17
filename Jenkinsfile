pipeline{
    agent any 
    tool{
        nodejs 'node18'
    }
    stages{
        stage('Node Test'){
            steps{
                sh "node -v && npm -v"

            }
        }
    }
}