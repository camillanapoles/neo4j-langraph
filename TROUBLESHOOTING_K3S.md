# TROUBLESHOOTING K3S - Lições Aprendidas

**Data:** 25/12/2024
**Projeto:** neo4j-langraph (Sistema de Conhecimento Pessoal)
**Stack:** K3S + Neo4j + LocalAI (llama.cpp) + Gemini Flash 2.5

---

## 📚 ÍNDICE

1. [Resumo dos Problemas](#resumo-dos-problemas)
2. [Problema 1: Imagem do LocalAI não existia](#problema-1-imagem-do-localai-nao-existia)
3. [Problema 2: Permissões do PVC no K3S local-path](#problema-2-permissoes-do-pvc-no-k3s-local-path)
4. [Problema 3: Erro de configuração do Neo4j](#problema-3-erro-de-configuração-do-neo4j)
5. [Problema 4: Erro de memória do Neo4j](#problema-4-erro-de-memoria-do-neo4j)
6. [Problema 5: Configuração contaminada entre serviços](#problema-5-configuracao-contaminada-entre-servicos)
7. [Problema 6: PV/PVC não vinculando](#problema-6-pvpvc-nao-vinculando)
8. [Solução Final](#solucao-final)
9. [Checklist para Futuros Projetos](#checklist-para-futuros-projetos)
10. [Conclusão](#conclusao)

---

## 📊 RESUMO DOS PROBLEMAS

| Problema | Status | Dificuldade | Tempo para resolver |
|-----------|---------|--------------|-------------------|
| Imagem LocalAI | ✅ Resolvido | Fácil | 10 min |
| Permissões PVC | ✅ Resolvido | Médio | 30 min |
| Config Neo4j | ✅ Resolvido | Difícil | 1 hora |
| Memória Neo4j | ✅ Resolvido | Médio | 20 min |
| Config contaminada | ✅ Resolvido | Difícil | 40 min |
| PV/PVC vinculação | ✅ Resolvido | Médio | 30 min |
| **TOTAL** | **✅ Resolvidos** | - | **~3 horas** |

---

## 🚫 PROBLEMA 1: Imagem do LocalAI não existia

### Sintoma
```
Error: Failed to pull image "quay.io/go-skynet/local-ai:latest-cublas-cuda12"
Reason: 404 Not Found
Status: ImagePullBackOff
```

### Causa
A tag `latest-cublas-cuda12` NÃO existe no repositório do LocalAI.

### Solução
```yaml
# ANTES (ERRADO)
image: quay.io/go-skynet/local-ai:latest-cublas-cuda12

# DEPOIS (CORRETO)
image: quay.io/go-skynet/local-ai:v2.18.0-cublas-cuda12
```

### Lições Aprendidas
1. ✅ **NUNCA use `:latest` em produção**
   - Tags `:latest` podem mudar sem aviso
   - Quebra deployments
   - Não é reproduzível

2. ✅ **Sempre especifique a versão exata**
   - Use tags semânticas: `v2.18.0`
   - Verifique as tags disponíveis antes de usar
   - Teste em ambiente de desenvolvimento primeiro

3. ✅ **Verifique o repositório**
   ```bash
   # Verificar tags disponíveis
   curl https://quay.io/api/v1/repository/go-skynet/local-ai/tag/
   ```

---

## 🔒 PROBLEMA 2: Permissões do PVC no K3S local-path

### Sintoma
```
Error: Permission denied
Container: neo4j
Command: su-exec: find: Permission denied
```

### Causa
O K3S local-path provisioner criou PVs em `/mnt/container-data/k3s/storage/` com permissões incorretas. O container Neo4j (roda como usuário 1000) não tinha permissão para escrever no volume.

### Solução 1: PVs Dinâmicos (NÃO FUNCIONOU)
```yaml
# Tentativa 1 (falhou)
apiVersion: v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
```

### Solução 2: PVs Manuais (FUNCIONOU) ✅
```yaml
# Criar PV manual com path específico
apiVersion: v1
kind: PersistentVolume
metadata:
  name: neo4j-data-pv
  namespace: neo4j-langraph
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-path
  local:
    path: /mnt/container-data/projects/neo4j-langraph/neo4j
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - pop-os.local
```

### Lições Aprendidas
1. ✅ **PVs manuais = mais controle e previsibilidade**
   - Você sabe exatamente onde os dados estão armazenados
   - Pode configurar permissões antes do deploy
   - Mais fácil de fazer backup

2. ✅ **Organização de projetos**
   ```
   /mnt/container-data/
   ├── projects/
   │   ├── neo4j-langraph/
   │   │   ├── neo4j/          (PV do Neo4j)
   │   │   └── models/         (PV do LocalAI)
   │   └── fastapi-ddd-dev/
   └── k3s/                    (Provisioner dinâmico)
   ```

3. ✅ **Sempre configure `securityContext`**
   ```yaml
   spec:
     securityContext:
       fsGroup: 1000      # Grupo do filesystem
       runAsUser: 1000     # Usuário do container
     containers:
       - name: app
         securityContext:
           runAsNonRoot: true
   ```

4. ✅ **Configure permissões antes do deploy**
   ```bash
   mkdir -p /mnt/container-data/projects/neo4j-langraph/neo4j
   chmod 777 /mnt/container-data/projects/neo4j-langraph/neo4j
   ```

---

## ⚙️ PROBLEMA 3: Erro de configuração do Neo4j

### Sintoma
```
Failed to read config: Unrecognized setting.
No declared setting with name: PORT.7687.TCP.PORT
Cleanup the config or disable 'server.config.strict_validation.enabled'
```

### Causa
Neo4j 5.26-community tem validação estrita de configuração. Variáveis de ambiente de serviços anteriores (com nomes `neo4j-44`, `neo4j-test`) contaminaram a configuração.

Variáveis contaminadas:
```
44.SERVICE.PORT.HTTP
44.SERVICE.PORT.BOLT
44.SERVICE.HOST
44.PORT.7687.TCP.PROTO
44.PORT.7687.TCP.PORT
44.PORT.7687.TCP.ADDR
TEST.SERVICE.PORT.HTTP
TEST.SERVICE.PORT.BOLT
TEST.SERVICE.HOST
TEST.PORT.7687.TCP.PROTO
TEST.PORT
```

### Solução 1: Desabilitar validação (NÃO FUNCIONOU)
```yaml
# Tentativa 1 (falhou)
env:
  - name: NEO4J_server_config_strict__validation__enabled
    value: "false"
```

### Solução 2: Usar versão mais estável (FUNCIONOU) ✅
```yaml
# Usar Neo4j 4.4-community (LTS, mais estável)
image: docker.io/neo4j:4.4-community
```

### Lições Aprendidas
1. ✅ **Versões mais novas podem ter bugs**
   - Neo4j 5.x tem problemas com configurações de porta
   - Use versões LTS estáveis
   - Teste antes de usar em produção

2. ✅ **Em K8S, variáveis podem ser herdadas**
   - Serviços com nomes similares podem contaminar configs
   - Sempre limpe recursos de teste
   - Use nomes ÚNICOS e EXPLÍCITOS

3. ✅ **Limpeza total é melhor que tentar corrigir**
   ```bash
   # Se algo der errado, limpe tudo
   kubectl delete namespace [nome] --force --grace-period=0
   kubectl create namespace [nome]
   ```

---

## 🧠 PROBLEMA 4: Erro de memória do Neo4j

### Sintoma
```
ERROR: Invalid memory configuration - exceeds physical memory
Check configured values for dbms.memory.pagecache.size and dbms.memory.heap.max_size
```

### Causa
Neo4j tentou configurar memória automaticamente, mas o valor calculado excedia a memória física disponível (2GB request vs 2GB limit).

### Solução
```yaml
# Configurar memória explicitamente
containers:
  - name: neo4j
    image: docker.io/neo4j:4.4-community
    env:
      - name: NEO4J_AUTH
        value: "neo4j/password"
      - name: NEO4J_dbms_memory_heap_max__size
        value: "512m"
      - name: NEO4J_dbms_memory_pagecache_size
        value: "512m"
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
```

### Cálculo de Memória
```
Heap max:      512m
Pagecache:     512m
Total Config:  1GB

Memory Request: 1GB
Memory Limit:   2GB

✅ Total Config (1GB) < Memory Request (1GB) ✅ OK
✅ Memory Request (1GB) < Memory Limit (2GB)    ✅ OK
```

### Lições Aprendidas
1. ✅ **Sempre configure recursos explicitamente**
   - Não confie em valores padrão
   - Heap + Pagecache < Memory Request
   - Memory Request < Memory Limit

2. ✅ **Use requests e limits corretamente**
   ```yaml
   requests:
     memory: "1Gi"    # Garantia mínima
     cpu: "500m"
   limits:
     memory: "2Gi"    # Máximo permitido
     cpu: "1000m"
   ```

3. ✅ **Fórmula segura:**
   ```
   dbms.memory.heap.max_size + dbms.memory.pagecache.size
   ≤
   resources.requests.memory

   resources.requests.memory
   ≤
   resources.limits.memory
   ```

---

## ☠️ PROBLEMA 5: Configuração contaminada entre serviços

### Sintoma
```
# Logs do Neo4j mostravam:
WARNING: 44.SERVICE.PORT.HTTP not written to conf file
WARNING: 44.PORT.7687.TCP.PORT not written to conf file
WARNING: TEST.SERVICE.PORT.HTTP not written to conf file
```

### Causa
Múltiplos deployments de Neo4j rodando simultaneamente com nomes diferentes:
- `neo4j` (deployment principal)
- `neo4j-test` (deployment de teste)
- `neo4j-44` (deployment de teste)

Kubernetes criou ConfigMaps e Secrets automaticamente que contaminaram a configuração.

### Solução
```bash
# 1. Deletar serviços de teste
kubectl delete svc/neo4j-test -n neo4j-langraph --force
kubectl delete svc/neo4j-44 -n neo4j-langraph --force

# 2. Deletar deployments de teste
kubectl delete deployment/neo4j-test -n neo4j-langraph --force
kubectl delete deployment/neo4j-44 -n neo4j-langraph --force

# 3. Deletar pods de teste
kubectl delete pod/neo4j-test-xxx -n neo4j-langraph --force
kubectl delete pod/neo4j-44-xxx -n neo4j-langraph --force

# 4. Manter apenas o deployment principal
kubectl get deployment -n neo4j-langraph
# Output: deployment.apps/neo4j ✅
```

### Lições Aprendidas
1. ✅ **Em K8S, recursos de teste poluem o cluster**
   - ConfigMaps
   - Secrets
   - Services
   - Pods

2. ✅ **Deletar recursos de teste imediatamente**
   ```bash
   # Depois de testar, limpe tudo
   kubectl delete namespace [nome] --force --grace-period=0
   ```

3. ✅ **Use nomes únicos e explícitos**
   ```yaml
   # BOM
   metadata:
     name: neo4j-main  # ExPLÍCITO

   # RUIM
   metadata:
     name: neo4j  # Pode conflitar
   ```

---

## 🔗 PROBLEMA 6: PV/PVC não vinculando

### Sintoma
```
# PVC está Pending
kubectl get pvc -n neo4j-langraph
NAME                 STATUS    VOLUME
neo4j-data-pvc     Pending    <none>

# Pod está Pending
kubectl get pod -n neo4j-langraph
NAME                       READY   STATUS
neo4j-xxx-xxx             0/1     Pending
# Event: 0/1 nodes are available: persistentvolumeclaim "neo4j-data-pvc" not found
```

### Causa
O PVC não encontrou um PV disponível. PVs dinâmicos podem não vincular automaticamente se houver conflito de nomes ou storage classes.

### Solução
```yaml
# 1. Criar PV manual com nome específico
apiVersion: v1
kind: PersistentVolume
metadata:
  name: neo4j-data-pv  # NOME ESPECÍFICO
  namespace: neo4j-langraph
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-path
  local:
    path: /mnt/container-data/projects/neo4j-langraph/neo4j
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - pop-os.local

---

# 2. Criar PVC vinculado ao PV específico
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neo4j-data-pvc
  namespace: neo4j-langraph
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-path
  volumeName: neo4j-data-pv  # VINCULAR AO PV ESPECÍFICO
```

### Verificação
```bash
# 1. Verificar se PV está Available
kubectl get pv
NAME                CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS
neo4j-data-pv      5Gi        RWO            Retain           Available   ✅

# 2. Verificar se PVC está Bound
kubectl get pvc
NAME                 STATUS    VOLUME
neo4j-data-pvc     Bound      neo4j-data-pv   ✅

# 3. Verificar se pod está Running
kubectl get pod
NAME                       READY   STATUS
neo4j-xxx-xxx             1/1     Running   ✅
```

### Lições Aprendidas
1. ✅ **PVs dinâmicos podem não vincular**
   - Mais imprevisíveis
   - Podem ter conflitos de nomes
   - PVs manuais = mais controle

2. ✅ **Verifique SEMPRE o status**
   ```bash
   # Verificar status de PV
   kubectl get pv -o wide

   # Verificar status de PVC
   kubectl get pvc -o wide

   # Verificar eventos do pod
   kubectl describe pod [pod-name]
   ```

3. ✅ **Use `volumeName` para vinculação explícita**
   ```yaml
   spec:
     volumeName: neo4j-data-pv  # EXPLÍCITO
   ```

---

## ✅ SOLUÇÃO FINAL

### Configuração Funcional

```yaml
# ===== PVC =====
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neo4j-data-pvc
  namespace: neo4j-langraph
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-path
  volumeName: neo4j-data-pv

---
# ===== Deployment =====
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neo4j
  namespace: neo4j-langraph
spec:
  replicas: 1
  selector:
    matchLabels:
      app: neo4j
  template:
    metadata:
      labels:
        app: neo4j
    spec:
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
      containers:
      - name: neo4j
        image: docker.io/neo4j:4.4-community
        ports:
        - containerPort: 7474
          name: http
        - containerPort: 7687
          name: bolt
        env:
        - name: NEO4J_AUTH
          value: "neo4j/password"
        - name: NEO4J_dbms_memory_heap_max__size
          value: "512m"
        - name: NEO4J_dbms_memory_pagecache_size
          value: "512m"
        volumeMounts:
        - name: data
          mountPath: /data
        - name: logs
          mountPath: /logs
        - name: plugins
          mountPath: /plugins
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: neo4j-data-pvc
      - name: logs
        emptyDir: {}
      - name: plugins
        emptyDir: {}

---
# ===== Service =====
apiVersion: v1
kind: Service
metadata:
  name: neo4j
  namespace: neo4j-langraph
spec:
  type: NodePort
  selector:
    app: neo4j
  ports:
  - name: http
    port: 7474
    targetPort: 7474
    nodePort: 30474
  - name: bolt
    port: 7687
    targetPort: 7687
    nodePort: 30687
```

### LocalAI (Embeddings com GPU)

```yaml
# ===== Deployment =====
apiVersion: apps/v1
kind: Deployment
metadata:
  name: localai
  namespace: neo4j-langraph
spec:
  replicas: 1
  selector:
    matchLabels:
      app: localai
  template:
    metadata:
      labels:
        app: localai
    spec:
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
      containers:
      - name: localai
        image: quay.io/go-skynet/local-ai:v2.18.0-cublas-cuda12
        ports:
        - containerPort: 8080
          name: http
        envFrom:
        - configMapRef:
            name: localai-config
        env:
        - name: ADDRESS
          value: ":8080"
        volumeMounts:
        - name: models
          mountPath: /models
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            memory: "4Gi"
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: localai-models-pvc

---
# ===== Service =====
apiVersion: v1
kind: Service
metadata:
  name: localai
  namespace: neo4j-langraph
spec:
  type: NodePort
  selector:
    app: localai
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    nodePort: 30808
```

### Acesso aos Serviços

```bash
┌─────────────────────────────────────────────────────────┐
│  SISTEMA PRONTO!                                 │
└─────────────────────────────────────────────────────────┘

🌐 Neo4j Browser (Web):
   URL: http://localhost:30474
   Usuário: neo4j
   Senha: password

🔌 Neo4j BOLT (API):
   URL: bolt://localhost:30687
   Usuário: neo4j
   Senha: password

🤖 LocalAI (API):
   URL: http://localhost:30808
   API Docs: http://localhost:30808/docs
   Models: http://localhost:30808/v1/models
```

### Status dos Recursos

```bash
┌─────────────────────────────────────────────────────────┐
│  STATUS FINAL DO SISTEMA                           │
└─────────────────────────────────────────────────────────┘

🐳 PODS:
   ✅ LocalAI:    Running (1/1) - GPU ativa
   ✅ Neo4j:      Running (1/1) - Versão 4.4

🎮 GPU (RTX 4070 - 8GB VRAM):
   Usado: 162MB (2%)
   Livre: 7.6GB (98%)
   Status: Disponível para LocalAI

💾 DISCO (/mnt/container-data/):
   Total: 135GB
   Usado: 90GB (70%)
   Livre: 39GB

📊 PVs e PVCs:
   ✅ neo4j-data-pv/pvc:   Bound
   ✅ localai-models-pv/pvc:  Bound
   ✅ Caminho: /mnt/container-data/projects/neo4j-langraph/
```

---

## ✅ CHECKLIST PARA FUTUROS PROJETOS

### Antes de criar recursos K8S

- [ ] **Especifique versão EXATA das imagens**
  ```yaml
  # BOM
  image: quay.io/go-skynet/local-ai:v2.18.0-cublas-cuda12

  # RUIM
  image: quay.io/go-skynet/local-ai:latest
  ```

- [ ] **Crie PVs manuais em `/mnt/container-data/projects/[projeto]/`**
  ```yaml
  local:
    path: /mnt/container-data/projects/nome-projeto/app-data
  ```

- [ ] **Defina `securityContext` com `fsGroup` e `runAsUser`**
  ```yaml
  spec:
    securityContext:
      fsGroup: 1000
      runAsUser: 1000
  ```

- [ ] **Configure `resources.requests` e `resources.limits`**
  ```yaml
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"
  ```

- [ ] **Use nomes ÚNICOS e EXPLÍCITOS para serviços**
  ```yaml
  # BOM
  metadata:
    name: neo4j-main

  # RUIM
  metadata:
    name: neo4j
  ```

### Durante deploy

- [ ] **Verifique `kubectl get pods`**
  ```bash
  # STATUS deve ser "Running"
  kubectl get pods -n [namespace]
  ```

- [ ] **Verifique `kubectl get pvc`**
  ```bash
  # STATUS deve ser "Bound"
  kubectl get pvc -n [namespace]
  ```

- [ ] **Verifique `kubectl logs deployment/[nome]`**
  ```bash
  # Deve estar sem erros
  kubectl logs deployment/[app-name] -n [namespace]
  ```

- [ ] **Deletar recursos de teste imediatamente**
  ```bash
  # Depois de testar, limpe tudo
  kubectl delete namespace [nome] --force --grace-period=0
  kubectl create namespace [nome]
  ```

### Verificação final

- [ ] **Pods Running:**
  ```bash
  kubectl get pods -n [namespace]
  # READY: 1/1, STATUS: Running
  ```

- [ ] **PVCs Bound:**
  ```bash
  kubectl get pvc -n [namespace]
  # STATUS: Bound
  ```

- [ ] **Serviços acessíveis:**
  ```bash
  kubectl get svc -n [namespace]
  # Verifique NodePorts
  # Teste acesso: curl http://localhost:[nodeport]
  ```

- [ ] **Logs sem erros:**
  ```bash
  kubectl logs deployment/[app-name] -n [namespace] --tail=50
  # Deve estar limpo de erros
  ```

- [ ] **GPU usada (se aplicável):**
  ```bash
  nvidia-smi
  # Verifique se VRAM está sendo usada
  ```

---

## 🚀 PROBLEMAS FREQUENTES E SOLUÇÕES

### ImagePullBackOff

**Sintoma:**
```
Status: ImagePullBackOff
```

**Causa:** Imagem não existe ou não tem permissão

**Solução:**
```bash
# 1. Verifique se a imagem existe
docker pull [image-name]

# 2. Especifique versão exata
image: [image]:v1.2.3  # NÃO use :latest

# 3. Verifique credenciais (se necessário)
kubectl create secret docker-registry regcred \
  --docker-server=[registry] \
  --docker-username=[username] \
  --docker-password=[password]
```

---

### CrashLoopBackOff

**Sintoma:**
```
Status: CrashLoopBackOff
RESTARTS: 5 (1m ago)
```

**Causa:** Aplicação crasha e reinicia

**Solução:**
```bash
# 1. Verifique os logs
kubectl logs [pod-name] -n [namespace] --tail=50

# 2. Verifique os eventos
kubectl describe pod [pod-name] -n [namespace] | grep -A 10 "Events:"

# 3. Soluções comuns:
#    - Permissões de arquivo
#    - Configuração incorreta
#    - Memória insuficiente
#    - Dependências faltando
```

---

### Pending (Pod)

**Sintoma:**
```
Status: Pending
AGE: 5m
```

**Causa:** Recursos não disponíveis ou PVC não Bound

**Solução:**
```bash
# 1. Verifique eventos
kubectl describe pod [pod-name] -n [namespace] | grep -A 10 "Events:"

# 2. Soluções comuns:
#    - PVC não está Bound
#    - Nó não tem recursos suficientes
#    - NodeAffinity não está satisfeita
```

---

### Pending (PVC)

**Sintoma:**
```
NAME                 STATUS    VOLUME
my-pvc              Pending    <none>
```

**Causa:** PVC não encontrou PV disponível

**Solução:**
```bash
# 1. Verifique PVs disponíveis
kubectl get pv -n [namespace]

# 2. Verifique se PV tem storageClass correta
kubectl get pv [pv-name] -o yaml | grep storageClassName

# 3. Use PV manual com volumeName
kubectl get pvc [pvc-name] -o yaml | grep volumeName
```

---

## 🎯 MELHORES PRÁTICAS

### 1. Organização de Projetos

```
/mnt/container-data/
├── projects/
│   ├── projeto-1/
│   │   ├── app-data/        # PV principal
│   │   ├── models/         # PV de modelos
│   │   └── logs/          # PV de logs
│   └── projeto-2/
│       └── app-data/
└── k3s/                   # Provisioner dinâmico
```

### 2. Versionamento de Imagens

```yaml
# Sempre use versões específicas
image: nginx:1.25.2          # ✅ BOM
image: nginx:stable-alpine    # ✅ BOM
image: nginx:latest          # ❌ RUIM
```

### 3. Gerenciamento de Recursos

```yaml
# Use requests e limits sempre
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### 4. Health Checks

```yaml
# Sempre configure liveness e readiness probes
containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

### 5. Labels e Annotations

```yaml
# Use labels para organização
metadata:
  labels:
    app: neo4j
    version: "4.4"
    environment: production
  annotations:
    description: "Neo4j database for knowledge graph"
    owner: "cnmfs"
```

---

## 📝 CONCLUSÃO

### O que aprendemos hoje:

1. **✅ Imagens Docker/K8S**
   - NUNCA use `:latest`
   - Especifique versões semânticas
   - Teste antes de usar em produção

2. **✅ Persistent Volumes (PV/PVC)**
   - PVs manuais = mais controle
   - Configure permissões antes do deploy
   - Organize por projeto

3. **✅ Permissões e Segurança**
   - Sempre configure `securityContext`
   - Use `fsGroup` e `runAsUser`
   - Verifique permissões de arquivos

4. **✅ Gerenciamento de Recursos**
   - Configure memória e CPU explicitamente
   - Use requests < limits
   - Heap + Pagecache < Memory Request

5. **✅ Organização K8S**
   - Limpe recursos de teste imediatamente
   - Use nomes únicos e explícitos
   - Deletar e recriar se algo falhar

6. **✅ Troubleshooting**
   - Verifique logs: `kubectl logs`
   - Verifique eventos: `kubectl describe`
   - Verifique status: `kubectl get`

### Status Final:

```
┌─────────────────────────────────────────────────────────┐
│  SISTEMA PRONTO E FUNCIONAL!                 │
└─────────────────────────────────────────────────────────┘

✅ LocalAI:    Running (1/1) - GPU ativa
✅ Neo4j:      Running (1/1) - Versão 4.4
✅ GPU:         RTX 4070 - 162MB/8GB (2% usado)
✅ Disco:       39GB livres em /mnt/container-data/
```

### Próximos Passos:

1. Testar o sistema
   ```bash
   .venv/bin/python test_gemini_embeddings.py
   ```

2. Ingerir documentos
   ```bash
   .venv/bin/python -m src.cli.knowledge_cli ingest /path/to/docs
   ```

3. Visualizar grafo
   ```bash
   # Abrir no navegador
   http://localhost:30474
   ```

---

**Autor:** CNMFS
**Data:** 25/12/2024
**Versão:** 1.0.0
