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
        stage("SAST Testing"){
            parallel{
                stage("NPM TEST"){
                    steps{
                        sh "npm audit --audit-level=critical && echo $?"
                    }
                }
                stage("OWASP Dependency Check"){
                    steps{
                        dependencyCheck additionalArguments: '''--scan \'./\'
                            --format \'ALL\'
                            prettyPrint''', odcInstallation: 'OWASP_DC'
                        
                    }
                }
            }
        }
    }
}