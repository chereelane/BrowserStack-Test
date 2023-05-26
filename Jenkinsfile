 pipeline {
  agent any
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: env.CREDENTIALS_ID) {
                 sh 'python3 -m venv bsenv'
                 sh '''
                 source bsenv/bin/activate
                 pip install -r requirements.txt
                 python3 scripts/parallel.py
                 '''
            }
         }
       }
     }
   }

