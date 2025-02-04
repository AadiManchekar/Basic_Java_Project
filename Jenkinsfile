pipeline {
    agent any

    tools{
        jdk 'openjdk11'
        maven 'Maven3'
    }

    environment {
        imageName = "basic-app:${env.BUILD_NUMBER}"
        repoPdf = "trivy_repository_scan${env.BUILD_NUMBER}"
        imagePdf = "trivy_image_scan${env.BUILD_NUMBER}"
        s3Bucket = "trivy-scans-pdf"
        awsProfile = "trivy-rwd"
        DOCKER = credentials('DEVVM_DOCKERHUB_CREDS')
    }

    stages {
        stage("CLEANUP BUILD FOLDER") {
            steps {
                sh "rm -rf ./*"
            }
        }
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
        stage("CODE BUILD") {
            steps {
                sh "mvn clean install"
            }
        }

        stage("DOCKER BUILD") {
            
            steps {
                withCredentials([usernamePassword(credentialsId: 'DEVVM_DOCKERHUB_CREDS', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    //  The password is piped from the echo command into the docker login command. 
                    //  This approach prevents the password from being exposed in the console output or logs.
                    sh ('echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin')

                    sh ('docker build -t $DOCKER_USERNAME/$imageName .')
                }
                
            }
        }
        stage("TRIVY SCAN") {
            steps {
                echo "RUNNING TRIVY SCAN ON REPOSITORY"
                sh ("trivy fs --scanners vuln,config -f json -o trivy_repository_scan${BUILD_NUMBER}.json .")
                
                echo "RUNNING TRIVY SCAN ON IMAGE"
                sh ('trivy image --severity HIGH,CRITICAL --scanners vuln -f json -o trivy_image_scan$BUILD_NUMBER.json $DOCKER_USR/$imageName')

            }
        }
        stage('GENERATE TRIVY PDF AND UPLOAD TO S3') {
            steps {
                script {
                    sh "python3 json_to_html.py"
        
                    withAWS(credentials: 'trivy-s3-aws-credentials', profileName: awsProfile) {
                        sh "aws s3 cp ${repoPdf}.html s3://${s3Bucket}/${repoPdf}.html"
                        sh "aws s3 cp ${imagePdf}.html s3://${s3Bucket}/${imagePdf}.html"
                    }
                }
            }
        }
        stage("IMAGE PUSH") {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    sh ('docker push $DOCKER_USR/$imageName')
                }
            }
        }   
    }
}
