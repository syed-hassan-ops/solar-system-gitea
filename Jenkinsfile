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
                sh "npm install"

            }
        }
        stage("SAST CODE & DEPENDECY"){
            parallel{
                stage("SAST Testing"){
                    steps{
                        catchError(buildResult: 'UNSTABLE', message: 'Test Result Made this Unstable No worriers we can continue this Pipeline') {
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
                stage("Code Analysis"){
                    steps{
                        withSonarQubeEnv('sonarqube-scanner') {
                            sh """
                            "${SCANNER}/bin/sonar-scanner" \
                            -Dsonar.sources=./ \
                            -Dsonar.projectName=Solar-System-App \
                            -Dsonar.javascript.lcov.reportPaths=./coverage/lcov.info \
                            -Dsonar.projectKey=syed-hassan-ops-netflix_solar-system-app \
                            -Dsonar.organization=syed-hassan-ops-netflix
                            """
                        }
                        timeout(time: 60, unit: 'SECONDS') {
                            catchError(message: 'Quality gate Error') {
                                waitForQualityGate abortPipeline: true
                            }
                        }
                    }
                }
            }
        }
        stage("Trivy Image Scan"){
            steps{
                sh """
                trivy image  --severity  LOW,MEDIUM,HIGH  solar-app:0.1 --format json -o trivy-modrate-vul.json

                trivy image  --severity  CRITICAL  solar-app:0.1 --format json -o trivy-critical-vul.json

                """
            }
            post{
                always{
                        sh"""
                        trivy convert -f template -t "@/usr/local/share/trivy/templates/html.tpl" -o trivy-critical-vul.html trivy-critical-vul.json
                        trivy convert -f template -t "@/usr/local/share/trivy/templates/html.tpl" -o trivy-modrate-vul.html trivy-modrate-vul.json

                        trivy convert -f template -t "@/usr/local/share/trivy/templates/junit.tpl" -o trivy-critical-vul.xml trivy-critical-vul.json
                        trivy convert -f template -t "@/usr/local/share/trivy/templates/junit.tpl" -o trivy-modrate-vul.xml trivy-modrate-vul.json
                        """
                    }
            }
        }
        stage("Reports & Tests"){
            steps{
                catchError(buildResult: 'UNSTABLE', message: 'Test Result Made this Unstable No worriers we can continue this Pipeline') {
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'dependency-check-jenkins.html', reportName: 'Deoendency Report', reportTitles: '', useWrapperFileDirectly: true])
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'trivy-critical-vul.html', reportName: 'Trivy Critical Report', reportTitles: '', useWrapperFileDirectly: true])
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'trivy-modrate-vul.html', reportName: 'Trivy Moderate Report', reportTitles: '', useWrapperFileDirectly: true])

                    junit stdioRetention: '', testResults: 'dependency-check-junit.xml'
                    junit stdioRetention: '', testResults: 'trivy-critical-vul.xml'
                    junit stdioRetention: '', testResults: 'trivy-modrate-vul.xml'
                }
            }
        }
    }
}