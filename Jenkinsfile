pipeline {
    agent any

    tools{
        jdk 'openjdk11'
        maven 'Maven3'
    }

    environment {
        imageName = "basic-app:${env.BUILD_NUMBER}"
        pdfFilename = "trivy_repository_scan_${env.BUILD_NUMBER}"
        s3Bucket = "trivy-scans-pdf"
        awsProfile = "trivy-rwd"
    }

    stages {
        stage('GIT CHECKOUT') {
            steps {
                git branch: 'main', changelog: false, poll: false, url: 'https://github.com/AadiManchekar/Basic_Java_Project.git'
            }
        }
        stage('PRINT VERSIONS') {
            steps {
                script {
                    sh 'java -version'
                    sh 'mvn --version'
                    sh 'python3 --version'
                    sh 'docker --version'
                    sh 'aws --version'
                }
            }
        }
        stage('CODE COMPILE') {
            steps {
                sh "mvn clean compile"
            }
        }
        stage("TRIVY SCAN ON REPOSITORY") {
            steps {
                sh "trivy fs --security-checks vuln,config -f json -o trivy_repository_scan.json /root/.jenkins/workspace/test"
            }
        }
        stage('GENERATE TRIVY PDF AND UPLOAD TO S3') {
            steps {
                script {
                    sh "python3 json_to_html.py"

                    withAWS(credentials: 'aws-credentials', profileName: awsProfile) {
                    sh "aws s3 cp ${pdfFilename}.pdf s3://${s3Bucket}/${pdfFilename}.pdf"
                }
                }
            }
        }
        stage("CODE BUILD") {
            steps {
                sh "mvn clean install"
            }
        }
        stage("DOCKER BUILD") {
            steps {
            //   The password is piped from the echo command into the docker login command. 
            //  This approach prevents the password from being exposed in the console output or logs.
                withCredentials([usernamePassword(credentialsId: 'DEVVM_DOCKERHUB_CREDS', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    // Use the credentials in your pipeline
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }

                sh "docker build -t $imageName ."
            }    
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    sh "docker push $imageName"
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    sh "docker push $imageName"
                }
            }
        }
    
    }
}
