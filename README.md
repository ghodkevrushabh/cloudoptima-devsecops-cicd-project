# ☁️ CloudOptima: A DevSecOps-Integrated Internal Developer Platform for Automated, Secure & Policy-Governed AWS Provisioning 🕵

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Cloud%20Security-232F3E?logo=amazonaws&logoColor=white" alt="AWS"/>
  <img src="https://img.shields.io/badge/DevSecOps-Jenkins-D24939?logo=jenkins&logoColor=white" alt="Jenkins"/>
  <img src="https://img.shields.io/badge/Infrastructure-Terraform-844FBA?logo=terraform&logoColor=white" alt="Terraform"/>
  <img src="https://img.shields.io/badge/Security-Wazuh-4C9AFF?logo=wazuh&logoColor=white" alt="Wazuh"/>
  <img src="https://img.shields.io/badge/IDS-Suricata-EF3B2D?logo=suricata&logoColor=white" alt="Suricata"/>
  <img src="https://img.shields.io/badge/Web%20Security-AWS%20WAF-FF9900?logo=amazonaws&logoColor=white" alt="AWS WAF"/>
  <img src="https://img.shields.io/badge/Monitoring-Grafana-F46800?logo=grafana&logoColor=white" alt="Grafana"/>
</p>

<p align="center">
  <strong>End-to-end Internal Developer Platform + DevSecOps + Cloud Security + SOC Demonstration</strong>
</p>

<p align="center">
  <em>CloudOptima is a self-service cloud platform that connects developer workflows, infrastructure automation, CI/CD security controls, runtime security, cloud auditing, and security operations into one demonstrable lifecycle.</em>
</p>

---

## 📌 Project Status

> **Documentation is being built in phases.** This repository README is intentionally designed as a recruiter-facing technical document: architecture first, implementation second, validation third, and evidence last.

| Area | Status |
|---|---|
| Internal Developer Platform (Flask) | ✅ Implemented |
| GitHub integration | ✅ Implemented / demonstrated |
| Jenkins CI/CD | ✅ Implemented / demonstrated |
| Terraform automation | ✅ Implemented / demonstrated |
| Ansible automation | ✅ Implemented / demonstrated |
| DevSecOps security gates | ✅ Demonstrated |
| AWS WAF protection | ✅ Implemented |
| Suricata IDS | ✅ Implemented |
| Wazuh SIEM / HIDS | ✅ Implemented |
| AWS CloudTrail | ✅ Implemented |
| Grafana / Prometheus / Loki observability | ✅ Implemented |
| Five controlled web-attack demonstrations | ✅ Validated |


---

# 1. 🎯 Executive Summary

CloudOptima is an **end-to-end cloud-native DevSecOps and security operations project** designed to demonstrate how an organization can move from a developer request to infrastructure deployment, security validation, runtime monitoring, and incident visibility through a connected workflow.

The platform combines:

- **Platform Engineering / IDP** — developer self-service through Flask.
- **Source Control** — GitHub as the source of truth.
- **CI/CD** — Jenkins-driven automation.
- **Infrastructure as Code** — Terraform.
- **Configuration Management** — Ansible.
- **DevSecOps controls** — SonarQube, GitLeaks, Checkov, Infracost, OPA, Trivy and related pipeline stages.
- **Container security / registry workflow** — Docker + Amazon ECR.
- **Runtime security** — Wazuh + Suricata + AWS WAF.
- **Cloud auditability** — AWS CloudTrail → S3 → Wazuh.
- **Observability** — Prometheus, Node Exporter, Loki, Promtail and Grafana.
- **Security visualization** — Wazuh Security Operations dashboard and AWS WAF dashboard.

The project intentionally demonstrates **defense in depth** rather than relying on a single security product.

---

# 2. 🧭 Problem Statement

Modern cloud teams need more than a CI/CD pipeline. A production-oriented workflow must answer all of the following:

1. How does a developer request infrastructure or an application environment?
2. How is the request converted into reproducible infrastructure?
3. How is source code and infrastructure validated before deployment?
4. How are secrets, insecure Terraform patterns, vulnerabilities and policy violations caught early?
5. How is the workload protected once deployed?
6. How are application-layer attacks detected and blocked?
7. How are host, network and cloud-control-plane events correlated?
8. How does the team observe infrastructure health and troubleshoot incidents?
9. How can the entire workflow be demonstrated to an engineering or security reviewer?

CloudOptima was built to answer these questions in one integrated project.

---

# 3. 🏗️ High-Level Architecture

```text
                                    ┌─────────────────────────────┐
                                    │        Developer            │
                                    │  Self-Service / Git Commit  │
                                    └──────────────┬──────────────┘
                                                   │
                                                   ▼
                                    ┌─────────────────────────────┐
                                    │      CloudOptima IDP        │
                                    │ Flask + PostgreSQL          │
                                    │ Terraform/Ansible Generator │
                                    │ GitHub Integration           │
                                    └──────────────┬──────────────┘
                                                   │
                                                   ▼
                                             ┌───────────┐
                                             │  GitHub   │
                                             └─────┬─────┘
                                                   │
                                                   ▼
                                    ┌─────────────────────────────┐
                                    │          Jenkins             │
                                    │       DevSecOps VM          │
                                    ├─────────────────────────────┤
                                    │ Terraform                   │
                                    │ Checkov                      │
                                    │ Infracost                    │
                                    │ SonarQube                    │
                                    │ GitLeaks                     │
                                    │ Docker                       │
                                    │ Trivy                        │
                                    │ Amazon ECR                   │
                                    │ OPA                          │
                                    │ Ansible                      │
                                    └──────────────┬──────────────┘
                                                   │
                                                   ▼
                                    ┌─────────────────────────────┐
                                    │        AWS Runtime           │
                                    │      CloudOptima ALB         │
                                    └──────────────┬──────────────┘
                                                   │
                                      ┌────────────┴────────────┐
                                      │                         │
                                      ▼                         │
                               ┌─────────────┐                  │
                               │  AWS WAF    │                  │
                               │ Prevention  │                  │
                               └──────┬──────┘                  │
                                      │                         │
                                      ▼                         │
                               ┌─────────────┐                  │
                               │ Juice Shop  │                  │
                               │ 10.0.104.170│                  │
                               └──────┬──────┘                  │
                                      │                         │
                           Traffic Mirror                       │
                                      │                         │
                                      ▼                         │
                               ┌─────────────┐                  │
                               │  Suricata   │                  │
                               │    IDS      │                  │
                               └──────┬──────┘                  │
                                      │                         │
                                      ▼                         │
                               ┌─────────────┐                  │
                               │    Wazuh    │◄─────────────────┘
                               │  SIEM/HIDS  │
                               └──────┬──────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │ Wazuh Security         │
                          │ Operations Dashboard   │
                          └────────────────────────┘

       AWS CloudTrail ──► S3 ──► Wazuh AWS-S3 module ──► Wazuh

       Prometheus / Node Exporter / Loki / Promtail ──► Grafana
```

