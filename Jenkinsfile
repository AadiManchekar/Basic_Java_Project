pipeline {
    agent any

    tools{
        jdk 'openjdk11'
        maven 'Maven3'
    }

    environment {
        imageName = "basic-app:${env.BUILD_NUMBER}"
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
                sh "ls"
            }
        }
        stage("CODE BUILD") {
            steps {
                sh "mvn clean install"
                sh "ls"
                sh "pwd"
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
        stage('Deploy to Production') {
            steps {
                script {
                    // Use the 'imageName' variable in other stages
                    sh "docker run $imageName"
                    // Other deployment steps
                }
            }
        }
    }
}
