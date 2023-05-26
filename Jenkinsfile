 pipeline {
  agent any
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: env.CREDENTIALS_ID) {
                 sh 'pip install -r requirements.txt'
                 sh 'python3 scripts/parallel.py'
             }
         }
       }
     }
   }