> **Important design decision:** Suricata is deployed as a **passive IDS sensor using AWS Traffic Mirroring**, not as an inline IPS. AWS WAF is the web-prevention layer at the ALB; Suricata provides network detection/visibility for traffic that reaches the monitored backend ENI.

---

# 4. 🔐 Security Architecture / Defense-in-Depth Model

CloudOptima uses multiple controls at different layers instead of trying to make one product solve everything.

| Layer | Technology | Responsibility |
|---|---|---|
| Edge / Web | AWS WAF | Prevent malicious HTTP requests |
| Load Balancing | AWS ALB | Controlled public entry point |
| Application | Juice Shop | Controlled vulnerable training application |
| Network Detection | Suricata | Inspect mirrored backend traffic |
| Host / SIEM | Wazuh | Host monitoring, rule correlation and security analytics |
| Cloud Audit | AWS CloudTrail | AWS API/control-plane auditing |
| Audit Storage | S3 | CloudTrail log storage |
| Infrastructure | Terraform / Ansible | Reproducible provisioning/configuration |
| CI/CD Security | Checkov / SonarQube / GitLeaks / Trivy / OPA | Shift-left validation |
| Observability | Prometheus / Loki / Grafana | Metrics, logs and operational visibility |

---

# 5. 🧩 Major Components

## 5.1 Platform Engineering / Internal Developer Platform

The CloudOptima IDP provides a developer-facing entry point for infrastructure/application requests.

### Core components

- Flask
- PostgreSQL
- Terraform generator
- Ansible generator
- GitHub integration

### Current implementation note

The earliest working Flask portal was created directly on an EC2 instance as a rapid prototype. This was later recognized as a non-ideal deployment pattern. The project documentation therefore distinguishes between the **working prototype path** and the **target production architecture** rather than hiding this engineering trade-off.

---

## 5.2 Source Control

GitHub is treated as the source of truth for:

- application code
- Jenkinsfile
- Terraform
- Ansible
- security/policy configuration
- documentation

> **Repository hygiene rule:** changes to Jenkinsfile/Terraform/Ansible/repository files should be made from the proper development/source location (GitHub or a normal Git clone), committed and pushed there. The Jenkins workspace is treated as an ephemeral checkout and is not used as the place for development commits.

---

## 5.3 CI/CD / DevSecOps

The intended CloudOptima pipeline is:

```text
GitHub
  │
  ▼
Jenkins Checkout
  │
  ├── SonarQube
  ├── GitLeaks
  ├── Terraform validation / plan
  ├── Checkov
  ├── Infracost
  ├── OPA policy validation
  ├── Docker build
  ├── Trivy image scan
  ├── Amazon ECR
  └── Ansible
          │
          ▼
      AWS Runtime
```

> Detailed stage-by-stage commands, Jenkinsfile excerpts, credentials model, workspace handling, tool installation and screenshots will be documented in **Phase 3 — DevSecOps Pipeline**.

---

# 6. ☁️ AWS Runtime Architecture

## Primary security-relevant resources

| Resource | Role |
|---|---|
| `cloudoptima-alb` | Public application entry point |
| Juice Shop EC2 | Vulnerable demo application |
| Suricata EC2 | Traffic Mirror destination / IDS |
| Wazuh EC2 | SIEM/HIDS manager |
| DevSecOps/Jenkins EC2 | CI/CD + AWS administrative automation |
| CloudTrail S3 bucket | Audit log storage |

### Important addresses used in the lab

```text
Juice Shop          10.0.104.170
Suricata sensor     10.0.47.60
Wazuh Manager       10.0.39.73
DevSecOps/Jenkins   10.0.13.50
```

The public application is reached through the ALB DNS name:

```text
cloudoptima-alb-708681634.eu-north-1.elb.amazonaws.com
```

> Exact production addressing, subnet IDs, security-group IDs and account-specific values should be added to the private/internal appendix if the repository is public.

---

# 7. 🛡️ AWS WAF — Web Application Prevention

CloudOptima's ALB is protected by a Regional AWS WAF Web ACL named:

```text
cloudoptima-waf
```

### Final rule set

```text
AWSCommonRules
AWSManagedRulesSQLiRuleSet
RateLimit          = 1000 requests / 5 minutes / IP
AWSManagedRulesLinuxRuleSet
AWSManagedRulesKnownBadInputsRuleSet
```

### Why WAF is used

WAF sits at the web-entry layer and can block malicious HTTP requests **before the request reaches Juice Shop**.

This is complementary to Suricata:

```text
AWS WAF   → Prevention / blocking
Suricata  → Network detection / visibility
Wazuh     → Correlation / investigation / host telemetry
```

---

# 8. 🧪 Five Validated Web-Attack Demonstrations

The project deliberately demonstrated five controlled attacks against the Juice Shop path.

| # | Attack | Primary WAF protection | Observed outcome |
|---|---|---|---|
| 1 | SQL Injection | `AWSManagedRulesSQLiRuleSet` | `403 BLOCK` |
| 2 | XSS | `AWSManagedRulesCommonRuleSet` | `403 BLOCK` |
| 3 | LFI / Path Traversal | `AWSManagedRulesLinuxRuleSet` | `403 BLOCK`; `LFI_URIPATH` |
| 4 | Log4Shell-style known-bad input | `AWSManagedRulesKnownBadInputsRuleSet` | `403 BLOCK`; `Log4J#RC_QUERYSTRING` |
| 5 | SSRF / EC2 metadata access attempt | `AWSManagedRulesCommonRuleSet` | `403 BLOCK`; `EC2MetaDataSSRF_QUERYARGUMENTS` |

### Attack flow

```text
Kali
  │
  ▼
AWS WAF
  │
  ├── malicious request → BLOCK
  │
  └── legitimate request → ALB → Juice Shop
```

### 📸 Screenshot placeholders

> **[SCREENSHOT — WAF DASHBOARD: five attack categories]**  
> Paste screenshot here: `docs/screenshots/waf/five-attack-dashboard.png`

> **[SCREENSHOT — SQLi sampled request showing BLOCK]**  
> Paste screenshot here: `docs/screenshots/waf/sqli-block.png`

> **[SCREENSHOT — XSS 403 response]**  
> Paste screenshot here: `docs/screenshots/waf/xss-403.png`

> **[SCREENSHOT — LFI sampled request showing LFI_URIPATH]**  
> Paste screenshot here: `docs/screenshots/waf/lfi-block.png`

> **[SCREENSHOT — Log4Shell sampled request showing BLOCK]**  
> Paste screenshot here: `docs/screenshots/waf/log4j-block.png`

> **[SCREENSHOT — SSRF sampled request showing BLOCK]**  
> Paste screenshot here: `docs/screenshots/waf/ssrf-block.png`

---

# 9. 🛰️ Suricata IDS Architecture

Suricata is deliberately deployed as a **passive IDS** using AWS Traffic Mirroring.

