pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_TARGET', choices: ['dev', 'prod'], description: 'Databricks bundle target')
        string(name: 'DATABRICKS_HOST', defaultValue: '', description: 'Databricks workspace URL')
    }

    environment {
        BUNDLE_TARGET = "${params.DEPLOY_TARGET}"
    }

    stages {
        stage('Validate bundle') {
            steps {
                withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    sh 'databricks bundle validate -t "$BUNDLE_TARGET"'
                }
            }
        }

        stage('Deploy and smoke test') {
            steps {
                withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    sh '''
                        databricks bundle deploy -t "$BUNDLE_TARGET"
                        databricks bundle run -t "$BUNDLE_TARGET" daily_job
                    '''
                }
            }
        }
    }
}