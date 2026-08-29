pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_TARGET', choices: ['dev', 'prod'], description: 'Databricks bundle target')
        string(name: 'DATABRICKS_HOST', defaultValue: '', description: 'Databricks workspace URL, for example https://<workspace-host>')
    }

    environment {
        BUNDLE_TARGET = "${params.DEPLOY_TARGET}"
        DATABRICKS_HOST = "${params.DATABRICKS_HOST}"
    }

    stages {
        stage('Check prerequisites') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            set -e
                            if ! command -v databricks >/dev/null 2>&1; then
                                echo "Databricks CLI is not installed or not on PATH. Install it on the Jenkins agent first."
                                exit 1
                            fi

                            if [ -z "$DATABRICKS_HOST" ]; then
                                echo "DATABRICKS_HOST is required. Set the Jenkins string parameter or env var for the Databricks workspace URL."
                                exit 1
                            fi

                            databricks --version
                        '''
                    } else {
                        bat '''
                            @echo off
                            where databricks >nul 2>nul
                            if errorlevel 1 (
                                echo Databricks CLI is not installed or not on PATH. Install it on the Jenkins agent first.
                                exit /b 1
                            )

                            if "%DATABRICKS_HOST%"=="" (
                                echo DATABRICKS_HOST is required. Set the Jenkins string parameter or env var for the Databricks workspace URL.
                                exit /b 1
                            )

                            databricks --version
                        '''
                    }
                }
            }
        }

        stage('Validate bundle') {
            steps {
                withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    script {
                        if (isUnix()) {
                            sh '''
                                set -e
                                export DATABRICKS_HOST="$DATABRICKS_HOST"
                                databricks bundle validate -t "$BUNDLE_TARGET"
                            '''
                        } else {
                            bat '''
                                @echo off
                                set DATABRICKS_HOST=%DATABRICKS_HOST%
                                set DATABRICKS_TOKEN=%DATABRICKS_TOKEN%
                                databricks bundle validate -t %BUNDLE_TARGET%
                            '''
                        }
                    }
                }
            }
        }

        stage('Deploy and smoke test') {
            steps {
                withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    script {
                        if (isUnix()) {
                            sh '''
                                set -e
                                export DATABRICKS_HOST="$DATABRICKS_HOST"
                                databricks bundle deploy -t "$BUNDLE_TARGET"
                                databricks bundle run -t "$BUNDLE_TARGET" daily_job
                            '''
                        } else {
                            bat '''
                                @echo off
                                set DATABRICKS_HOST=%DATABRICKS_HOST%
                                set DATABRICKS_TOKEN=%DATABRICKS_TOKEN%
                                databricks bundle deploy -t %BUNDLE_TARGET%
                                databricks bundle run -t %BUNDLE_TARGET% daily_job
                            '''
                        }
                    }
                }
            }
        }
    }
}