```text
Juice Shop ENI
      │
      ├──────────► normal application traffic
      │
      └── mirrored copy ──► Suricata
                                  │
                                  ▼
                               Wazuh
```

### Final custom Suricata rule set

The final project kept only the meaningful custom SQL injection signature:

```suricata
alert http any any -> $HOME_NET any (msg:"CloudOptima SQL Injection Attempt"; http.uri.raw; content:"%27+OR+1%3d1--"; nocase; sid:1000003; rev:1;)
```

A generic HTTP rule that generated excessive low-value alert volume was removed. An experimental TCP port-scan rule was also removed because the current mirror point is the Juice Shop backend ENI, not the ALB.

### Important architectural lesson

An ALB-facing port scan does not automatically traverse the Juice Shop ENI. Therefore, a Suricata sensor attached to a Traffic Mirror source on the Juice Shop ENI cannot be claimed as a detector for **ALB-level reconnaissance**.

The project intentionally documents this limitation instead of manufacturing a false validation result.

### 📸 Screenshot placeholders

> **[SCREENSHOT — Suricata startup / rules loaded]**  
> `docs/screenshots/suricata/suricata-healthy.png`

> **[SCREENSHOT — Suricata SQLi event / SID 1000003]**  
> `docs/screenshots/suricata/sqli-event.png`

> **[SCREENSHOT — Traffic Mirror / tcpdump VXLAN evidence]**  
> `docs/screenshots/suricata/traffic-mirroring.png`

---

# 10. 🛡️ Wazuh SIEM / HIDS

Wazuh acts as the central security analysis and correlation layer.

### Active agents

```text
000  cloudoptima-wazuh       Local
001  juice-shop-demo         Active
002  suricata-sensor         Active
004  cloudoptima-devsecops   Active
```

### Security data sources demonstrated

- Juice Shop host telemetry
- Suricata alerts
- SSH brute-force detection
- AWS CloudTrail events
- AWS-S3 ingestion
- Host integrity/security telemetry

### 📸 Screenshot placeholders

> **[SCREENSHOT — Wazuh agent list]**  
> `docs/screenshots/wazuh/agents-active.png`

> **[SCREENSHOT — SSH brute-force / rule 5712]**  
> `docs/screenshots/wazuh/ssh-bruteforce.png`

> **[SCREENSHOT — Suricata SQLi event in Wazuh]**  
> `docs/screenshots/wazuh/suricata-sqli.png`

> **[SCREENSHOT — CloudTrail rule 80202]**  
> `docs/screenshots/wazuh/cloudtrail-80202.png`

---

# 11. ☁️ AWS CloudTrail → S3 → Wazuh

CloudTrail was configured as a multi-region trail and delivered logs into a dedicated S3 bucket.

```text
AWS API / Control Plane
          │
          ▼
      CloudTrail
          │
          ▼
          S3
          │
          ▼
    Wazuh aws-s3 module
          │
          ▼
      Wazuh analysis
          │
          ▼
     Wazuh Dashboard
```

### Final CloudTrail state

```text
Trail:          cloudoptima-security-trail
Region:         eu-north-1
Multi-region:   enabled
Logging:        True
Last failure:   None
S3 delivery:    verified
```

### AWS/Wazuh IAM design

A dedicated Wazuh CloudTrail read role/profile was created so that Wazuh could retrieve CloudTrail data from S3 without embedding long-lived AWS access keys on the host.

### 📸 Screenshot placeholders

> **[SCREENSHOT — CloudTrail trail status]**  
> `docs/screenshots/cloudtrail/trail-status.png`

> **[SCREENSHOT — CloudTrail objects delivered to S3]**  
> `docs/screenshots/cloudtrail/s3-delivery.png`

> **[SCREENSHOT — Wazuh AWS-S3 module fetching logs]**  
> `docs/screenshots/cloudtrail/wazuh-s3-ingestion.png`

---

# 12. 📊 Wazuh Security Operations Dashboard

The final dashboard is:

```text
CloudOptima Security Operations
```

### Dashboard goals

- overall alert volume
- high/critical alerts
- authentication failures
- Suricata activity
- SQL injection detections
- CloudTrail events
- alert volume by agent
- validated WAF attack evidence / documentation context

### Time-window convention

```text
Last 24 hours  → default / historical SOC overview
Last 15 minutes → live attack demonstration
```

### Agent naming cleanup

The DevSecOps agent was renamed from the EC2 hostname-style name to:

```text
cloudoptima-devsecops
```

The existing Wazuh agent ID and key were preserved, avoiding unnecessary re-enrollment.

### 📸 Screenshot placeholders

> **[SCREENSHOT — Final CloudOptima Security Operations dashboard]**  
> `docs/screenshots/wazuh/final-dashboard.png`

> **[SCREENSHOT — Last 15 minutes live view]**  
> `docs/screenshots/wazuh/dashboard-15m.png`

> **[SCREENSHOT — Last 24 hours overview]**  
> `docs/screenshots/wazuh/dashboard-24h.png`

---

# 13. 📡 Observability Stack

The runtime observability layer is intentionally separate from the security stack.

```text
Node Exporter ─► Prometheus ─► Grafana

Promtail ─► Loki ─► Grafana
```

### Responsibilities

| Tool | Purpose |
|---|---|
| Prometheus | Metrics collection and time-series storage |
| Node Exporter | Host metrics |
| Loki | Log aggregation |
| Promtail | Log shipping |
| Grafana | Visualization and operational dashboards |

### 📸 Screenshot placeholders

> **[SCREENSHOT — Grafana infrastructure dashboard]**  
> `docs/screenshots/grafana/infrastructure-overview.png`

> **[SCREENSHOT — Grafana alerting]**  
> `docs/screenshots/grafana/alerting.png`

---

# 14. 🔄 End-to-End Security Workflow

```text
Developer
   │
   ▼
CloudOptima IDP
   │
   ▼
GitHub
   │
   ▼
Jenkins
   │
   ├── Code security
   ├── Secret detection
   ├── IaC security
   ├── Cost validation
   ├── Policy validation
   ├── Container security
   └── Configuration automation
   │
   ▼
AWS Deployment
   │
   ▼
ALB + WAF
   │
   ▼
Juice Shop
   │
   ├── Wazuh Agent
   └── Traffic Mirror
          │
          ▼
       Suricata
          │
          ▼
        Wazuh
          │
          ▼
       SOC View
```

Separately:

```text
AWS Control Plane
       │
       ▼
   CloudTrail
       │
       ▼
       S3
       │
       ▼
     Wazuh
```

---

# 15. 🧪 Final Validation Matrix

