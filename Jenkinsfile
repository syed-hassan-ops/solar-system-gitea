pipeline{
    agent any 
    tools{
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