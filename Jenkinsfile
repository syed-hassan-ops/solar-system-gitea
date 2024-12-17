pipeline{
    agent any 
    tools{
        nodejs 'node23'
    }
    stages{
        stage('Node package Install'){
            steps{
                sh "npm install --no-audit"

            }
        }
    }
}