| Control | Validation | Result |
|---|---|---|
| WAF attached to ALB | `get-web-acl-for-resource` | ✅ |
| ALB health | `describe-load-balancers` | ✅ Active |
| Legitimate application traffic | `curl -I ALB` | ✅ HTTP 200 |
| SQLi prevention | WAF sampled request | ✅ BLOCK |
| XSS prevention | WAF sampled request / 403 | ✅ BLOCK |
| LFI prevention | `LFI_URIPATH` | ✅ BLOCK |
| Log4Shell prevention | `Log4J#RC_QUERYSTRING` | ✅ BLOCK |
| SSRF prevention | `EC2MetaDataSSRF_QUERYARGUMENTS` | ✅ BLOCK |
| Suricata health | config test + Docker status | ✅ |
| Suricata packet drops | runtime counters | ✅ 0 drops observed |
| Wazuh Manager health | `wazuh-control status` | ✅ |
| Wazuh agents | `agent_control -l` | ✅ Active |
| CloudTrail logging | `get-trail-status` | ✅ |
| CloudTrail → S3 | object delivery | ✅ |
| Wazuh AWS-S3 ingestion | `ossec.log` | ✅ |
| Dashboard persistence | logout/login | ✅ |

---

# 16. 📁 Proposed Repository Documentation Structure

```text
CloudOptima/
│
├── README.md
│
├── docs/
│   ├── architecture/
│   │   ├── cloudoptima-architecture.png
│   │   ├── network-flow.png
│   │   ├── devsecops-pipeline.png
│   │   └── security-data-flow.png
│   │
│   ├── screenshots/
│   │   ├── idp/
│   │   ├── github/
│   │   ├── jenkins/
│   │   ├── terraform/
│   │   ├── devsecops/
│   │   ├── waf/
│   │   ├── suricata/
│   │   ├── wazuh/
│   │   ├── cloudtrail/
│   │   └── grafana/
│   │
│   ├── implementation/
│   │   ├── 01-idp.md
│   │   ├── 02-github.md
│   │   ├── 03-jenkins.md
│   │   ├── 04-devsecops.md
│   │   ├── 05-aws-infrastructure.md
│   │   ├── 06-waf.md
│   │   ├── 07-suricata.md
│   │   ├── 08-wazuh.md
│   │   ├── 09-cloudtrail.md
│   │   └── 10-observability.md
│   │
│   ├── attacks/
│   │   ├── 01-sqli.md
│   │   ├── 02-xss.md
│   │   ├── 03-lfi.md
│   │   ├── 04-log4j.md
│   │   └── 05-ssrf.md
│   │
│   ├── operations/
│   │   ├── troubleshooting.md
│   │   ├── health-checks.md
│   │   └── incident-response.md
│   │
│   └── command-reference.md
│
├── backend/
├── frontend/
├── terraform/
├── ansible/
├── jenkins/
├── policies/
├── scripts/
└── .github/
    └── workflows/
```

---

# 17. 🧾 Command & Configuration Documentation Policy

The final repository will include an **exact command reference**, but commands will be grouped by purpose instead of dumped into one giant terminal transcript.

Example:

```text
AWS discovery
→ WAF creation
→ WAF association
→ CloudTrail
→ IAM
→ Suricata
→ Traffic Mirror validation
→ Wazuh
→ Dashboard validation
→ Attack validation
```

Each command will include:

1. **Where it was executed**
2. **Why it was executed**
3. **What it changes / observes**
4. **Expected output**
5. **Observed output / evidence**
6. **Operational/security significance**

> **Accuracy note:** I have the commands and outputs that are present in our conversation context, but I do not have a guaranteed verbatim transcript of every command ever executed in your terminal. In later documentation phases, any command that is not directly supported by our retained project history will be marked as a placeholder rather than fabricated.

---

# 18. 🎥 Recruiter-Facing Demonstration Flow

A 10–15 minute technical demonstration can follow this order:

```text
1. Project architecture
2. IDP / developer request
3. GitHub workflow
4. Jenkins DevSecOps pipeline
5. Infrastructure deployment
6. AWS ALB + WAF
7. Juice Shop
8. Five controlled attacks
9. WAF BLOCK evidence
10. Suricata detection
11. Wazuh correlation
12. CloudTrail → Wazuh
13. Grafana observability
14. Final security dashboard
```

This sequence maps naturally to target roles:

- SOC Analyst
- Cybersecurity Analyst
- Cloud Security Engineer
- DevSecOps Engineer
- DevOps Engineer
- Security Operations / Detection Engineer

---

# 19. 🧠 Key Engineering Decisions

### Why WAF + Suricata + Wazuh?

Because they solve different problems:

```text
WAF      = prevent malicious web requests
Suricata = detect network patterns
Wazuh    = correlate host/network/security events
```

### Why passive Suricata instead of inline IPS?

The current Traffic Mirror architecture provides detection without inserting a new routing dependency into the application path.

### Why not force port scanning through Suricata?

The current mirror source is the Juice Shop backend ENI. ALB-facing reconnaissance may terminate before reaching that ENI. The project therefore documents the observation-point limitation instead of claiming unsupported detection coverage.

### Why keep WAF as the web-prevention layer?

It blocks application-layer attacks before they reach the vulnerable application, while preserving a clean public ALB entry point.

---

# 20. 📚 Documentation Roadmap

This README is the foundation. The following phases will expand it into a complete engineering repository.

### Phase 1 — Architecture & Executive Overview

✅ This document section.

### Phase 2 — Internal Developer Platform

- Flask application
- PostgreSQL
- project structure
- Terraform generator
- Ansible generator
- GitHub integration
- configuration files
- `.env` handling
- deployment approach
- screenshots
- troubleshooting

### Phase 3 — DevSecOps Pipeline

- Jenkins architecture
- Jenkinsfile
- every pipeline stage
- tool installation
- credentials model
- Terraform state
- S3 / locking
- SonarQube
- GitLeaks
- Checkov
- Infracost
- OPA
- Docker
- Trivy
- ECR
- Ansible
- pipeline screenshots
- failure examples and fixes

### Phase 4 — Cloud Infrastructure

- EC2 roles
- IAM
- networking
- ALB
- target groups
- security groups
- S3
- CloudTrail
- Traffic Mirroring
- DNS/public path
- resource relationships

### Phase 5 — Runtime Security / SOC

- WAF
- Suricata
- Wazuh
- CloudTrail ingestion
- agent enrollment
- custom rules
- dashboard construction
- alert flow
- attack demonstrations

### Phase 6 — Observability

- Prometheus
- Node Exporter
- Loki
- Promtail
- Grafana
- dashboards
- alerting

### Phase 7 — Attack Laboratory

For each attack:

```text
Threat model
→ request/payload
→ WAF rule
→ expected result
→ actual result
→ WAF evidence
→ Suricata evidence
→ Wazuh evidence
→ screenshot
→ analyst interpretation
```

### Phase 8 — Operations & Troubleshooting

Document every important issue encountered during the build, including:

- AWS credentials / IAM resolution
- Jenkins Java compatibility
- suspicious process investigation
- Terraform state
- Wazuh AWS-S3 IAM errors
- Wazuh JSON decoder tuning
- Suricata rule management
- traffic mirroring validation
- WAF rule tuning
- dashboard persistence
- agent naming

