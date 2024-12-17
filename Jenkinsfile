pipeline{
    agent any 
    tools{
        nodejs 'node18'
    }
    stages{
        stage('Node package Install'){
            steps{
                sh "npm install --no-audit"

            }
        }
    }
}