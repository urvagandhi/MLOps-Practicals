# Practical 6: CI/CD for Machine Learning Project Using Jenkins

Implementation of Continuous Integration and Continuous Deployment (CI/CD) pipelines for an ML Web Application using **Jenkins**, based directly on the lecture guidelines in [`CICD.pdf`](file:///home/urva/Documents/Academics/Semester%20-%207/MLOps/Practicals/CICD.pdf).

---

## 📋 Overview & Architecture

The ML project consists of an **Iris Flower Classification** web application:
- **ML Model**: Pre-trained Scikit-Learn Naive Bayes classifier (`model.pkl`).
- **Web Application & Database**: Flask REST service embedding an internal SQLite database (`predictions.db`) for prediction history logging.
- **Unit & Integration Tests**: Automated `pytest` suite (`test_sample.py`) testing model deserialization, prediction correctness, and web endpoints.
- **Docker Compose Orchestration**: `docker-compose.yml` deploying each scenario on a **dedicated host port** with a unique container name so all scenarios can run simultaneously without conflicts:
  - **Scenario 1**: Port `8001:5000` (`http://localhost:8001`, Container: `cntwebapp_s1`)
  - **Scenario 2**: Port `8002:5000` (`http://localhost:8002`, Container: `cntwebapp_s2`)
  - **Scenario 3**: Port `8003:5000` (`http://localhost:8003`, Container: `cntwebapp_s3`)

### Directory Layout
```text
P6/
├── README.md
├── scenario_1_local_folder/         # Scenario 1: Local folder without Git (Pipeline Script + customWorkspace)
│   ├── app.py
│   ├── model.pkl
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Jenkinsfile
│   ├── test_sample.py
│   ├── .dockerignore
│   ├── static/
│   │   └── main.css
│   └── templates/
│       ├── index.html
│       ├── prediction.html
│       └── records.html
├── scenario_2_local_git_repo/       # Scenario 2: Local Git repo (Pipeline Script from SCM + file:/// URL)
│   ├── app.py
│   ├── model.pkl
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Jenkinsfile
│   ├── test_sample.py
│   ├── init_git.sh
│   ├── .dockerignore
│   ├── static/
│   │   └── main.css
│   └── templates/
│       ├── index.html
│       ├── prediction.html
│       └── records.html
└── scenario_3_github_repo/          # Scenario 3: Remote GitHub repo (Pipeline Script from SCM + https:// URL)
    ├── app.py
    ├── model.pkl
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── Jenkinsfile
    ├── test_sample.py
    ├── .dockerignore
    ├── static/
    │   └── main.css
    └── templates/
        ├── index.html
        ├── prediction.html
        └── records.html
```

---

## ⚙️ Initial Jenkins Pre-requisites & System Configuration

### 1. Configure Built-In Node Label as `local` (Slide 32, 42)
For pipelines using `agent { node { label 'local' } }`:
1. Log in to Jenkins (`http://localhost:8080`).
2. Go to **Manage Jenkins** → **Nodes** → Click **Built-In Node**.
3. Click **Configure** (in the left sidebar).
4. In **Labels**, enter: `local` (or `local built-in`).
5. Set **Usage** to: `Use this node as much as possible`.
6. Click **Save**.

### 2. Docker Permissions for Jenkins Service (Linux)
Since Jenkins executes build commands as the `jenkins` background system user:
```bash
sudo usermod -aG docker jenkins && sudo chmod 666 /var/run/docker.sock && sudo systemctl restart jenkins
```

### 3. Workspace Read/Write Permissions (Linux)
Ensure the `jenkins` background service user has write permission to create execution scripts and temporary folders (`@tmp`):
```bash
chmod -R a+rwx "/home/urva/Documents/Academics/Semester - 7/MLOps/Practicals/P6"
```

### 4. Enable Local Git Checkouts (`file:///...`)
Modern Jenkins Git Plugin blocks local directory checkouts for security unless `ALLOW_LOCAL_CHECKOUT=true` is enabled:
```bash
sudo mkdir -p /etc/systemd/system/jenkins.service.d
sudo tee /etc/systemd/system/jenkins.service.d/override.conf << 'EOF'
[Service]
Environment="JAVA_OPTS=-Djava.awt.headless=true -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true"
EOF
sudo systemctl daemon-reload && sudo systemctl restart jenkins
```

---

## 🚀 Scenario 1: Local Directory (Non-Git) with Custom Workspace

### Concept (Slide 40–42)
- Assumes the project is located locally on disk and is **not** a Git repository.
- Jenkins does not perform SCM checkout. Instead, it directly binds the project directory using `customWorkspace`.
- **Pipeline Definition in Jenkins UI**: `Pipeline script` (paste script directly into Job configuration).
- **Deployed Port**: `http://localhost:8001` (Container: `cntwebapp_s1`).

### Jenkinsfile (`scenario_1_local_folder/Jenkinsfile`)
```groovy
pipeline {
    agent { // agent any does not allow specifying custom workspace
        node {
            label 'local'
            customWorkspace '/home/urva/Documents/Academics/Semester - 7/MLOps/Practicals/P6/scenario_1_local_folder' /* as our project is not at standard path */
        }
    }
    stages {
        /*
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/iris_project.git'
            }
        }
        */
        stage('Show Workspace') {
            steps {
                // bat 'cd' // Windows
                sh 'pwd'   // Linux
            }
        }
        stage('Build Images') {
            steps {
                // bat 'docker compose build' // Windows
                sh 'docker compose build'     // Linux
            }
        }
        stage('Run Tests') {
            steps {
                // bat 'docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"' // Windows
                sh 'docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"'     // Linux
            }
        }
        stage('Deploy Containers') {
            steps {
                // bat 'docker compose up -d' // Windows
                sh 'docker compose up -d'     // Linux
            }
        }
    }
}
```

### Steps in Jenkins UI
1. Click **+ New Item** → Enter name: `P6-Scenario1-LocalFolder` → Select **Pipeline** → Click **OK**.
2. Leave General options and Triggers unchecked (as per Slide 49).
3. In the **Pipeline** section at the bottom:
   - **Definition**: Select `Pipeline script`.
   - **Script**: Paste the entire code from `scenario_1_local_folder/Jenkinsfile`.
4. Click **Save** → Click **Build Now**.
5. Once complete, open **`http://localhost:8001`** to view the deployed web app.

---

## 🚀 Scenario 2: Local Git Repository via SCM (`file:///...`)

### Concept (Slide 43–44)
- Assumes the project is available locally and is initialized as a local Git repository.
- Jenkins pulls the code from the local directory using the `file:///` Git URL protocol.
- `customWorkspace` is replaced with `agent { node { label 'local' } }`.
- **URL Rules** (Slide 44):
  - Starts with `file:///` (3 forward slashes).
  - Spaces in folder names must be URL-encoded as `%20`.
  - Always use forward slashes `/`.
- **Pipeline Definition in Jenkins UI**: `Pipeline script from SCM`.
- **Deployed Port**: `http://localhost:8002` (Container: `cntwebapp_s2`).

### Initializing Local Git Repository
Initialize the local git repository once using the provided helper:
```bash
cd "/home/urva/Documents/Academics/Semester - 7/MLOps/Practicals/P6/scenario_2_local_git_repo"
bash init_git.sh
```

### Jenkinsfile (`scenario_2_local_git_repo/Jenkinsfile`)
```groovy
pipeline {
    agent {
        node {
            label 'local'
        }
    }
    stages {
        stage('Checkout Code') {
            steps {
                // file:/// starts the path (3 slashes). Spaces URL-encoded as %20
                git branch: 'main', url: 'file:///home/urva/Documents/Academics/Semester%20-%207/MLOps/Practicals/P6/scenario_2_local_git_repo'
            }
        }
        stage('Show Workspace') {
            steps {
                // bat 'cd' // Windows
                sh 'pwd'   // Linux
            }
        }
        stage('Build Images') {
            steps {
                // bat 'docker compose build' // Windows
                sh 'docker compose build'     // Linux
            }
        }
        stage('Run Tests') {
            steps {
                // bat 'docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"' // Windows
                sh 'docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"'     // Linux
            }
        }
        stage('Deploy Containers') {
            steps {
                // bat 'docker compose up -d' // Windows
                sh 'docker compose up -d'     // Linux
            }
        }
    }
}
```

### Steps in Jenkins UI
1. Click **+ New Item** → Enter name: `P6-Scenario2-LocalGit` → Select **Pipeline** → Click **OK**.
2. In the **Pipeline** section:
   - **Definition**: Select `Pipeline script from SCM`.
   - **SCM**: Select `Git`.
   - **Repository URL**: 
     ```text
     file:///home/urva/Documents/Academics/Semester%20-%207/MLOps/Practicals/P6/scenario_2_local_git_repo
     ```
   - **Branch Specifier**: `*/main` (or `main`).
   - **Script Path**: `Jenkinsfile`.
3. Click **Save** → Click **Build Now**.
4. Once complete, open **`http://localhost:8002`** to view the deployed web app.

---

## 🚀 Scenario 3: Remote GitHub Repository via SCM (`https://...`)

### Concept (Slide 45)
- Assumes the project is hosted remotely on GitHub.
- Jenkins clones code over HTTPS from GitHub.
- `agent any` is used because the agent pulls everything freshly into its standard workspace.
- **Pipeline Definition in Jenkins UI**: `Pipeline script from SCM`.
- **Deployed Port**: `http://localhost:8003` (Container: `cntwebapp_s3`).

### Jenkinsfile (`scenario_3_github_repo/Jenkinsfile`)
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/urvagandhi/MLOps-Practicals.git'
                // Or dedicated repo: git branch: 'main', url: 'https://github.com/your-username/iris_project.git'
            }
        }
        stage('Show Workspace') {
            steps {
                // bat 'cd' // Windows
                sh 'pwd'   // Linux
            }
        }
        stage('Build Images') {
            steps {
                // bat 'docker compose build' // Windows
                sh '''
                    if [ -d "P6/scenario_3_github_repo" ]; then
                        cd "P6/scenario_3_github_repo"
                    fi
                    docker compose build
                '''
            }
        }
        stage('Run Tests') {
            steps {
                // bat 'docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"' // Windows
                sh '''
                    if [ -d "P6/scenario_3_github_repo" ]; then
                        cd "P6/scenario_3_github_repo"
                    fi
                    docker run --rm demo1_jenkins_as_container_webapp pytest || echo "No tests found"
                '''
            }
        }
        stage('Deploy Containers') {
            steps {
                // bat 'docker compose up -d' // Windows
                sh '''
                    if [ -d "P6/scenario_3_github_repo" ]; then
                        cd "P6/scenario_3_github_repo"
                    fi
                    docker compose up -d
                '''
            }
        }
    }
}
```

### Steps in Jenkins UI
1. Push your repository to GitHub:
   ```bash
   git add P6/
   git commit -m "feat(P6): add Jenkins CI/CD pipelines"
   git push origin main
   ```
2. In Jenkins, click **+ New Item** → Enter name: `P6-Scenario3-GitHubRepo` → Select **Pipeline** → Click **OK**.
3. In the **Pipeline** section:
   - **Definition**: Select `Pipeline script from SCM`.
   - **SCM**: Select `Git`.
   - **Repository URL**: `https://github.com/urvagandhi/MLOps-Practicals.git` (or your dedicated repo URL).
   - **Branch Specifier**: `*/main`.
   - **Script Path**: `P6/scenario_3_github_repo/Jenkinsfile`.