### Phase 9 — Final Security Review

- threat model
- attack surface
- controls matrix
- known limitations
- residual risks
- improvements for production
- lessons learned

### Phase 10 — Recruiter / Portfolio Packaging

- polished README
- architecture diagrams
- portfolio summary
- screenshots
- demo video script
- project outcomes
- technical skill mapping
- future roadmap

---

# ⭐ Final Project Narrative

> **CloudOptima demonstrates how a developer-facing Internal Developer Platform can be connected to GitHub-driven DevSecOps automation and a layered cloud security architecture. The platform combines infrastructure automation, secure CI/CD, application-layer prevention, network detection, host/SIEM correlation, cloud audit logging, and operational observability into one end-to-end workflow.**

The project is intentionally designed not only to show that individual tools work, but to demonstrate **how the tools work together**:

```text
Developer intent
      ↓
Platform automation
      ↓
Source control
      ↓
Secure CI/CD
      ↓
Cloud deployment
      ↓
Web protection
      ↓
Runtime detection
      ↓
Security correlation
      ↓
Observability
      ↓
Evidence-driven security operations
```

---

## ⚠️ Public Repository Security Notice

Before publishing this repository publicly:

- remove real AWS account IDs where not needed
- remove public IPs if sensitive
- remove passwords, tokens and API keys
- never commit `.env` files containing secrets
- use placeholders for credentials
- sanitize CloudTrail logs if required
- sanitize screenshots containing sensitive account information
- review IAM policies for least privilege
- review all command outputs for secrets

---

<p align="center">
  <strong>CloudOptima</strong><br/>
  <em>Build Secure. Deploy Repeatably. Detect Early. Respond Intelligently.</em>
</p>


# 🧩 CloudOptima — Phase 2: Internal Developer Platform (IDP)

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Flask-000000?logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/IaC-Terraform-844FBA?logo=terraform&logoColor=white" alt="Terraform"/>
  <img src="https://img.shields.io/badge/Config-Ansible-EE0000?logo=ansible&logoColor=white" alt="Ansible"/>
  <img src="https://img.shields.io/badge/SCM-GitHub-181717?logo=github&logoColor=white" alt="GitHub"/>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python"/>
</p>

<p align="center">
  <strong>Developer Self-Service Layer of CloudOptima</strong>
</p>

<p align="center">
  Flask portal → PostgreSQL → Terraform/Ansible generation → GitHub → CI/CD
</p>

> **Phase 2 scope:** This document describes the CloudOptima Internal Developer Platform (IDP), its purpose, application structure, database integration, infrastructure/configuration generation, GitHub workflow, deployment approach, troubleshooting history, commands used during implementation, and the engineering decisions behind the design.

---

# 1. 🎯 Objective of the IDP

The Internal Developer Platform is the **developer-facing front door** of CloudOptima.

Instead of asking a developer to manually create infrastructure files, understand every Terraform resource, write Ansible configuration, configure a Git repository, and then trigger CI/CD manually, the IDP is intended to provide a simpler self-service workflow.

The conceptual workflow is:

```text
Developer
   │
   │ Self-service request
   ▼
CloudOptima Flask Portal
   │
   ├── Authentication / application logic
   ├── PostgreSQL
   ├── Terraform generator
   ├── Ansible generator
   └── GitHub integration
           │
           ▼
        GitHub
           │
           ▼
        Jenkins
           │
           ▼
   DevSecOps pipeline
```

The IDP therefore separates **developer intent** from the low-level implementation of infrastructure and deployment.

---

# 2. 🏗️ IDP Architecture

```text
                         ┌───────────────────────┐
                         │      Developer        │
                         │                       │
                         │ Select environment    │
                         │ / application config  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │  CloudOptima IDP       │
                         │                        │
                         │ Flask                  │
                         │ Flask-Login            │
                         │ SQLAlchemy             │
                         │ Terraform Generator    │
                         │ Ansible Generator      │
                         │ GitHub Integration     │
                         └───────┬────────┬───────┘
                                 │        │
                    persistence │        │ generated artifacts
                                 │        │
                                 ▼        ▼
                         ┌───────────┐  ┌───────────────┐
                         │PostgreSQL │  │ Terraform /   │
                         │           │  │ Ansible files │
                         └───────────┘  └───────┬───────┘
                                                 │
                                                 ▼
                                          ┌────────────┐
                                          │   GitHub   │
                                          └─────┬──────┘
                                                │
                                                ▼
                                          ┌────────────┐
                                          │  Jenkins   │
                                          └────────────┘
```

---

# 3. 🧱 Technology Stack

| Layer | Technology | Why it was used |
|---|---|---|
| Web application | Flask | Lightweight Python web framework suitable for a focused IDP prototype |
| Authentication | Flask-Login | Session/user authentication support |
| ORM | Flask-SQLAlchemy | Database access through SQLAlchemy integration |
| Database | PostgreSQL | Persistent relational storage |
| Configuration | python-dotenv | Environment-specific configuration through `.env` |
| WSGI/application layer | Flask / Werkzeug | Application runtime and HTTP utilities |
| Infrastructure generation | Terraform | Declarative infrastructure generation |
| Configuration management | Ansible | Post-provisioning configuration automation |
| Source control | GitHub | Central source of truth and pipeline trigger point |
| CI/CD | Jenkins | Build, security and deployment orchestration |

---

# 4. 📁 Application Structure

The working Flask implementation used the following structure/concepts:

```text
cloudoptima/
│
├── backend/
│   ├── app.py
│   └── models.py
│
├── config/
│   └── .env
│
├── templates/
│   └── ... Flask HTML templates ...
│
├── requirements.txt
│
└── ... generated/project files ...
```

> **Repository note:** the exact final repository tree should be updated with the actual files from the GitHub source repository. This document records the files that were explicitly established during the implementation history and leaves placeholders where the final tree should be authoritative.

---

# 5. 🐍 Python Dependencies

The Flask portal used the following dependency versions during the implementation:

```text
Flask==3.0.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
psycopg2-binary==2.9.9
python-dotenv==1.0.1
Werkzeug==3.0.1
```

### Why these packages?

| Package | Role |
|---|---|
| `Flask` | Web application framework |
| `Flask-SQLAlchemy` | SQLAlchemy integration with Flask |
| `Flask-Login` | Login/session management |
| `psycopg2-binary` | PostgreSQL database driver |
| `python-dotenv` | Loads environment variables from `.env` |
| `Werkzeug` | Flask's underlying WSGI/web utility layer |

### Screenshot placeholder

> 📸 **SCREENSHOT — `docs/screenshots/idp/requirements.png`**
>
> Show the `requirements.txt` file containing the dependency list.

---

# 6. 🗄️ PostgreSQL Integration

PostgreSQL was selected as the persistent database for the portal.

The Flask application used SQLAlchemy through `Flask-SQLAlchemy`, while PostgreSQL was accessed through `psycopg2-binary`.

