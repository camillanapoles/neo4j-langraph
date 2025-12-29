# 📂 ESTRUTURA DE DIRETÓRIOS - MELHORES PRÁTICAS

neo4j-langraph/
├── .github/
│   └── workflows/
│       ├── test.yml                    # Testes (GitHub Runner)
│       ├── deploy-dev.yml             # Deploy dev (Self-Hosted)
│       ├── deploy-staging.yml         # Deploy staging (GitHub Runner)
│       ├── deploy-prod.yml           # Deploy prod (GitHub Runner)
│       └── backup.yml                # Backup (CronJob)
│
├── k8s/
│   ├── base/                        # Manifestos base
│   │   ├── namespace.yaml
│   │   ├── neo4j/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml
│   │   └── localai/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   │
│   ├── overlays/                    # Kustomize overlays
│   │   ├── dev/
│   │   │   ├── kustomization.yaml
│   │   │   ├── dev-patch.yaml
│   │   │   └── secrets.yaml
│   │   ├── staging/
│   │   │   ├── kustomization.yaml
│   │   │   └── staging-patch.yaml
│   │   └── prod/
│   │       ├── kustomization.yaml
│   │       └── prod-patch.yaml
│   │
│   └── scripts/                     # Scripts K8S
│       ├── setup.sh
│       ├── cleanup.sh
│       └── backup.sh
│
├── scripts/                       # Scripts de automação
│   ├── setup_runner.sh            # Setup self-hosted runner
│   ├── setup_k3s.sh              # Setup K3S
│   ├── backup.sh                 # Backup automatizado
│   └── deploy.sh                 # Script de deploy
│
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   ├── integration/              # Testes de integração
│   └── e2e/                     # Testes end-to-end
│
├── docs/                         # Documentação
│   ├── architecture.md
│   ├── setup.md
│   └── deployment.md
│
├── .github/workflows/             # Workflows GitHub Actions
├── .gitignore                    # Ignorar arquivos sensíveis
├── .dockerignore                 # Ignorar no Docker
├── Dockerfile                    # Imagem Docker
├── docker-compose.yml            # Compose local
├── requirements.txt              # Dependências Python
├── kustomization.yaml            # Kustomize raiz
└── README.md                     # Documentação principal