4. Click **Save** → Click **Build Now**.
5. Once complete, open **`http://localhost:8003`** to view the deployed web app.

---

## 🧪 Automated Testing Verification

The automated test suite in `test_sample.py` is invoked during the `Run Tests` stage:
1. `test_model_loaded`: Validates model deserialization and predicts sample Iris Setosa features `[5.1, 3.5, 1.4, 0.2]`.
2. `test_index_page`: Confirms HTTP 200 on `/`.
3. `test_prediction_endpoint`: Tests `POST /predict` form submission and confirms prediction output `Setosa`.
4. `test_records_page`: Tests `GET /records` database retrieval.

Manual verification command:
```bash
docker run --rm demo1_jenkins_as_container_webapp pytest
```
Output:
```text
============================= test session starts ==============================
rootdir: /app
collected 4 items

test_sample.py ....                                                      [100%]
========================= 4 passed, 1 warning in 1.96s =========================
```

---

## 🌐 Summary of Deployed Services

All 3 scenarios are configured with unique container names and host ports so they can be run and demonstrated simultaneously without port collisions or container name clashes:

| Scenario | Mode | Port | Container Name | Verification URL |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | Local Folder (`customWorkspace`) | `8001` | `cntwebapp_s1` | [http://localhost:8001](http://localhost:8001) |
| **Scenario 2** | Local Git (`file:///` SCM) | `8002` | `cntwebapp_s2` | [http://localhost:8002](http://localhost:8002) |
| **Scenario 3** | Remote GitHub (`https://` SCM) | `8003` | `cntwebapp_s3` | [http://localhost:8003](http://localhost:8003) |

### Verifying Running Containers
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Tear Down All Running Containers
To cleanly stop and remove all deployed containers:
```bash
docker rm -f cntwebapp_s1 cntwebapp_s2 cntwebapp_s3 2>/dev/null || true
```

---

## 🛠️ Practical Troubleshooting & Lab Learnings

During real-world setup and execution in Jenkins on Ubuntu/Linux, several common pipeline and environment issues were resolved:

### 1. `docker-compose: not found` (Exit code 127)
- **Cause**: Modern Docker installations on Ubuntu use Docker CLI Compose V2 (`docker compose` space-separated) rather than the legacy standalone binary `docker-compose`.
- **Fix**: Replaced all `docker-compose build` and `docker-compose up -d` commands with `docker compose build` and `docker compose up -d` in all `Jenkinsfile` scripts. Additionally removed obsolete `version: "3.8"` attributes from compose files to eliminate parser warnings.

### 2. `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`
- **Cause**: Jenkins executes shell steps as the system user `jenkins`, which does not belong to the `docker` user group by default.
- **Fix**: Added the `jenkins` user to the `docker` group and set socket permissions:
  ```bash
  sudo usermod -aG docker jenkins
  sudo chmod 666 /var/run/docker.sock
  sudo systemctl restart jenkins
  ```

### 3. `AccessDeniedException: /home/urva/.../P6/...@tmp`
- **Cause**: Jenkins automatically attempts to create durable task script files inside a `@tmp` directory alongside the custom workspace directory. If the parent path has restricted permissions for other users, the build crashes at stage start.
- **Fix**: Granted read-write-execute permissions across the practical directory:
  ```bash
  chmod -R a+rwx "/home/urva/Documents/Academics/Semester - 7/MLOps/Practicals/P6"
  ```

### 4. `Checkout of Git remote 'file:///...' aborted because it references a local directory, which may be insecure`
- **Cause**: Starting from recent versions of the Jenkins Git Plugin, checking out local directories via `file:///` is blocked by default for security reasons.
- **Fix**: Added system property `-Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true` to Jenkins systemd service options:
  ```bash
  sudo mkdir -p /etc/systemd/system/jenkins.service.d
  sudo tee /etc/systemd/system/jenkins.service.d/override.conf << 'EOF'
  [Service]
  Environment="JAVA_OPTS=-Djava.awt.headless=true -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true"
  EOF
  sudo systemctl daemon-reload && sudo systemctl restart jenkins
  ```

### 5. `Conflict. The container name "/cntwebapp" is already in use` & Port Collisions
- **Cause**: Running multiple pipeline jobs using identical container names (`cntwebapp`) and identical host ports (`8000:5000`) caused Docker daemon name collisions and `bind: address already in use` failures.
- **Fix**: Assigned isolated container names and independent host ports across the 3 scenarios:
  - Scenario 1: `cntwebapp_s1` → Port `8001:5000`
  - Scenario 2: `cntwebapp_s2` → Port `8002:5000`
  - Scenario 3: `cntwebapp_s3` → Port `8003:5000`