The configuration was deliberately kept outside application code using an environment file.

## Environment configuration

The implementation used:

```text
config/.env
```

with a database connection configuration represented by a `DATABASE_URI`/database URI setting.

> ⚠️ **Never commit the real `.env` file or database credentials into GitHub.**
>
> The public repository should contain a sanitized example such as:
>
> ```text
> config/.env.example
> ```
>
> with placeholders only.

Recommended pattern:

```dotenv
DATABASE_URI=postgresql://<user>:<password>@<host>:5432/<database>
```

---

# 7. 🔐 Configuration and Secret Handling

The initial prototype used environment-based configuration:

```text
Application code
      │
      └── reads environment variables
                 │
                 ▼
             config/.env
```

The final repository should use:

```text
.env                # local only, never committed
.env.example        # committed template, no secrets
```

Recommended `.gitignore` entries:

```gitignore
.env
*.env
__pycache__/
*.pyc
.venv/
venv/
```

If the project is published publicly, **rotate any credential that was ever exposed in shell history, screenshots, terminal output, or repository history**.

---

# 8. 🐘 PostgreSQL Setup — Implementation Record

The portal was backed by PostgreSQL during the EC2 prototype stage.

The implementation included the usual administrative sequence:

```text
1. Install PostgreSQL
2. Start/enable PostgreSQL
3. Create application database
4. Create application database user
5. Grant database privileges
6. Configure Flask DATABASE_URI
7. Start Flask application
8. Validate database-backed application behavior
```

Representative service-management commands used during the setup/troubleshooting workflow included:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

> **Evidence note:** the exact database-name/user/password values are intentionally not reproduced here. The final repository should use placeholders and never publish credentials.

### Screenshot placeholders

> 📸 **SCREENSHOT — `docs/screenshots/idp/postgresql-service.png`**
>
> PostgreSQL service active.

> 📸 **SCREENSHOT — `docs/screenshots/idp/postgresql-db-user.png`**
>
> Sanitized proof of database/user setup. Do not expose passwords.

---

# 9. 🧬 Database/Application Layer

The application used a model layer represented by:

```text
backend/models.py
```

and the Flask application entry point:

```text
backend/app.py
```

The model layer handled application persistence while the Flask application provided:

- routes
- authentication/session handling
- request processing
- template rendering
- generator integration
- database access

### SQLAlchemy version compatibility note

During development, SQLAlchemy emitted a warning around the legacy form:

```python
Query.get()
```

The warning indicated that `Query.get()` is considered legacy in SQLAlchemy 2.x-era usage and that the newer session-based approach is preferred.

Recommended modern pattern:

```python
session.get(Model, primary_key)
```

> 📸 **SCREENSHOT — `docs/screenshots/idp/sqlalchemy-warning.png`**
>
> The development log showing the SQLAlchemy compatibility warning. This is useful as a troubleshooting/evolution note, not as a production error.

---

# 10. 🌐 Flask Portal Runtime

The Flask portal was initially hosted directly on an EC2 instance as a rapid prototype.

The application was exposed on a single application port:

```text
5000/TCP
```

The single-port approach was intentionally kept simple for the prototype and demonstration.

### Runtime verification

Commands used during troubleshooting included:

```bash
ss -ltnp
```

and:

```bash
curl -I http://127.0.0.1:5000
```

or equivalent local service checks.

The EC2 host was also checked for listening services such as:

```text
5000 → Flask
8080 → Jenkins
```

### Important architectural lesson

The portal working on EC2 proved the application concept, but deploying the development-facing Flask portal directly to a manually configured EC2 server is **not the target production architecture**.

A production-oriented evolution would be:

```text
Developer
   │
   ▼
ALB / ingress
   │
   ▼
Containerized Flask service
   │
   ├── managed/isolated PostgreSQL
   └── secrets manager
```

or an equivalent managed/container platform.

The project deliberately documents this distinction instead of presenting the prototype as a production-ready deployment.

---

# 11. 🧪 Flask Application Development Workflow

The working development loop was:

```text
Modify Flask code
      ↓
Validate Python/application configuration
      ↓
Start Flask
      ↓
Test locally on EC2
      ↓
Check port/listener
      ↓
Check AWS Security Group
      ↓
Check application response
      ↓
Move stable source into GitHub
```

### Example application startup pattern

The implementation used the Flask application entry point under:

```text
backend/app.py
```

and the application was exposed on port `5000`.

A representative development command is:

```bash
python3 backend/app.py
```

> **Use the exact startup command from the final source repository in the final documentation if it differs.** This README intentionally avoids inventing a command that was not preserved verbatim in the project history.

---

# 12. 🧭 EC2 Prototype Networking

During the initial Flask portal phase, the application was hosted on EC2 and browser connectivity initially failed even though the application was running.

The troubleshooting sequence was:

```text
Flask running?
      ↓
Port listening?
      ↓
UFW?
      ↓
AWS Security Group?
      ↓
Browser connectivity?
```

The implementation verified the listener using:

```bash
ss -ltnp
```

The project also checked UFW status:

```bash
sudo ufw status
```

The relevant lesson was that **a process listening on `0.0.0.0:5000` is not sufficient for external reachability**; the AWS security group/network path must also permit the connection.

### Screenshot placeholders

> 📸 **SCREENSHOT — `docs/screenshots/idp/flask-listening.png`**
>
> `ss -ltnp` showing Flask listening on port 5000.

> 📸 **SCREENSHOT — `docs/screenshots/idp/aws-sg-flask-port.png`**
>
> AWS Security Group rule used during development. Sanitize unrelated infrastructure details if publishing publicly.

---

# 13. 🔧 Terraform Generator

One of the IDP's core functions was the **Terraform generator**.

The purpose is to translate higher-level developer/platform requirements into reproducible Infrastructure as Code rather than requiring the developer to hand-write every Terraform resource.

Conceptually:

```text
Developer input
      │
      ▼
Flask portal
      │
      ▼
Terraform generator
      │
      ▼
Generated Terraform files
      │
      ▼
GitHub
      │
      ▼
Jenkins
      │
      ▼
Terraform validation / plan / apply
```

### Why Terraform generation belongs in an IDP

The generator establishes a controlled abstraction boundary:

```text
Developer intent
      ↓
Platform-approved template
      ↓
Terraform
      ↓
Cloud infrastructure
```

This can reduce ad-hoc infrastructure creation and makes it easier to enforce:

- naming conventions
- required tags
- network standards
- approved resource types
- security defaults
- cost controls
- policy rules

### Repository placeholders

The final repository should include the actual generator source files under an explicit path such as:

```text
idp/
├── generators/
│   ├── terraform/
│   └── ansible/
```

> **Use the actual project paths from GitHub as the source of truth when completing this section.**

### Screenshot placeholders

> 📸 **SCREENSHOT — `docs/screenshots/idp/terraform-generator-ui.png`**
>
> Portal form used to request/generate infrastructure.

