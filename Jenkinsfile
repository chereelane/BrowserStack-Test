 pipeline {
  agent
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: 'c9198883-a803-4091-8021-0e7212fbeffc') {
                 sh 'python3 scripts/parallel.py'
             }
         }
       }
     }
   }

