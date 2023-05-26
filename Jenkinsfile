 pipeline {
  agent any
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: env.CREDENTIALS_ID) {
                 sh 'python3 -m venv bsenv'
                 sh 'cd bsenv/bin/activate'
                 sh 'pip install -r requirements.txt'
                 sh 'python3 scripts/parallel.py'
             }
         }
       }
     }
   }