> 📸 **SCREENSHOT — `docs/screenshots/idp/generated-terraform.png`**
>
> Generated Terraform output with secrets redacted.

---

# 14. ⚙️ Ansible Generator

The IDP also included an **Ansible generator** so that infrastructure provisioning and post-provisioning configuration could be separated.

The conceptual split is:

```text
Terraform
   ↓
Provision infrastructure

Ansible
   ↓
Configure operating system / application
```

This separation is useful because Terraform describes **desired infrastructure state**, while Ansible is suited to **host/application configuration tasks**.

The IDP therefore targets a workflow such as:

```text
Developer request
      ↓
Terraform generated
      ↓
Infrastructure deployed
      ↓
Ansible generated
      ↓
Configuration applied
```

### Screenshot placeholders

> 📸 **SCREENSHOT — `docs/screenshots/idp/ansible-generator.png`**
>
> Portal-generated Ansible configuration.

> 📸 **SCREENSHOT — `docs/screenshots/idp/ansible-run.png`**
>
> Jenkins/Ansible execution evidence.

---

# 15. 🔗 GitHub Integration

GitHub is the boundary between **platform self-service** and **DevSecOps automation**.

The intended lifecycle is:

```text
Flask IDP
   │
   │ generate project/configuration
   ▼
Git repository
   │
   ▼
GitHub
   │
   │ push / update
   ▼
Jenkins trigger
   │
   ▼
DevSecOps pipeline
```

The repository becomes the reviewable source of truth for generated infrastructure/configuration.

This is especially important for an engineering audience because it provides:

- Git history
- peer review
- pull requests
- reproducibility
- rollback capability
- CI/CD integration
- auditability

---

# 16. 🔒 GitHub / Jenkins Boundary — Important Engineering Practice

One of the key implementation lessons from CloudOptima is **not to treat the Jenkins workspace as a development environment**.

Jenkins checks out a repository commit into its workspace. That workspace is disposable and may be placed in detached-HEAD state.

Therefore:

```text
❌ Do not edit Jenkins workspace
❌ Do not commit from Jenkins workspace
❌ Do not push source changes from /var/lib/jenkins/...

✅ Edit in GitHub / normal development clone
✅ Commit normally
✅ Push to GitHub
✅ Let Jenkins check out the new commit
```

This prevents detached-HEAD and source-of-truth problems.

### Recommended source workflow

```text
Developer workstation / normal Git clone
                 │
                 ▼
              git add
                 │
                 ▼
             git commit
                 │
                 ▼
             git push
                 │
                 ▼
               GitHub
                 │
                 ▼
              Jenkins
```

---

# 17. 🔑 Terraform State Integration

The CloudOptima implementation used remote Terraform state backed by AWS S3.

The project established the following buckets during the AWS workflow:

```text
cloudoptima-idp-artifacts-<ACCOUNT_ID>
cloudoptima-tf-state-12345
```

The Terraform state architecture concept is:

```text
Jenkins
   │
   ▼
Terraform
   │
   ▼
S3 remote state
```

The project also established state locking through a DynamoDB-backed workflow during Terraform setup.

### Important configuration

The application/project configuration history referenced:

```text
TF_STATE_BUCKET
```

inside the CloudOptima environment configuration.

> 🔐 **Never publish real account IDs, bucket credentials, access keys or secret values.** Bucket names containing an AWS account number should be sanitized in public documentation where practical.

### Screenshot placeholder

> 📸 **SCREENSHOT — `docs/screenshots/idp/terraform-state-s3.png`**
>
> Sanitized S3 bucket/state configuration.

---

# 18. 💰 Cost Awareness

CloudOptima was designed with cost and infrastructure visibility in mind.

The platform therefore includes **Infracost** in the downstream DevSecOps pipeline.

The IDP's Terraform generation model supports the broader principle:

```text
Developer request
      ↓
Generated IaC
      ↓
Cost estimation
      ↓
Security checks
      ↓
Approval / deployment
```

This moves cost awareness earlier into the developer workflow.

---

# 19. 🛡️ Security by Design in the IDP

The IDP itself is intentionally positioned as a **controlled entry point** rather than a direct AWS console replacement.

A mature version should enforce:

| Control | Purpose |
|---|---|
| Authentication | Identify developer |
| Authorization | Restrict what developers may create |
| Input validation | Prevent unsafe generation parameters |
| Template allowlists | Prevent arbitrary resources/configuration |
| Secrets externalization | Avoid hard-coded secrets |
| Git review | Human-readable change history |
| CI security gates | Validate generated artifacts |
| Cost checks | Prevent unexpectedly expensive deployments |
| Policy as Code | Enforce organizational rules |
| Audit logging | Track requests and actions |

This model allows the IDP to evolve from a prototype into a platform-engineering control plane.

---

# 20. 🧪 IDP Validation Checklist

The IDP phase was considered functional when the following workflow could be demonstrated:

```text
[ ] Flask portal starts
[ ] Portal reachable on configured application port
[ ] PostgreSQL is running
[ ] Flask can connect to PostgreSQL
[ ] Database-backed functionality works
[ ] Terraform generator produces expected files
[ ] Ansible generator produces expected files
[ ] Generated artifacts can be placed into GitHub
[ ] Jenkins can consume the GitHub source
[ ] Generated infrastructure passes downstream validation
```

### Screenshot placeholders

> 📸 **SCREENSHOT — `docs/screenshots/idp/portal-home.png`**
>
> CloudOptima portal landing/dashboard page.

> 📸 **SCREENSHOT — `docs/screenshots/idp/portal-form.png`**
>
> Developer self-service request form.

> 📸 **SCREENSHOT — `docs/screenshots/idp/postgres-connected.png`**
>
> Evidence that the portal successfully connects to PostgreSQL.

> 📸 **SCREENSHOT — `docs/screenshots/idp/generator-output.png`**
>
> Generated Terraform/Ansible output.

> 📸 **SCREENSHOT — `docs/screenshots/idp/github-repository.png`**
>
> Generated/project files visible in GitHub.

---

# 21. 🧰 Troubleshooting Record

CloudOptima's implementation included several real troubleshooting steps. These are valuable in the final portfolio because they demonstrate operational reasoning rather than only successful end states.

## 21.1 Flask process running but browser cannot connect

### Symptom

The Flask application showed a listening process on port `5000`, but external browser access initially failed.

### Investigation

```bash
ss -ltnp
sudo ufw status
```

The investigation established that application-level listening and AWS network accessibility are separate concerns.

### Lesson

```text
Application listener
        ≠
Network accessibility
```

Both the host and cloud networking path must allow the traffic.

---

## 21.2 Port conflict

A port conflict was encountered during the broader CloudOptima setup.

The general diagnostic approach used was:

```bash
ss -ltnp
```

and process inspection before deciding which service should own the port.

### Lesson

Avoid changing ports blindly. First identify:

```text
PID → process → service → dependency
```

---

## 21.3 PostgreSQL / Flask integration

