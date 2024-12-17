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
                        sh "npm audit --audit-level=critical"
                        sh "npm audit fix --force"  
                            
                        
                    }
                }
                stage("OWASP Dependency Check"){
                    steps{
                        dependencyCheck additionalArguments: '''
                            --scan \'./\'
                            --out \'./\'  
                            --format \'ALL\'
                            --disableYarnAudit \
                            --prettyPrint''', odcInstallation: 'OWASP_DC'
                        
                        dependencyCheckPublisher failedTotalCritical: 5, pattern: 'dependency-check-report.xml', stopBuild: false
                        
                    }
                }
            }
        }
    }
}