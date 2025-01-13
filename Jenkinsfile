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
                        catchError(message: 'QualityGate Error') {
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
                            /*timeout(time: 60, unit: 'SECONDS') {
                                catchError(message: 'Quality gate Error') {
                                    waitForQualityGate abortPipeline: false
                                }
                            }*/
                        }
                    }
                }
            }
        }
        stage("Docker Build and Push"){
            steps{
                script{
                    image = docker.build("markmama/solar-app:$BUILD_NUMBER")
                    echo "Branch name: ${env.BRANCH_NAME}"

                    withDockerRegistry(credentialsId: 'dockerreg', url: '') {
                        image.push()
                    }  
                }
            }
        }
        stage("Trivy Image Scan"){
            steps{
                sh """
                trivy image  --severity  LOW,MEDIUM,HIGH  markmama/solar-app:$BUILD_NUMBER --format json -o trivy-modrate-vul.json

                trivy image  --severity  CRITICAL  markmama/solar-app:$BUILD_NUMBER --format json -o trivy-critical-vul.json

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
        stage("Helm Chart K8 Config Update"){
            when{
                branch 'main'
            }
            steps{
                sh "git clone https://github.com/syed-hassan-ops/solar-system-gitea.git"
                dir("solar-system-gitea"){
                    script{
                        withEnv(["KUBECONFIG=/var/lib/jenkins/.minikube/config"]) {
                            sh "helm upgrade --install  solar-app -n sola-app --set image.tag=$BUILD_NUMBER ./helmchart/solar-app/"
                        }
                         
                    }
                   
                }
            }
        }
        stage('DAST - OWASP ZAP') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    #### REPLACE below with Kubernetes http://192.168.49.2:30012/api-docs/ #####
                    chmod 777 $(pwd)
                    docker run -v $(pwd):/zap/wrk/:rw --network=minikube ghcr.io/zaproxy/zaproxy zap-api-scan.py \
                    -t http://192.168.49.2:30012/api-docs/ \
                    -f openapi \
                    -r zap_report.html \
                    -w zap_report.md \
                    -J zap_json_report.json \
                    -x zap_xml_report.xml \
                    -c ignore_rules
                '''
            }
        }
        stage("Report-Report"){
            steps{
                withAWS(credentials: 'aws-ec2-s3-access', region: 'ap-south-1') {
                    sh """
                        mkdir report-$BUILD_NUMBER
                        cp dependency* trivy* zap_report * ./report-$BUILD_NUMBER/
                        ll ./report-$BUILD_NUMBER/
                    """

                    s3Upload acl: 'Private', bucket: 'solar-app-jenkins-report', cacheControl: '', excludePathPattern: '', file: 'report-$BUILD_NUMBER', includePathPattern: '', metadatas: [''], path: 'jenkins-report-$BUILD_NUMBER', redirectLocation: '', sseAlgorithm: '', tags: '', text: '', workingDir: ''
                }
            }
        }
        stage("Reports & Tests"){
            steps{
                catchError(message: 'Quality gate Error') {
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'dependency-check-jenkins.html', reportName: 'Deoendency Report', reportTitles: '', useWrapperFileDirectly: true])
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'trivy-critical-vul.html', reportName: 'Trivy Critical Report', reportTitles: '', useWrapperFileDirectly: true])
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'trivy-modrate-vul.html', reportName: 'Trivy Moderate Report', reportTitles: '', useWrapperFileDirectly: true])
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: './', reportFiles: 'zap_report.html', reportName: 'DAST Report', reportTitles: '', useWrapperFileDirectly: true])


                    junit stdioRetention: '', testResults: 'dependency-check-junit.xml'
                    junit stdioRetention: '', testResults: 'trivy-critical-vul.xml'
                    junit stdioRetention: '', testResults: 'trivy-modrate-vul.xml'
                }
            }
        }
    }
    post {
        always {
            script {
                if (fileExists('solar-system-gitea')) {
                    sh 'rm -rf solar-system-gitea'
                }
            }
        }
    }
}