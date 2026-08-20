# ☁️ CloudOptima: A DevSecOps-Integrated Internal Developer Platform for Automated, Secure & Policy-Governed
AWS Provisioning 🕵

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
| Final repository documentation | 🟡 In progress |

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
