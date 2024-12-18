pipeline{
    agent any 
    environment {
        SCANNER = tool 'sonar-scanner'
    }
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
                
            }
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
        stage("Code Analysis"){
            steps{
                withSonarQubeEnv('sonarqube-scanner') {
                    sh """
                    "${SCANNER}/bin/sonar-scanner" \
                    -Dsonar.projectName=Solar-System-App \
                    -Dsonar.projectKey=syed-hassan-ops-netflix_solar-system-app \
                    -Dsonar.organization=syed-hassan-ops-netflix
                    """
                }
            }
        }
        stage("NPM Test"){
            steps{
                sh "npm test"
            }
        }
        stage("Reports & Tests"){
            steps{

                publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'dependency-check-jenkins.html', reportName: 'HTML Report', reportTitles: '', useWrapperFileDirectly: true])

                junit stdioRetention: '', testResults: 'dependency-check-junit.xml'
            }
        }
    }
}