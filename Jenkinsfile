pipeline{
    agent any 
    tool{
        nodejs 'node18'
    }
    stages{
        stage('Node Test'){
            step{
                sh "node -v && npm -v"

            }
        }
    }
}