PostgreSQL was explicitly started and enabled as a system service:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

The application configuration was then connected through the environment-based database URI.

### Lesson

Keep credentials and environment-specific connection details outside source code.

---

## 21.4 SQLAlchemy legacy API warning

The Flask application produced a warning about `Query.get()` being considered legacy in newer SQLAlchemy usage.

### Lesson

During modernization, prefer the current session-oriented API:

```python
session.get(Model, id)
```

rather than continuing to rely on legacy query APIs.

---

# 22. 🚀 Prototype → Production Evolution

The CloudOptima IDP was intentionally built in a time-constrained environment. The working prototype proved the workflow, while the project architecture identifies where a production deployment should evolve.

## Prototype

```text
Developer
   ↓
Flask on EC2
   ↓
PostgreSQL
   ↓
Generated IaC
   ↓
GitHub
```

## Production-oriented evolution

```text
Developer
   ↓
HTTPS / ALB
   ↓
Containerized IDP
   ↓
Managed PostgreSQL
   ↓
Secrets Manager
   ↓
GitHub
   ↓
Jenkins / CI platform
```

### Specific improvements

- Containerize the Flask application.
- Remove manual EC2 application management.
- Use managed PostgreSQL where appropriate.
- Use AWS Secrets Manager/Parameter Store for secrets.
- Put the IDP behind HTTPS.
- Add role-based authorization.
- Add centralized application logging.
- Add automated unit/integration tests.
- Add CI tests for generated Terraform/Ansible.
- Add approval controls for privileged infrastructure actions.

These improvements are deliberately separated from the working prototype so the repository remains technically honest.

---

# 23. 📸 Recommended Evidence Structure

Use a consistent screenshot hierarchy:

```text
 docs/
 ├── screenshots/
 │   └── idp/
 │       ├── portal-home.png
 │       ├── portal-form.png
 │       ├── postgres-service.png
 │       ├── flask-listening.png
 │       ├── generated-terraform.png
 │       ├── generated-ansible.png
 │       ├── github-repository.png
 │       └── github-to-jenkins.png
```

### Screenshot naming convention

Use:

```text
<component>-<purpose>.png
```

Examples:

```text
flask-listening.png
postgres-service.png
terraform-generator-ui.png
ansible-generator.png
github-repository.png
```

Avoid names such as:

```text
Screenshot123.png
finalfinal.png
image2.png
```

---

# 24. 📝 Recommended README Embedding Pattern

For each major implementation section in the main repository README, use the same structure:

```markdown
## Component

### Purpose
Explain what it does.

### Architecture
Show the relevant flow.

### Implementation
Explain what was created.

### Commands
Show reproducible commands.

### Configuration
Show sanitized configuration.

### Validation
Explain how it was tested.

### Evidence
![Flask Portal](docs/screenshots/idp/portal-home.png)

### Production considerations
Explain limitations and improvements.
```

This creates a consistent engineering narrative throughout the repository.

---

# 25. 🔍 Recruiter-Focused Engineering Takeaways

The IDP demonstrates the following practical capabilities:

### Platform Engineering

- Developer self-service
- Infrastructure abstraction
- Template-driven provisioning
- Git-based workflow

### DevOps

- GitHub-centered source workflow
- CI/CD integration
- Terraform automation
- Ansible automation

### Cloud Engineering

- AWS EC2 deployment
- S3-backed Terraform state
- AWS IAM integration
- Cloud infrastructure automation

### Security Engineering

- Secret externalization
- Controlled infrastructure generation
- Shift-left security through downstream pipeline gates
- Security-aware platform design

### Operational Engineering

- Linux service administration
- PostgreSQL administration
- Network troubleshooting
- Cloud security-group troubleshooting
- Application-level diagnostics

---

# 26. ✅ Phase 2 Completion Matrix

| Deliverable | Status | Evidence placeholder |
|---|---:|---|
| Flask portal | ✅ | `portal-home.png` |
| PostgreSQL | ✅ | `postgres-service.png` |
| Database-backed application | ✅ | `postgres-connected.png` |
| Flask authentication/session layer | ✅ | `portal-login.png` |
| Terraform generator | ✅ | `generated-terraform.png` |
| Ansible generator | ✅ | `generated-ansible.png` |
| GitHub integration | ✅ | `github-repository.png` |
| Jenkins handoff | ✅ | `github-to-jenkins.png` |
| EC2 prototype deployment | ✅ | `flask-listening.png` |
| Prototype limitations documented | ✅ | This section |
| Secret-handling guidance | ✅ | `.env.example` |
| Troubleshooting record | ✅ | This section |

---

# 27. 🗺️ Phase 2 → Phase 3 Handoff

The IDP is the **front door**. The next phase documents what happens after GitHub receives the source.

```text
             PHASE 2
        Internal Developer Platform

Developer
   ↓
Flask
   ↓
Terraform / Ansible generation
   ↓
GitHub

               │
               │ HANDOFF
               ▼

             PHASE 3
          DevSecOps Pipeline

GitHub
   ↓
Jenkins
   ↓
Source validation
   ↓
Security gates
   ↓
Terraform
   ↓
Docker / Trivy / ECR
   ↓
Ansible
   ↓
Deployment
```

Phase 3 should document **every Jenkins stage**, the Jenkinsfile structure, GitHub-to-Jenkins flow, tool configuration, failures encountered, security gates, artifacts, screenshots, and successful pipeline evidence.

---

# 28. 📚 Phase 2 Evidence Checklist

Before marking this phase complete in the public repository, add the following screenshots/evidence:

```text
[ ] IDP home/dashboard
[ ] Developer request form
[ ] PostgreSQL service running
[ ] Database connectivity
[ ] Flask application running
[ ] Port 5000 listener
[ ] Terraform generated output
[ ] Ansible generated output
[ ] GitHub repository containing generated/source files
[ ] GitHub → Jenkins trigger/build
[ ] Sanitized .env.example
[ ] Final repository tree
```

> 🔐 **Before publishing:** inspect screenshots for passwords, API tokens, private keys, session cookies, AWS account details, private IPs that should not be public, GitHub secrets, database connection strings, and any other sensitive information.

---

# 🏁 Phase 2 Summary

The CloudOptima IDP establishes a developer-oriented abstraction layer over infrastructure and deployment automation.

Its central idea is simple:

```text
Developer intent
      ↓
Self-service portal
      ↓
Generated IaC / configuration
      ↓
GitHub source of truth
      ↓
Automated DevSecOps pipeline
```

The implementation also provides several valuable engineering lessons:

- A working prototype is not automatically production-ready.
- Cloud networking and application listeners must be debugged separately.
- Secrets belong outside source code.
- Jenkins workspaces should not be treated as development clones.
- Generated infrastructure should remain reviewable through Git.
- Platform engineering is most valuable when it reduces complexity for developers without removing governance.

**Phase 2 complete.**

➡️ Continue with **Phase 3 — DevSecOps CI/CD Pipeline**.
