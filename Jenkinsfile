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
                        sh '''
                            npm audit --audit-level=critical  
                            echo $?
                        '''
                    }
                }
                stage("OWASP Dependency Check"){
                    steps{
                        dependencyCheck additionalArguments: '''
                            --scan \'./\'
                            --out \'./\'  
                            --format \'ALL\'
                            --prettyPrint''', odcInstallation: 'OWASP_DC'
                        
                        dependencyCheckPublisher failedTotalCritical: 1, pattern: 'dependency-check-report.xml', stopBuild: false
                        
                    }
                }
            }
        }
    }
}